---
name: ingest-raw-knowledge
description: 'Ingest raw files (pdf, pptx, docx, md, txt, ...) from raw_knowledge_files/ into the knowledge base. Use when the user asks to ingest, process, extract or absorb raw files, or to update the knowledge base from new documents. Converts files to Markdown with Microsoft MarkItDown (snapshots kept in raw_markdowns/), extracts all knowledge into KBxxxx.md files, updates index and tracker, then deletes the raw files.'
---

# Ingest Raw Knowledge

Extract ALL information from raw files in raw_knowledge_files/ and store it in knowledge_base/, following the conventions in AGENTS.md (which is binding; re-read it if in doubt).

## When to Use

- The user placed files in raw_knowledge_files/ and asks to ingest/process them.
- The user provides documents in a session and confirms they are correct knowledge.

## Procedure

1. List the files in raw_knowledge_files/ (ignore tracker.md).
2. Convert each raw file to Markdown with Microsoft MarkItDown by running the bundled script from the repository root:
   .venv\Scripts\python.exe .github\skills\ingest-raw-knowledge\scripts\convert_to_markdown.py
   This saves one Markdown snapshot per raw file in raw_markdowns/, named <original_filename>.md (e.g. manual_v2.pdf -> manual_v2.pdf.md). These snapshots are kept permanently and are never deleted, so a faithful text version of the original survives after the raw file is removed. Do not overwrite existing snapshots (the script skips them by default).
3. Read each raw file fully, using BOTH readings:
   - your own direct reading of the raw file (e.g. native pdf reading), and
   - the MarkItDown snapshot in raw_markdowns/, which is often more reliable for pptx, xlsx and complex layouts.
   If the two readings disagree, trust whichever is clearly more complete and mention the discrepancy to the user.
4. Handle visual content. Neither text reading captures images embedded inside documents (diagrams, charts, scanned pages). For every pdf, pptx, docx or xlsx file, run the image extraction script from the repository root:
   .venv\Scripts\python.exe .github\skills\ingest-raw-knowledge\scripts\extract_images.py
   This renders PDF pages as PNGs and extracts embedded media into raw_knowledge_files/_extracted_images/<original_filename>/.
   - VIEW the extracted images (they can be viewed and interpreted directly) and incorporate the knowledge they contain into the KB files, described as text.
   - For documents with many rendered pages, prioritize viewing pages where the text readings show gaps, plus the embedded*.* files.
   - The _extracted_images/ folder is a temporary working area: delete the subfolder for a raw file at the same time the raw file itself is deleted (step 9).
   - If extraction fails but the text readings are complete, proceed and tell the user that visual content may have been lost.
5. Read knowledge_base/index.md to learn which topics already have KB files.
6. For each raw file, split its content by topic:
   - If a KB file on that topic exists, ENRICH it. Do not create a duplicate.
   - Only create a new KB file (next free KBxxxx number, 4 digits, sequential) for genuinely new topics.
   - One coherent topic per file. A single raw file may feed several KB files.
7. Write or update each KB file with the exact structure required by AGENTS.md Section 4, starting new files from [the KB template](./assets/template.md):
   metadata block (ID, Title, Created, Updated, Tags), Summary, Index, Sources, Related, then the knowledge sections exactly as listed in the Index.
   - Add the raw file name to Sources.
   - Update the Updated date.
   - Cross-link related KB and LL files in Related (both directions when meaningful).
   - NEVER use Markdown tables. Plain "Key: value" lines, no YAML fences inside KB files.
   - If a file would exceed roughly 500 lines, split by subtopic.
8. Update knowledge_base/index.md: one line per file, alphabetical order, format "KBxxxx.md - brief description". Required for every new file or topic change.
9. Append one line per ingested raw file to raw_knowledge_files/tracker.md, at the bottom, never rewriting old lines:
   original_filename -> KBxxxx[, KByyyy, ...] (YYYY-MM-DD)
10. Only after the KB files, index, tracker AND the raw_markdowns/ snapshot are all written successfully, delete the raw file from raw_knowledge_files/ and its _extracted_images/<original_filename>/ subfolder if present.
11. Report to the user: which raw files were ingested, which KB files were created or enriched, and anything that could not be extracted (including visual content).

## MarkItDown Environment

- The conversion uses the Python virtual environment at .venv/ in the repository root, with the packages markitdown[all] and pymupdf installed.
- If .venv/ is missing or packages are not installed, recreate it from the repository root:
  python -m venv .venv
  .venv\Scripts\python.exe -m pip install "markitdown[all]" pymupdf
- The script [convert_to_markdown.py](./scripts/convert_to_markdown.py) accepts optional file paths to convert specific files, and --force to overwrite existing snapshots.
- The script [extract_images.py](./scripts/extract_images.py) accepts optional file paths, --dpi N (default 150) and --max-pages N (default 100). With no arguments it processes all pending pdf/pptx/docx/xlsx files.

## Failure Handling

- If a raw file cannot be read or parsed (by both MarkItDown and direct reading), do NOT delete it. Leave it in place, skip its tracker entry, and tell the user.
- If MarkItDown fails on a file but direct reading works, proceed with direct reading only and tell the user that no snapshot could be saved.
- If unsure whether content belongs to an existing topic, prefer enriching the closest existing KB file and note the decision to the user.
