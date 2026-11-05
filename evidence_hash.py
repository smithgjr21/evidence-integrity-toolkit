#!/usr/bin/env python3
"""Inventory and hash regular files, or verify a previous JSON manifest."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()

def inventory(root):
    root = root.resolve()
    if not root.is_dir():
        raise ValueError('Source must be a directory')
    items = []
    for p in sorted(root.rglob('*')):
        if p.is_file() and not p.is_symlink():
            items.append({'path': p.relative_to(root).as_posix(), 'size_bytes': p.stat().st_size, 'sha256': sha256(p)})
    return {'generated_utc': datetime.now(timezone.utc).isoformat(), 'files': items}

def verify(root, manifest):
    expected = {x['path']: x for x in manifest['files']}
    actual = {x['path']: x for x in inventory(root)['files']}
    changes = []
    for path in sorted(expected.keys() | actual.keys()):
        if path not in actual:
            changes.append({'path': path, 'status': 'missing'})
        elif path not in expected:
            changes.append({'path': path, 'status': 'added'})
        elif expected[path]['sha256'] != actual[path]['sha256'] or expected[path]['size_bytes'] != actual[path]['size_bytes']:
            changes.append({'path': path, 'status': 'modified'})
    return changes

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    scan = subs.add_parser('scan');scan.add_argument('folder');scan.add_argument('--output',default='manifest.json')
    check = subs.add_parser('verify');check.add_argument('folder');check.add_argument('manifest')
    args = parser.parse_args()
    if args.command == 'scan':
        out = Path(args.output).resolve()
        source = Path(args.folder).resolve()
        if out == source or source in out.parents:
            parser.error('Manifest must be written outside the evidence folder')
        result=inventory(source);out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(f"Inventoried {len(result['files'])} files -> {out}")
    else:
        manifest=json.loads(Path(args.manifest).read_text(encoding='utf-8'))
        differences=verify(Path(args.folder),manifest)
        print(json.dumps({'verified':not differences,'differences':differences},indent=2))
        if differences: raise SystemExit(1)
if __name__=='__main__':main()
