"""Consistency checker for the MemoryAI repository.

Part of the validate-memory skill. Verifies that the memory files follow
the conventions defined in AGENTS.md:

1. File naming: knowledge_base/ contains only KB followed by exactly 4
   digits (.md) plus index.md; lessons_learnt/ the same with LL.
2. Index completeness: every KB/LL file has exactly one line in its
   folder's index.md, and the index lists no nonexistent files.
3. No Markdown tables anywhere (lines starting with |), in any .md file
   of the repository except under .github/ (SKILL.md files may need them).
4. Metadata block: every KB/LL file starts with ID, Title, Created,
   Updated and Tags lines, and the ID matches the file name.
5. Required sections: every KB/LL file has Summary, Index, Sources and
   Related sections.
6. Size: warns when a KB/LL file exceeds 500 lines.
7. Tracker: raw_knowledge_files/tracker.md entries reference existing KB
   files.
8. Contradictions: files in contradictions/ are named CD + 4 digits, have
   ID/Title/Created/Involves metadata and the required sections.

Usage (from the repository root):
  .venv\\Scripts\\python.exe .github\\skills\\validate-memory\\scripts\\validate_memory.py

Exit code 0 if no errors (warnings allowed), 1 otherwise.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
ERRORS: list[str] = []
WARNINGS: list[str] = []


def error(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def check_folder(folder_name: str, prefix: str) -> None:
    folder = REPO_ROOT / folder_name
    pattern = re.compile(rf"^{prefix}\d{{4}}\.md$")

    files = {p.name for p in folder.glob("*.md")} - {"index.md"}
    for name in sorted(files):
        if not pattern.match(name):
            error(f"{folder_name}/{name}: bad file name (expected {prefix} + 4 digits + .md)")

    index_path = folder / "index.md"
    if not index_path.exists():
        error(f"{folder_name}/index.md is missing")
        return
    index_text = index_path.read_text(encoding="utf-8")
    listed = re.findall(rf"^({prefix}\d{{4}}\.md)\s*-", index_text, flags=re.MULTILINE)

    for name in sorted(files - set(listed)):
        error(f"{folder_name}/index.md: missing entry for {name}")
    for name in sorted(set(listed) - files):
        error(f"{folder_name}/index.md: lists nonexistent file {name}")
    dupes = {n for n in listed if listed.count(n) > 1}
    for name in sorted(dupes):
        error(f"{folder_name}/index.md: duplicate entry for {name}")
    if listed != sorted(listed):
        warn(f"{folder_name}/index.md: entries are not in alphabetical order")

    for name in sorted(files):
        if pattern.match(name):
            check_memory_file(folder / name, prefix)


def check_memory_file(path: Path, prefix: str) -> None:
    rel = f"{path.parent.name}/{path.name}"
    lines = path.read_text(encoding="utf-8").splitlines()
    text = "\n".join(lines)

    # Metadata block.
    meta = {}
    for line in lines[:12]:
        m = re.match(r"^(ID|Title|Created|Updated|Tags):\s*(.*)$", line)
        if m:
            meta[m.group(1)] = m.group(2).strip()
    for key in ("ID", "Title", "Created", "Updated", "Tags"):
        if key not in meta:
            error(f"{rel}: missing metadata line '{key}:'")
    if "ID" in meta and meta["ID"] != path.stem:
        error(f"{rel}: metadata ID '{meta['ID']}' does not match file name")
    for key in ("Created", "Updated"):
        if key in meta and not re.match(r"^\d{4}-\d{2}-\d{2}$", meta[key]):
            error(f"{rel}: {key} is not in YYYY-MM-DD format")

    # Required sections.
    for section in ("Summary", "Index", "Sources", "Related"):
        if not re.search(rf"^#+\s*{section}\b", text, flags=re.MULTILINE):
            error(f"{rel}: missing section '{section}'")

    if len(lines) > 500:
        warn(f"{rel}: {len(lines)} lines (soft limit is 500; consider splitting)")


def check_no_tables() -> None:
    for path in REPO_ROOT.rglob("*.md"):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel.startswith((".github/", ".venv/")):
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("|"):
                error(f"{rel}:{i}: Markdown table detected (tables are forbidden)")


def check_tracker() -> None:
    tracker = REPO_ROOT / "raw_knowledge_files" / "tracker.md"
    if not tracker.exists():
        error("raw_knowledge_files/tracker.md is missing")
        return
    kb_files = {p.name for p in (REPO_ROOT / "knowledge_base").glob("KB*.md")}
    for i, line in enumerate(tracker.read_text(encoding="utf-8").splitlines(), 1):
        if "->" not in line:
            continue
        for kb in re.findall(r"KB\d{4}", line):
            if f"{kb}.md" not in kb_files:
                error(f"raw_knowledge_files/tracker.md:{i}: references nonexistent {kb}.md")


def check_contradictions() -> None:
    folder = REPO_ROOT / "contradictions"
    if not folder.exists():
        return
    pattern = re.compile(r"^CD\d{4}\.md$")
    known = {p.name for p in (REPO_ROOT / "knowledge_base").glob("KB*.md")}
    known |= {p.name for p in (REPO_ROOT / "lessons_learnt").glob("LL*.md")}
    for path in sorted(folder.glob("*.md")):
        if path.name == "README.md":
            continue
        rel = f"contradictions/{path.name}"
        if not pattern.match(path.name):
            error(f"{rel}: bad file name (expected CD + 4 digits + .md)")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        text = "\n".join(lines)
        meta = {}
        for line in lines[:12]:
            m = re.match(r"^(ID|Title|Created|Involves):\s*(.*)$", line)
            if m:
                meta[m.group(1)] = m.group(2).strip()
        for key in ("ID", "Title", "Created", "Involves"):
            if key not in meta:
                error(f"{rel}: missing metadata line '{key}:'")
        if "ID" in meta and meta["ID"] != path.stem:
            error(f"{rel}: metadata ID '{meta['ID']}' does not match file name")
        if "Created" in meta and not re.match(r"^\d{4}-\d{2}-\d{2}$", meta["Created"]):
            error(f"{rel}: Created is not in YYYY-MM-DD format")
        for section in ("Summary", "Conflicting Claims", "Analysis", "Suggested Resolutions"):
            if not re.search(rf"^#+\s*{re.escape(section)}\b", text, flags=re.MULTILINE):
                error(f"{rel}: missing section '{section}'")
        for ref in re.findall(r"(?:KB|LL)\d{4}", meta.get("Involves", "")):
            if f"{ref}.md" not in known:
                warn(f"{rel}: Involves references nonexistent {ref}.md")


def main() -> int:
    check_folder("knowledge_base", "KB")
    check_folder("lessons_learnt", "LL")
    check_no_tables()
    check_tracker()
    check_contradictions()

    for msg in WARNINGS:
        print(f"WARN:  {msg}")
    for msg in ERRORS:
        print(f"ERROR: {msg}")
    print(f"Done: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s).")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    raise SystemExit(main())
