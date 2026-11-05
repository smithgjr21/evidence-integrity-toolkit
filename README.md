# Digital Forensics Portfolio Project

> Educational demonstration using **synthetic evidence only**. No real person's data is included. Results require analyst validation and should not be treated as proof of wrongdoing.

## Skills demonstrated
SHA-256 verification, immutable-source workflow, manifest comparison, JSON reports, Python testing.

## Run (Python 3.9+; standard library only)
```bash
python evidence_hash.py scan sample_evidence --output manifest.json
python evidence_hash.py verify sample_evidence manifest.json
python -m unittest discover -s tests -v
```

## Evidence handling
All example files are fictional. Preserve originals, verify hashes, document timestamps/time zones, and maintain a chain of custody before using any process in a real investigation.

## Limitations
File hashes demonstrate byte-level equality, **not** authenticity, acquisition quality, or a complete chain of custody. Symlinks are intentionally skipped.

## Suggested next steps
Add screenshots from your own run, a sample investigator report, and a brief explanation of what you learned. Only list forensic tools you have personally operated.
