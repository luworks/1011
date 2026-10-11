#!/usr/bin/env python3
"""Package an explicit committed CREAO scope; never upload or mutate source.

Default is a read-only inventory. Final package requires --package --commit SHA.
Verification extracts to an independent directory and optionally executes checks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from urllib.parse import unquote, urlsplit
import zipfile

SCOPES = ["exam", "creao-design-lab", ".github/workflows/creao-design.yml"]
REQUIRED = ["exam/design-system-guideline.md", "exam/compliance-audit.md",
            "creao-design-lab/package-lock.json", "creao-design-lab/design.md"]
EXCLUDED_PARTS = {"node_modules", ".next", ".git", "__pycache__", ".cache",
                  "profiles", "browser-profile",
                  "auth-storage", "out"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def excluded(name):
    p = PurePosixPath(name)
    return (bool(set(p.parts) & EXCLUDED_PARTS)
            or any(x.startswith(".env") for x in p.parts)
            or name.startswith(("exam/delivery/", "exam/staging/", "creao-design-lab/experiments/runs/",
                                "creao-design-lab/reports/"))
            or name.startswith(("creao-design-lab/test-results/", "creao-design-lab/playwright-report/"))
            or p.name.endswith((".tsbuildinfo", ".pyc"))
            or p.name in {"storageState.json", "auth.json", "cookies.json", ".DS_Store"})


def in_scope(name):
    return any(name == s or name.startswith(s + "/") for s in SCOPES)


def classify(name):
    return "evidence" if name.startswith(("exam/research/", "creao-design-lab/experiments/results/")) else "candidate"


def inventory(root):
    tracked = git(root, "ls-files", "-z", "--", *SCOPES).decode().split("\0")
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "-z", "--", *SCOPES).decode().split("\0")
    return {"head": git(root, "rev-parse", "HEAD").decode().strip(),
            "trackedIncluded": sorted(n for n in tracked if n and not excluded(n)),
            "trackedExcluded": sorted(n for n in tracked if n and excluded(n)),
            "untrackedNotPackaged": sorted(n for n in untracked if n and not excluded(n)),
            "note": "Read-only inventory. Untracked or modified files must be committed before packaging."}


def markdown_links(root):
    """Check actual inline/reference Markdown links, not examples or bare paths."""
    broken, checked = [], 0
    for file in sorted(root.rglob("*.md")):
        if "node_modules" in file.parts or ".next" in file.parts:
            continue
        text = file.read_text(errors="replace")
        text = re.sub(r"(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1\s*$", "", text)
        text = re.sub(r"`[^`\n]*`", "", text)
        # Non-nested Markdown destinations and reference definitions.
        targets = re.findall(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+['\"][^\n]*?['\"])?\s*\)", text)
        targets += re.findall(r"(?m)^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)", text)
        for raw in targets:
            target = raw.strip("<>")
            if not target or target.startswith("#") or urlsplit(target).scheme or target.startswith("//"):
                continue
            path = unquote(urlsplit(target).path)
            if not path:
                continue
            checked += 1
            resolved = (file.parent / path).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                broken.append({"file": file.relative_to(root).as_posix(), "target": target})
    return {"checked": checked, "broken": broken}


def readme(commit):
    return f"""# CREAO 设计规范：源码与证据交付包

来源提交：`{commit}`。此包只在本地生成，未上传；不证明远端 CI、部署或每日巡查已启用。

## 阅读顺序

1. **正式交付**：[设计规范](exam/design-system-guideline.md)、[合规审计](exam/compliance-audit.md)。
2. **题面与探索**：[原题](exam/task.md)、[中文题面](exam/task.zh-CN.md)、[研究发现](exam/research-findings.zh-CN.md)。
3. **实施过程**：[计划](exam/implementation-plan.zh-CN.md)、[验收结果](exam/validation-results.zh-CN.md)、[工程师实验](exam/engineer-experiment-review.zh-CN.md)。
4. **可运行实现**：[项目 README](creao-design-lab/README.md)、[设计契约](creao-design-lab/design.md)、[Agent 约束](creao-design-lab/AGENTS.md)。
5. **持续治理**：[巡查职责](exam/agents/design-drift-auditor.md)、[打包边界](exam/delivery-packaging-plan.zh-CN.md)。

`exam/research/` 保留原站研究、首轮失败和漏检、复验与合成原型证据；历史收据中的绝对路径仅作来源说明。原站与合成数据不可混为一谈。原站截图仅保留本地，外发前需审阅。

## 复现

使用 Node 24，在 `creao-design-lab/` 执行 `npm ci`、`npm run typecheck`、`npm run lint`、`npm run test:design`、`npm run check:design`、`npm run build`。浏览器安装、环境选择和视觉基线要求见项目 README；不同平台的截图不可替代已审阅基线。

`candidate-manifest.json` 标识本次源码和文档；`evidence-manifest.json` 标识历史及最终运行证据。历史 mutation 不在打包时重复运行，也不能自动视为覆盖最终源码；须核对其源码摘要及验证文档。包级摘要与独立解压验收结果在压缩包外的收据中，避免递归哈希。
"""


def package(root, commit, output):
    resolved = git(root, "rev-parse", commit + "^{commit}").decode().strip()
    head = git(root, "rev-parse", "HEAD").decode().strip()
    if resolved != head:
        raise ValueError("Package only current frozen HEAD; requested commit differs.")
    dirty = git(root, "status", "--porcelain", "--untracked-files=all", "--", *SCOPES).decode()
    if dirty.strip():
        raise ValueError("Scoped worktree/index is not clean; commit owner must freeze it first.\n" + dirty)
    files, rejected = {}, []
    for record in git(root, "ls-tree", "-rz", "--full-tree", resolved, "--", *SCOPES).split(b"\0"):
        if not record:
            continue
        meta, raw_name = record.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        name = raw_name.decode()
        if excluded(name):
            rejected.append(name)
            continue
        if mode not in {"100644", "100755"} or kind != "blob":
            raise ValueError(f"Symlink/submodule/non-regular asset cannot be packaged: {name}")
        files[name] = git(root, "cat-file", "blob", oid)
    for name in REQUIRED:
        if name not in files:
            raise ValueError("Missing required committed asset: " + name)
    files["README.md"] = readme(resolved).encode()
    stamp = datetime.now(timezone.utc).isoformat()
    for category in ("candidate", "evidence"):
        entries = [{"path": name, "size": len(data), "sha256": sha(data)}
                   for name, data in sorted(files.items()) if classify(name) == category]
        manifest = {"schemaVersion": 1, "kind": category, "sourceCommit": resolved,
                    "createdAt": stamp, "files": entries, "excludedTracked": rejected,
                    "claims": {"remoteCIExecuted": False, "deployed": False, "uploaded": False}}
        files[category + "-manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
    output.mkdir(parents=True, exist_ok=True)
    dest = output / f"creao-design-{resolved[:12]}.zip"
    if dest.exists():
        raise ValueError(f"Refusing to overwrite immutable package: {dest}")
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 11, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, data)
    receipt = {"sourceCommit": resolved, "archive": dest.name, "size": dest.stat().st_size,
               "sha256": sha(dest.read_bytes()), "fileCount": len(files), "createdAt": stamp,
               "manifestDigests": {n: sha(files[n]) for n in ("candidate-manifest.json", "evidence-manifest.json")},
               "verification": "notRun", "uploaded": False}
    dest.with_suffix(".receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


def verify(archive_path, run_checks, browser_args):
    # Always use a fresh extraction; never follow symlinks or reuse the source checkout.
    target = Path(tempfile.mkdtemp(prefix="creao-delivery-verify-"))
    result = {"archive": str(archive_path), "archiveSha256": sha(archive_path.read_bytes()),
              "extractedTo": str(target), "checks": [], "mutationRerun": False,
              "visualEnvironment": "Caller must select the documented reviewed environment; no snapshot updates."}
    with zipfile.ZipFile(archive_path) as archive:
        for info in archive.infolist():
            p = PurePosixPath(info.filename)
            if p.is_absolute() or ".." in p.parts or "\\" in info.filename or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Unsafe archive member: " + info.filename)
        archive.extractall(target)
    expected = {"candidate-manifest.json", "evidence-manifest.json"}
    for category in ("candidate", "evidence"):
        manifest = json.loads((target / (category + "-manifest.json")).read_text())
        for item in manifest["files"]:
            name = item["path"]
            p = (target / name).resolve()
            if not p.is_relative_to(target) or not p.is_file():
                raise ValueError("Missing or unsafe manifest path: " + name)
            data = p.read_bytes()
            if len(data) != item["size"] or sha(data) != item["sha256"]:
                raise ValueError("Manifest mismatch: " + name)
            expected.add(name)
    actual = {p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file()}
    if expected != actual:
        raise ValueError("Archive contains unmanifested or missing files: " + str(expected ^ actual))
    result["links"] = markdown_links(target)
    commands = [["npm", "ci"], ["npm", "run", "typecheck"], ["npm", "run", "lint"],
                ["npm", "run", "test:design"], ["npm", "run", "check:design"], ["npm", "run", "build"]]
    if browser_args:
        if "--update-snapshots" in " ".join(browser_args) or "-u" in browser_args:
            raise ValueError("Verification cannot update screenshot baselines.")
        commands.append(["npx", "playwright", "test", *browser_args])
    if run_checks and not result["links"]["broken"]:
        # No inherited production secrets are passed to package lifecycle scripts.
        env = {k: v for k, v in os.environ.items() if k in {"PATH", "HOME", "TMPDIR", "LANG", "LC_ALL",
               "PW_CHANNEL", "PW_SERVER_COMMAND", "BASE_URL", "VISUAL_BASELINE_ENV", "PLAYWRIGHT_BROWSERS_PATH"}}
        env["NEXT_TELEMETRY_DISABLED"] = "1"
        for index, command in enumerate(commands):
            log = target / f"verification-{index + 1}.log"
            started = datetime.now(timezone.utc).isoformat()
            with log.open("w") as handle:
                try:
                    proc = subprocess.run(command, cwd=target / "creao-design-lab", env=env,
                                          stdout=handle, stderr=subprocess.STDOUT, timeout=600)
                    code = proc.returncode
                except subprocess.TimeoutExpired:
                    code = 124
            result["checks"].append({"command": command, "exitCode": code, "startedAt": started, "log": str(log)})
            if code:
                break
    result["status"] = "failed" if result["links"]["broken"] or any(c["exitCode"] for c in result["checks"]) else ("passed" if run_checks else "integrityOnly")
    result["browserChecksRequested"] = bool(browser_args)
    result["checksRequested"] = run_checks
    receipt = archive_path.with_name(archive_path.stem + ".verification-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + ".json")
    receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--dry-run", action="store_true", help="Read-only inventory (default)")
    parser.add_argument("--package", action="store_true")
    parser.add_argument("--commit", help="Explicit frozen HEAD commit required for packaging")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path, metavar="ZIP")
    parser.add_argument("--run-checks", action="store_true", help="Execute npm install, types, lint, unit, static, build in extracted directory")
    parser.add_argument("--browser-args", nargs=argparse.REMAINDER, help="Playwright selected specs/project arguments; pass last")
    args = parser.parse_args()
    if args.package and args.verify:
        parser.error("Package and verify are separate operations.")
    if args.package:
        if not args.commit:
            parser.error("--package requires --commit SHA")
        result = package(args.root, args.commit, args.output or args.root / "exam/delivery")
    elif args.verify:
        result = verify(args.verify.resolve(), args.run_checks, args.browser_args)
    else:
        result = inventory(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result.get("status") == "failed" else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, subprocess.CalledProcessError, OSError) as error:
        print(json.dumps({"status": "error", "message": str(error)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
