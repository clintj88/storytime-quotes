# storytime-quotes

Public quote data for [Storytime Clock](https://github.com/clintj88/Storytime) devices.

Storytime Clock devices poll this repo daily for updated quotes. When a new version is published here, all internet-connected devices download it automatically.

## What's in here

- **`quotes.txt`** — the quote database (pipe-delimited: `HH:MM|quote|author|book`).
- **`manifest.json`** — version metadata. Devices fetch this first; if `version` is newer than what's installed, they download `quotes.txt`.

## Manifest format

```json
{
  "version": "20260528",
  "released": "2026-05-28",
  "sha256": "5630fef4...",
  "size": 1652679,
  "url": "https://raw.githubusercontent.com/clintj88/storytime-quotes/main/quotes.txt",
  "notes": "Optional release notes for humans"
}
```

- **`version`** (required) — string used for change detection. Just-greater-than comparison; date-string `YYYYMMDD` is the convention.
- **`sha256`** (required) — hex SHA-256 of `quotes.txt`. Devices verify before committing.
- **`size`** (required) — bytes. Devices skip the download if it won't fit their LittleFS partition.
- **`url`** (optional) — full URL to `quotes.txt`. Lets us serve from a CDN later without firmware change.
- **`notes`** (optional) — human-readable; ignored by firmware.

## Publishing a new release

```bash
cd ~/storytime-quotes
# Replace quotes.txt
cp ~/storytime/quotes.txt .
# Recompute sha + size
SHA=$(sha256sum quotes.txt | awk '{print $1}')
SIZE=$(stat -c '%s' quotes.txt)
# Edit manifest.json — bump version (date), update sha256 + size + notes
$EDITOR manifest.json
git commit -am "Refresh quotes $(date +%Y%m%d)"
git push
# Devices auto-update within 24 hours, or customers can hit "Check Now" in the web UI.
```

## License

These quotes are excerpted under fair use for the educational/aesthetic purpose of a literary clock. If you are an author or rights holder and want a passage removed, open an issue here.
