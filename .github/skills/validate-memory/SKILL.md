---
name: validate-memory
description: 'Check the consistency of the memory repository: KB/LL naming, index completeness, forbidden Markdown tables, metadata blocks, required sections, file size and tracker references. Use when the user asks to validate, check, audit or verify the knowledge base or lessons learnt, and after large ingestions or restructurings.'
---

# Validate Memory

Run the consistency checker and fix what it reports, following the conventions in AGENTS.md (which is binding).

## When to Use

- The user asks to validate, check, audit or verify the repository.
- After ingesting several raw files or restructuring/splitting KB or LL files.

## Procedure

1. Run the checker from the repository root:
   .venv\Scripts\python.exe .github\skills\validate-memory\scripts\validate_memory.py
2. The script checks:
   - file naming (kb-<slug>.md / ll-<slug>.md, lowercase kebab-case),
   - index.md completeness in both folders (no missing, nonexistent or duplicate entries, alphabetical order),
   - no Markdown tables anywhere (except .github/),
   - metadata blocks (ID, Title, Created, Updated, Tags; ID matches file name; dates in YYYY-MM-DD),
   - required sections (Summary, Index, Sources, Related),
   - contradiction files in contradictions/ (cd-<slug>.md; metadata ID, Title, Created, Involves; required sections; no tables),
   - files over 500 lines (warning),
   - dead references in Related sections and tracker.md lines pointing to nonexistent kb-/ll- files (warning).
3. Fix every ERROR. Warnings are judgment calls: report them to the user with a recommendation.
4. Re-run the script until it reports 0 errors.
5. Report to the user what was found and what was fixed.

## Failure Handling

- If a fix would require inventing content (e.g. a missing Sources section whose origin is unknown), do not invent it: add the section with "unknown (validation fix YYYY-MM-DD)" and tell the user.
- If the script itself crashes, report the traceback to the user instead of editing memory files blindly.
