#!/usr/bin/env python3
"""Advance the quote rotation by one volume.

Reads rotation.json, writes manifest.json pointing at the next volume, then
advances the index (wrapping 0..5) and bumps the release counter so every
rotation carries a unique version string (the firmware treats any version !=
the installed one as an update). All six volumes are already uploaded to R2
and CDN-verified, so this is a pure metadata flip — no upload, no signing.

Run by .github/workflows/rotate-quotes.yml on a schedule, or manually:
    python3 rotate_quotes.py && git add manifest.json rotation.json && git commit && git push
"""
import json, datetime, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(HERE, "rotation.json")))
i = cfg["index"] % len(cfg["volumes"])
rel = cfg["release"]
v = cfg["volumes"][i]

manifest = {
    "version": f"r{rel}-vol{v['vol']}",
    "released": datetime.date.today().isoformat() if len(sys.argv) < 2 else sys.argv[1],
    "sha256": v["sha256"],
    "size": v["size"],
    "url": v["url"],
    "notes": f"Rotating corpus, Volume {v['vol']} of {len(cfg['volumes'])} "
             f"(release {rel}). Clean-room public-domain, all 1440 minutes covered.",
}
json.dump(manifest, open(os.path.join(HERE, "manifest.json"), "w"), indent=2)
open(os.path.join(HERE, "manifest.json"), "a").write("\n")

cfg["index"] = (i + 1) % len(cfg["volumes"])
cfg["release"] = rel + 1
json.dump(cfg, open(os.path.join(HERE, "rotation.json"), "w"), indent=2)

print(f"published {manifest['version']} -> {v['file']}")
print(f"next rotation will publish vol{cfg['volumes'][cfg['index']]['vol']} as release {cfg['release']}")
