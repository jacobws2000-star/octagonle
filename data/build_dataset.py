#!/usr/bin/env python3
"""
Build the Octagonle fighter dataset.

Data source: ESPN's public MMA core API (no key/auth, JSON).
  - League roster:  sports.core.api.espn.com/v2/sports/mma/leagues/ufc/athletes
  - Athlete detail: .../athletes/{id}
  - Records:        .../athletes/{id}/records
  - Event log:      .../athletes/{id}/eventlog   (earliest event -> UFC debut year)

Champion tags: data/champions.py (curated set merged by normalized name).

Output: public/fighters.json  (consumed by the static game; the live site hits no API).

All network responses are cached under data/.cache/ so reruns are cheap and polite.
Run:  python3 data/build_dataset.py   [--limit N] [--refresh]
"""

import json
import os
import re
import sys
import time
import unicodedata
import urllib.request
import urllib.error
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(HERE, ".cache")
OUT_PATH = os.path.join(HERE, "..", "public", "fighters.json")
API = "https://sports.core.api.espn.com/v2/sports/mma"
UA = "octagonle-dataset-builder/1.0 (personal project; build-time only)"
SLEEP = 0.05  # polite delay between uncached requests

os.makedirs(CACHE_DIR, exist_ok=True)


def _cache_path(url):
    key = re.sub(r"[^a-zA-Z0-9]+", "_", url)[:180]
    return os.path.join(CACHE_DIR, key + ".json")


def fetch(url, refresh=False):
    """GET a JSON URL with on-disk caching and basic retry."""
    cp = _cache_path(url)
    if not refresh and os.path.exists(cp):
        with open(cp) as f:
            return json.load(f)
    last_err = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8"))
            with open(cp, "w") as f:
                json.dump(data, f)
            time.sleep(SLEEP)
            return data
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            last_err = e
            time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(f"failed to fetch {url}: {last_err}")


def norm_name(name):
    """Normalize a name for cross-source matching (strip accents, lowercase)."""
    if not name:
        return ""
    n = unicodedata.normalize("NFKD", name)
    n = "".join(c for c in n if not unicodedata.combining(c))
    n = re.sub(r"[^a-z0-9 ]", "", n.lower()).strip()
    n = re.sub(r"\s+", " ", n)
    return n


def athlete_ids():
    """Collect every UFC athlete id via paginated league roster."""
    ids = []
    page = 1
    while True:
        d = fetch(f"{API}/leagues/ufc/athletes?limit=1000&page={page}")
        items = d.get("items", [])
        for it in items:
            m = re.search(r"/athletes/(\d+)", it.get("$ref", ""))
            if m:
                ids.append(m.group(1))
        if page >= d.get("pageCount", 1):
            break
        page += 1
    return ids


def get_record(aid):
    try:
        d = fetch(f"{API}/athletes/{aid}/records?lang=en&region=us")
    except RuntimeError:
        return None
    for it in d.get("items", []):
        if it.get("name") == "overall":
            stats = {s["name"]: s.get("value") for s in it.get("stats", [])}
            return {
                "wins": int(stats.get("wins", 0) or 0),
                "losses": int(stats.get("losses", 0) or 0),
                "draws": int(stats.get("draws", 0) or 0),
                "summary": it.get("summary", ""),
            }
    return None


def get_debut_year(aid):
    """UFC debut year = date of the earliest event in the athlete's event log.

    The eventlog is ordered newest-first and each item's `event` is a $ref, so
    the debut is the last item; we fetch just that one event to read its date.
    """
    try:
        d = fetch(f"{API}/athletes/{aid}/eventlog?lang=en&region=us")
    except RuntimeError:
        return None
    ev = d.get("events", {})
    items = ev.get("items", []) if isinstance(ev, dict) else []
    if not items:
        return None
    ref = (items[-1].get("event") or {}).get("$ref")
    if not ref:
        return None
    try:
        edata = fetch(ref)
    except RuntimeError:
        return None
    dt = edata.get("date")
    if dt:
        m = re.match(r"(\d{4})", dt)
        if m:
            return int(m.group(1))
    return None


def build(limit=None, refresh=False):
    try:
        from champions import CHAMPION_NAMES
    except ImportError:
        CHAMPION_NAMES = set()
    champ_norm = {norm_name(n) for n in CHAMPION_NAMES}

    ids = athlete_ids()
    if limit:
        ids = ids[:limit]
    print(f"[roster] {len(ids)} athlete ids", file=sys.stderr)

    fighters = []
    kept = 0
    for i, aid in enumerate(ids):
        if i % 100 == 0:
            print(f"  ...{i}/{len(ids)} (kept {kept})", file=sys.stderr)
        try:
            d = fetch(f"{API}/athletes/{aid}?lang=en&region=us", refresh=refresh)
        except RuntimeError:
            continue

        # Active-roster filter
        if not d.get("active"):
            continue
        wc = (d.get("weightClass") or {}).get("text")
        flag = (d.get("flag") or {})
        nationality = flag.get("alt")
        dob = d.get("dateOfBirth")
        if not wc or not nationality or nationality == "default" or not dob:
            continue

        rec = get_record(aid)
        if not rec:
            continue

        name = d.get("displayName") or d.get("fullName")
        fighters.append({
            "id": aid,
            "name": name,
            "nickname": d.get("nickname") or "",
            "weightClass": wc,
            "nationality": nationality,
            "heightIn": d.get("height"),
            "displayHeight": d.get("displayHeight"),
            "reachIn": d.get("reach"),
            "stance": (d.get("stance") or {}).get("text") or "",
            "dob": dob,
            "wins": rec["wins"],
            "losses": rec["losses"],
            "draws": rec["draws"],
            "record": rec["summary"],
            "debutYear": get_debut_year(aid),
            "isChampion": norm_name(name) in champ_norm,
            "headshot": f"https://a.espncdn.com/i/headshots/mma/players/full/{aid}.png",
        })
        kept += 1

    # De-dup by normalized name, keep the one with most fights.
    by_name = {}
    for f in fighters:
        k = norm_name(f["name"])
        if k not in by_name or (f["wins"] + f["losses"]) > (by_name[k]["wins"] + by_name[k]["losses"]):
            by_name[k] = f
    fighters = sorted(by_name.values(), key=lambda x: x["name"])

    meta = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "count": len(fighters),
        "source": "ESPN public MMA API",
    }
    out = {"meta": meta, "fighters": fighters}
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    champs = sum(1 for f in fighters if f["isChampion"])
    print(f"[done] {len(fighters)} fighters -> {OUT_PATH} ({champs} champions tagged)", file=sys.stderr)


if __name__ == "__main__":
    args = sys.argv[1:]
    limit = None
    refresh = "--refresh" in args
    if "--limit" in args:
        limit = int(args[args.index("--limit") + 1])
    build(limit=limit, refresh=refresh)
