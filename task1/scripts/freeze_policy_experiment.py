#!/usr/bin/env python3
"""Freeze reproducible inputs without copying credentials or other run outputs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
TREES = ('src', 'config', 'fixtures', 'exam', 'tests', 'scripts', 'docs/policy_versions')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files():
    return sorted(p for tree in TREES for p in (ROOT/tree).rglob('*')
                  if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts
                  and p.suffix not in ('.pyc','.pyo') and not p.name.startswith('.env'))


def verify(folder):
    manifest=json.loads((folder/'frozen-inputs.json').read_text())
    for relative,expected in manifest['files'].items():
        path=folder/relative
        if not path.resolve().is_relative_to(folder.resolve()) or digest(path)!=expected:
            raise ValueError(f'Frozen input changed: {relative}')
    actual={p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
    if actual!=set(manifest['files'])|{'frozen-inputs.json'}:
        raise ValueError('Unexpected frozen input file')
    print('Verified',folder)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--verify',type=Path)
    args=parser.parse_args()
    if args.verify:
        verify(args.verify);return
    target=args.output or ROOT/'runs'/('policy-inputs-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    target.mkdir(parents=True,exist_ok=False)
    paths=files()+[ROOT/name for name in ('pyproject.toml','README.md','run.sh','uv.lock','LICENSE','.env.example','design_memo.md') if (ROOT/name).is_file()]
    before={p.relative_to(ROOT).as_posix():digest(p) for p in paths}
    for p in paths:
        dest=target/p.relative_to(ROOT)
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(p,dest)
    after={p.relative_to(ROOT).as_posix():digest(p) for p in paths}
    if before!=after:
        raise ValueError('Source changed while freezing; preserve this incomplete copy and create a fresh one')
    manifest={'created_at_utc':datetime.now(timezone.utc).isoformat(),'files':before,
              'content_sha256':hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),
              'credential_policy':'No .env or run artifacts copied. Use inherited environment for live calls.'}
    (target/'frozen-inputs.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    verify(target)


if __name__=='__main__':
    main()
