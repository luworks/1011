"""Validate policy-pair snapshots before they enter a workflow or experiment."""
import hashlib
import json
from pathlib import Path

NAMES = ('Nimbus Wireless — Billing Dispute & Refund Policy.md',
         'NimbusCare Knowledge Base — Billing & Credits Excerpt.md')


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_snapshot(folder: Path, *, check_parent: bool = True) -> dict:
    folder = Path(folder)
    manifest = json.loads((folder / 'manifest.json').read_text())
    if manifest['version_id'] != folder.name:
        raise ValueError('Version ID does not match directory')
    actual = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
    if actual != set(manifest['files']) | {'manifest.json'}:
        raise ValueError('Unexpected or missing snapshot files')
    for relative, expected in manifest['files'].items():
        path = folder / relative
        if not path.resolve().is_relative_to(folder.resolve()) or path.is_symlink():
            raise ValueError('Invalid snapshot path')
        if sha256(path) != expected:
            raise ValueError(f'Snapshot hash mismatch: {relative}')
    lock = json.loads((folder / 'config/corpus-lock.json').read_text())
    sources = {f'exam/{name}': manifest['files'][f'exam/{name}'] for name in NAMES}
    version = hashlib.sha256(json.dumps(sources, sort_keys=True).encode()).hexdigest()
    if lock['files'] != sources or manifest['corpus_version'] != version:
        raise ValueError('Corpus lock/version does not match snapshot')
    if check_parent and manifest['parent_version_id']:
        parent_id = manifest['parent_version_id']
        if Path(parent_id).name != parent_id:
            raise ValueError('Invalid parent version ID')
        parent = folder.parent / parent_id
        verify_snapshot(parent, check_parent=False)
        if sha256(parent / 'manifest.json') != manifest['parent_manifest_sha256']:
            raise ValueError('Parent manifest changed')
    return manifest


def version_directory(version_id: str, root: Path = Path('.')) -> Path:
    if Path(version_id).name != version_id or version_id in ('.', '..'):
        raise ValueError('Policy version must be a snapshot directory name')
    folder = root / 'docs/policy_versions' / version_id
    verify_snapshot(folder)
    return folder
