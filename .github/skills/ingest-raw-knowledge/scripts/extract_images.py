"""Extract visual content from raw files so the agent can view it directly.

Part of the ingest-raw-knowledge skill. For image-heavy documents, text
extraction (direct reading or MarkItDown) loses diagrams, charts and
scanned pages. This script makes that content visible:

- PDF  : renders every page as a PNG (captures images, vector charts and
         layout) and also extracts embedded raster images.
- PPTX / DOCX / XLSX : extracts all embedded media files (they are zip
         archives with a media folder inside).

Output goes to raw_knowledge_files/_extracted_images/<original_filename>/.
This folder is a temporary working area: review the images during
ingestion, then delete the subfolder together with the raw file.

Usage (from the repository root, using the repo virtual environment):
  .venv\\Scripts\\python.exe .github\\skills\\ingest-raw-knowledge\\scripts\\extract_images.py
  .venv\\Scripts\\python.exe .github\\skills\\ingest-raw-knowledge\\scripts\\extract_images.py file.pdf --dpi 200 --max-pages 30

With no arguments it processes all pdf/pptx/docx/xlsx files pending in
raw_knowledge_files/. Options:
  --dpi N        render resolution for PDF pages (default 150)
  --max-pages N  cap on rendered PDF pages per file (default 100)
"""

import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
RAW_DIR = REPO_ROOT / "raw_knowledge_files"
OUT_ROOT = RAW_DIR / "_extracted_images"
SUPPORTED = {".pdf", ".pptx", ".docx", ".xlsx"}
MEDIA_PREFIXES = ("ppt/media/", "word/media/", "xl/media/")


def extract_pdf(src: Path, out_dir: Path, dpi: int, max_pages: int) -> int:
    import fitz  # PyMuPDF

    count = 0
    with fitz.open(src) as doc:
        n_pages = min(len(doc), max_pages)
        if len(doc) > max_pages:
            print(f"NOTE: {src.name} has {len(doc)} pages; rendering first {max_pages} only (use --max-pages to raise).")
        for i in range(n_pages):
            page = doc[i]
            pix = page.get_pixmap(dpi=dpi)
            pix.save(out_dir / f"page{i + 1:04d}.png")
            count += 1
        # Embedded raster images (may duplicate page content, but lossless).
        seen_xrefs = set()
        for i in range(len(doc)):
            for img in doc[i].get_images(full=True):
                xref = img[0]
                if xref in seen_xrefs:
                    continue
                seen_xrefs.add(xref)
                try:
                    info = doc.extract_image(xref)
                except Exception:
                    continue
                if len(info["image"]) < 2048:  # skip tiny decorations
                    continue
                name = f"embedded{len(seen_xrefs):04d}.{info['ext']}"
                (out_dir / name).write_bytes(info["image"])
                count += 1
    return count


def extract_office(src: Path, out_dir: Path) -> int:
    count = 0
    with zipfile.ZipFile(src) as zf:
        for name in zf.namelist():
            if name.startswith(MEDIA_PREFIXES) and not name.endswith("/"):
                data = zf.read(name)
                if len(data) < 2048:  # skip tiny decorations
                    continue
                (out_dir / Path(name).name).write_bytes(data)
                count += 1
    return count


def process(src: Path, dpi: int, max_pages: int) -> bool:
    out_dir = OUT_ROOT / src.name
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        if src.suffix.lower() == ".pdf":
            count = extract_pdf(src, out_dir, dpi, max_pages)
        else:
            count = extract_office(src, out_dir)
    except Exception as exc:  # noqa: BLE001 - report and continue with other files
        print(f"FAIL: {src.name}: {exc}")
        return False
    print(f"OK:   {src.name} -> {count} image(s) in raw_knowledge_files/_extracted_images/{src.name}/")
    return True


def get_opt(args: list[str], name: str, default: int) -> int:
    if name in args:
        i = args.index(name)
        value = int(args[i + 1])
        del args[i:i + 2]
        return value
    return default


def main() -> int:
    args = sys.argv[1:]
    dpi = get_opt(args, "--dpi", 150)
    max_pages = get_opt(args, "--max-pages", 100)

    if args:
        targets = [Path(a).resolve() for a in args]
    else:
        targets = sorted(
            p for p in RAW_DIR.iterdir()
            if p.is_file() and p.suffix.lower() in SUPPORTED
        )

    if not targets:
        print("Nothing to process: no pdf/pptx/docx/xlsx files pending in raw_knowledge_files/.")
        return 0

    failures = sum(0 if process(t, dpi, max_pages) else 1 for t in targets)
    if failures:
        print(f"{failures} file(s) failed.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
