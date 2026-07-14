#!/usr/bin/env python3
"""Write the curated Defining Moments to public/moments.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "moments.json")

from moments import MOMENTS

out = {"meta": {"count": len(MOMENTS), "source": "curated; verified vs Wikipedia List of UFC events"},
       "moments": MOMENTS}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(f"[moments] wrote {len(MOMENTS)} moments -> {OUT}")
