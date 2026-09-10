#!/usr/bin/env python3
"""find-workflow.py — 确定性查找 Workflow 候选（work-for-me route 的辅助脚本，只读）。

扫描 Global 与 Project Workflow 的 SOP（workflow.md）以及各项目 README，
按关键词大小写不敏感匹配，按命中数排序输出候选。只列候选、不做评分、不做推荐。

用法：
    find-workflow.py [--project NAME] [--json] [--root PATH] KEYWORD...
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def default_root() -> Path:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return Path(out)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return Path.cwd()


def workflow_searchable_text(path: Path) -> str:
    """抽取 SOP 中用于匹配的段落：# Workflow / 位置 / Mission / Phase 标题。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    parts = [m.group(0) for m in re.finditer(r"^# Workflow:.*$", text, re.M)]
    parts += [m.group(0) for m in re.finditer(r"^> 位置:.*$", text, re.M)]
    mission = re.search(r"^## Mission\s*\n(.*?)(?=^## )", text, re.M | re.S)
    if mission:
        parts.append(mission.group(1))
    parts += [m.group(0) for m in re.finditer(r"^## Phase .*$", text, re.M)]
    return "\n".join(parts)


def collect(root: Path):
    """(project, workflow-name, path) 三元组：Global SOP + Project SOP + 项目 README。"""
    entries = []
    global_dir = root / ".ai" / "workflows"
    if global_dir.is_dir():
        for wf in sorted(global_dir.glob("**/workflow.md")):
            entries.append(("global", wf.parent.name, wf))
    projects_dir = root / "projects"
    if projects_dir.is_dir():
        for proj in sorted(p for p in projects_dir.iterdir() if p.is_dir()):
            wf_dir = proj / "workflows"
            if wf_dir.is_dir():
                for wf in sorted(wf_dir.glob("*/workflow.md")):
                    entries.append((proj.name, wf.parent.name, wf))
            readme = proj / "README.md"
            if readme.is_file():
                entries.append((proj.name, "README", readme))
    return entries


def main() -> int:
    ap = argparse.ArgumentParser(description="确定性查找 Workflow 候选（只读）")
    ap.add_argument("keywords", nargs="+", help="关键词（大小写不敏感）")
    ap.add_argument("--project", help="只列指定项目的候选")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--root", help="workspace 根目录（默认 git rev-parse --show-toplevel）")
    args = ap.parse_args()

    root = Path(args.root) if args.root else default_root()
    keys = [k.lower() for k in args.keywords]

    results = []
    for project, name, path in collect(root):
        if args.project and project != args.project:
            continue
        if name == "README":
            text = path.read_text(encoding="utf-8", errors="replace")
        else:
            text = workflow_searchable_text(path)
        low = text.lower()
        hits = sum(low.count(k) for k in keys)
        matched = [k for k in keys if k in low]
        if hits:
            results.append({
                "workflow": name,
                "project": project,
                "path": str(path),
                "hits": hits,
                "keywords": matched,
            })
    results.sort(key=lambda r: (-r["hits"], r["path"]))

    if args.json:
        json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
    else:
        for r in results:
            print(f"{r['hits']}\t{r['project']}\t{r['workflow']}\t{r['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
