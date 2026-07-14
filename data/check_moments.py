#!/usr/bin/env python3
"""
Verify data/moments.py against the Wikipedia numbered-events reference.

Checks, per moment:
  - eventNumber exists and its year matches Wikipedia's date.
  - both fighters' surnames appear in the event's Wikipedia subtitle when that
    subtitle is an "A vs. B" matchup (event-name subtitles are skipped, reported).
  - the clue contains no spoiler: no fighter surname, the event number, or the year.
Also reports duplicate event numbers and the total count.

Expects /tmp/ufc_ref.json (built from the List of UFC events wikitext).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
from moments import MOMENTS

ref = json.load(open("/tmp/ufc_ref.json"))  # {num: [subtitle, year]}


import unicodedata
def strip(x):
    return "".join(c for c in unicodedata.normalize("NFKD", x.lower()) if not unicodedata.combining(c))

def surnames(full):
    return full.split()[-1]

# Fighters whose Wikipedia subtitle uses a nickname/first name instead of surname.
SUBTITLE_ALIAS = {
    "Khabib Nurmagomedov": "khabib", "Donald Cerrone": "cowboy",
    "Mauricio Rua": "shogun", "Quinton Jackson": "rampage",
    "Antonio Silva": "bigfoot", "Cris Cyborg": "cyborg",
    "Mirko Filipovic": "cro cop", "Chan Sung Jung": "korean zombie",
}

def fighter_in_subtitle(full, sub):
    s = strip(sub)
    toks = full.split()
    # match on surname, first name, or a known nickname alias
    if strip(toks[-1]) in s or strip(toks[0]) in s:
        return True
    return strip(SUBTITLE_ALIAS.get(full, "\0")) in s


problems, notes = [], []
seen = {}
for m in MOMENTS:
    n = str(m["eventNumber"])
    tag = f"UFC {n}"
    if m["eventNumber"] in seen:
        problems.append(f"{tag}: DUPLICATE event number")
    seen[m["eventNumber"]] = True

    r = ref.get(n)
    if not r:
        notes.append(f"{tag}: not in reference (verify manually)")
    else:
        sub, year = r
        if year and year != m["year"]:
            problems.append(f"{tag}: year {m['year']} != Wikipedia {year}")
        if "vs." in (sub or ""):
            for f in (m["fighter1"], m["fighter2"]):
                if not fighter_in_subtitle(f, sub):
                    problems.append(f"{tag}: '{f}' not in subtitle '{sub}'")
        else:
            notes.append(f"{tag}: event-name subtitle '{sub}' (fighters verified manually)")

    # spoiler scan
    clue = strip(m["clue"])
    for f in (m["fighter1"], m["fighter2"]):
        s = strip(surnames(f))
        if len(s) > 3 and s in clue:
            problems.append(f"{tag}: SPOILER surname '{s}' in clue")
    if re.search(rf"\b{m['eventNumber']}\b", m["clue"]) or str(m["year"]) in m["clue"]:
        problems.append(f"{tag}: SPOILER event number or year in clue")

print(f"=== {len(MOMENTS)} moments ===")
print(f"PROBLEMS: {len(problems)}")
for p in problems:
    print("  X", p)
print(f"\nNOTES (manual-verify): {len(notes)}")
for nt in notes:
    print("  -", nt)
sys.exit(1 if problems else 0)
