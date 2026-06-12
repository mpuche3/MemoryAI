"""Convert raw files to Markdown using Microsoft MarkItDown.

Part of the ingest-raw-knowledge skill. Converts every file in
raw_knowledge_files/ (except tracker.md) to Markdown and saves the
result in raw_markdowns/, named <original_filename>.md so provenance
is preserved (e.g. manual_v2.pdf -> manual_v2.pdf.md).

Usage (from the repository root, using the repo virtual environment):
  .venv\\Scripts\\python.exe .github\\skills\\ingest-raw-knowledge\\scripts\\convert_to_markdown.py
  .venv\\Scripts\\python.exe .github\\skills\\ingest-raw-knowledge\\scripts\\convert_to_markdown.py path\\to\\single\\file.pdf

With no arguments it converts all pending files in raw_knowledge_files/.
With file arguments it converts only those files.
Existing outputs in raw_markdowns/ are never overwritten unless --force is given.
"""

import sys
from pathlib import Path

from markitdown import MarkItDown

REPO_ROOT = Path(__file__).resolve().parents[4]
RAW_DIR = REPO_ROOT / "raw_knowledge_files"
OUT_DIR = REPO_ROOT / "raw_markdowns"
SKIP_NAMES = {"tracker.md", ".gitkeep"}


def convert(md: MarkItDown, src: Path, force: bool) -> bool:
    out_path = OUT_DIR / (src.name + ".md")
    if out_path.exists() and not force:
        print(f"SKIP (exists): {out_path.name}")
        return True
    try:
        result = md.convert(str(src))
    except Exception as exc:  # noqa: BLE001 - report and continue with other files
        print(f"FAIL: {src.name}: {exc}")
        return False
    out_path.write_text(result.text_content, encoding="utf-8")
    print(f"OK:   {src.name} -> raw_markdowns/{out_path.name}")
    return True


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv[1:]

    if args:
        targets = [Path(a).resolve() for a in args]
    else:
        targets = sorted(
            p for p in RAW_DIR.iterdir() if p.is_file() and p.name not in SKIP_NAMES
        )

    if not targets:
        print("Nothing to convert: raw_knowledge_files/ has no pending files.")
        return 0

    OUT_DIR.mkdir(exist_ok=True)
    md = MarkItDown()
    failures = sum(0 if convert(md, t, force) else 1 for t in targets)
    if failures:
        print(f"{failures} file(s) failed to convert.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
