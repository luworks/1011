#!/usr/bin/env python3
"""Build the required nested submission archives from an explicit allowlist."""
from __future__ import annotations
import io
import os
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TREES = ('src', 'tests', 'config', 'fixtures', 'exam', 'scripts', 'examples', 'docs')
FILES = ('README.md', 'design_memo.md', 'pyproject.toml', 'uv.lock', 'run.sh', '.env.example', 'LICENSE')
SECRET_PATTERNS = (
    re.compile(rb'sk-ant-[A-Za-z0-9_-]{20,}'),
    re.compile(rb'sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}'),
    re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
)


def credentials() -> list[bytes]:
    """Read credential values only for matching; never display them."""
    values = [v for k, v in os.environ.items() if any(x in k.upper() for x in ('API_KEY', 'TOKEN', 'SECRET'))]
    env_path = ROOT / '.env'
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if '=' not in line or line.lstrip().startswith('#'):
                continue
            key, value = line.split('=', 1)
            if any(x in key.upper() for x in ('API_KEY', 'TOKEN', 'SECRET')):
                values.append(value.strip().strip('"\''))
    return [v.encode() for v in values if len(v) >= 12]


def check(data: bytes, name: str, secrets: list[bytes], depth: int = 0) -> None:
    if any(s in data for s in secrets) or any(p.search(data) for p in SECRET_PATTERNS):
        raise SystemExit(f'Packaging refused: potential credential in {name} (value suppressed)')
    if zipfile.is_zipfile(io.BytesIO(data)):
        if depth >= 4:
            raise SystemExit(f'Packaging refused: nested archive too deep: {name}')
        with zipfile.ZipFile(io.BytesIO(data)) as nested:
            if sum(info.file_size for info in nested.infolist()) > 100_000_000:
                raise SystemExit(f'Packaging refused: nested archive too large: {name}')
            for info in nested.infolist():
                if not info.is_dir():
                    check(nested.read(info), name + '/' + info.filename, secrets, depth + 1)


def selected_files() -> list[Path]:
    paths = [ROOT / name for name in FILES]
    for tree in TREES:
        paths.extend(p for p in (ROOT / tree).rglob('*') if p.is_file())
    report = ROOT / 'report' / 'dist' / 'index.html'
    if report.is_file():
        paths.append(report)
    elif (ROOT / 'model-evaluation-report.html').is_file():
        paths.append(ROOT / 'model-evaluation-report.html')
    approved = []
    for p in sorted(set(paths)):
        rel = p.relative_to(ROOT)
        if p.is_symlink() or any(part in ('__pycache__', '.pytest_cache', '.venv', '.git') for part in rel.parts):
            continue
        if p.suffix in ('.pyc', '.pyo') or (p.name.startswith('.env') and p.name != '.env.example'):
            continue
        if not p.is_file():
            raise SystemExit(f'Required package input missing: {rel}')
        # Reject traversal through a symlinked parent as well.
        if any(parent.is_symlink() for parent in p.parents if parent != ROOT):
            raise SystemExit(f'Packaging refused: symlink parent for {rel}')
        approved.append(p)
    return approved


def main() -> None:
    examples = ROOT / 'examples'
    if examples.exists() and any(p.is_file() for p in examples.rglob('*')) and not (examples / 'manifest.json').is_file():
        raise SystemExit('Curated examples require examples/manifest.json with provenance and scope')
    secrets = credentials()
    memo = (ROOT / 'design_memo.md').read_bytes()
    check(memo, 'design_memo.md', secrets)
    inner = io.BytesIO()
    with zipfile.ZipFile(inner, 'w', zipfile.ZIP_DEFLATED) as archive:
        for p in selected_files():
            name = p.relative_to(ROOT).as_posix()
            if name == 'report/dist/index.html':
                name = 'model-evaluation-report.html'
            data = p.read_bytes()
            check(data, name, secrets)
            info = zipfile.ZipInfo(name)
            info.external_attr = (0o100755 if name == 'run.sh' else 0o100644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    target = ROOT / 'dist' / 'policy-grounded-agent-prototype.zip'
    target.parent.mkdir(exist_ok=True)
    temporary = target.with_suffix('.tmp')
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('agent_prototype.zip', inner.getvalue())
        archive.writestr('design_memo.md', memo)
    temporary.replace(target)
    print(f'Created {target.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
