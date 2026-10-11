#!/usr/bin/env python3
"""Create new policy-pair snapshots and verify existing snapshots; no model calls."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = ROOT / 'docs/policy_versions'
NAMES = ('Nimbus Wireless — Billing Dispute & Refund Policy.md',
         'NimbusCare Knowledge Base — Billing & Credits Excerpt.md')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def verify(folder: Path) -> dict:
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    if manifest['version_id'] != folder.name:
        raise ValueError('Version ID does not match directory')
    expected_paths = set(manifest['files']) | {'manifest.json'}
    actual_paths = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
    if actual_paths != expected_paths:
        raise ValueError(f'Unexpected or missing files: {actual_paths ^ expected_paths}')
    for relative, expected in manifest['files'].items():
        path = folder / relative
        if path.resolve().is_relative_to(folder.resolve()) is False or path.is_symlink():
            raise ValueError(f'Invalid snapshot path: {relative}')
        if digest(path) != expected:
            raise ValueError(f'Snapshot hash mismatch: {relative}')
    lock = json.loads((folder / 'config/corpus-lock.json').read_text(encoding='utf-8'))
    expected_sources = {f'exam/{name}': manifest['files'][f'exam/{name}'] for name in NAMES}
    if lock['files'] != expected_sources:
        raise ValueError('Corpus lock does not match policy pair')
    corpus_version = hashlib.sha256(json.dumps(lock['files'], sort_keys=True).encode()).hexdigest()
    if corpus_version != manifest['corpus_version']:
        raise ValueError('Corpus version mismatch')
    return manifest


def snapshot(args: argparse.Namespace) -> Path:
    if not re.fullmatch(r'[a-z][a-z0-9-]*', args.label):
        raise ValueError('Label must be lowercase letters, digits, and hyphens')
    parent = None
    if args.parent:
        if Path(args.parent).name != args.parent:
            raise ValueError('Parent must be a version directory name')
        parent = verify(VERSIONS / args.parent)
    if args.status != 'original' and (parent is None or not args.changes or not args.decisions):
        raise ValueError('Non-original snapshots require parent, changes, and decisions')
    now = datetime.now(timezone.utc)
    version_id = now.strftime('%Y%m%dT%H%M%S%fZ') + '-' + args.label
    VERSIONS.mkdir(parents=True, exist_ok=True)
    target = VERSIONS / version_id
    if target.exists():
        raise ValueError('Snapshot already exists; never overwrite a version')
    with tempfile.TemporaryDirectory(prefix='.snapshot-', dir=VERSIONS) as temporary:
        stage = Path(temporary)
        (stage / 'exam').mkdir()
        (stage / 'config').mkdir()
        for name in NAMES:
            shutil.copyfile(args.source_dir / name, stage / 'exam' / name)
        for source, name in ((args.changes, 'CHANGES.md'), (args.decisions, 'OPEN_DECISIONS.md')):
            if source:
                shutil.copyfile(source, stage / name)
        sources = {f'exam/{name}': digest(stage / 'exam' / name) for name in NAMES}
        write_json(stage / 'config/corpus-lock.json', {'files': sources})
        manifest = {
            'schema_version': 1, 'version_id': version_id,
            'created_at_utc': now.isoformat(), 'status': args.status,
            'parent_version_id': parent['version_id'] if parent else None,
            'parent_manifest_sha256': digest(VERSIONS / args.parent / 'manifest.json') if parent else None,
            'corpus_version': hashlib.sha256(json.dumps(sources, sort_keys=True).encode()).hexdigest(),
            'files': {p.relative_to(stage).as_posix(): digest(p)
                      for p in sorted(stage.rglob('*')) if p.is_file()},
        }
        write_json(stage / 'manifest.json', manifest)
        stage.rename(target)
    verify(target)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    create = commands.add_parser('snapshot')
    create.add_argument('--source-dir', type=Path, required=True)
    create.add_argument('--label', required=True)
    create.add_argument('--status', choices=('original', 'editorial-draft', 'experiment'), required=True)
    create.add_argument('--parent')
    create.add_argument('--changes', type=Path)
    create.add_argument('--decisions', type=Path)
    check = commands.add_parser('verify')
    check.add_argument('version_id', nargs='?')
    args = parser.parse_args()
    if args.command == 'snapshot':
        print(snapshot(args).relative_to(ROOT))
    else:
        if args.version_id and Path(args.version_id).name != args.version_id:
            raise ValueError('Version must be a directory name')
        folders = [VERSIONS / args.version_id] if args.version_id else sorted(
            p for p in VERSIONS.iterdir() if p.is_dir() and not p.name.startswith('.'))
        for folder in folders:
            manifest = verify(folder)
            if manifest['parent_version_id']:
                parent = VERSIONS / manifest['parent_version_id']
                verify(parent)
                if digest(parent / 'manifest.json') != manifest['parent_manifest_sha256']:
                    raise ValueError('Parent manifest changed')
            print(f"OK {folder.name} corpus={manifest['corpus_version']}")


if __name__ == '__main__':
    main()
