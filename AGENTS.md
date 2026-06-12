# Agent Operating Policy

This file defines the mandatory behavior and conventions for any AI assistant (GitHub Copilot or other) working with this repository.
Read this file in full before doing anything else. Every rule here is binding.

## 1. Purpose of This Repository

This repository is the persistent memory of an AI agent. It stores two kinds of memory:

- knowledge_base/ : knowledge extracted from documents (manuals, papers, presentations, notes, ...).
- lessons_learnt/ : lessons gained from experience during sessions with the user (errors made, solutions found, constraints discovered).

All memory files are plain Markdown (.md) or text (.txt). This keeps the repository small while holding a large amount of information.

## 2. Repository Structure

- AGENTS.md            : this file. The contract for all agent sessions.
- README.md            : human-facing description of the repository.
- knowledge_base/      : knowledge files KB0000.md, KB0001.md, ... plus index.md.
- lessons_learnt/      : lesson files LL0000.md, LL0001.md, ... plus index.md.
- raw_knowledge_files/ : inbox for raw files (pdf, pptx, docx, md, txt, ...) waiting to be ingested. Contains tracker.md.
- raw_markdowns/       : permanent Markdown snapshots of ingested raw files, produced by MarkItDown during ingestion. Named <original_filename>.md. Never deleted.
- .github/skills/      : skills (step-by-step procedures) available to the agent, one folder per skill with a SKILL.md inside.
- requirements.txt     : Python dependencies for the ingestion tooling.
- .venv/               : Python virtual environment with markitdown[all] and pymupdf installed, used by the ingestion skill. Not committed to git.

## 3. Global Formatting Rules

1. NEVER use Markdown tables in any file in this repository. No exceptions. Files must read nicely as raw text without rendering.
2. Use plain "Key: value" lines for metadata. No YAML front matter fences. The only exception is SKILL.md files under .github/skills/, which require YAML front matter for VS Code to discover them.
3. Keep lines reasonably short and prose simple, so raw reading is comfortable.
4. File names: KB followed by exactly 4 digits for knowledge files (KB0000.md), LL followed by exactly 4 digits for lesson files (LL0000.md). Numbers are sequential, never reused, never renumbered.
5. Date-stamp volatile facts. Knowledge that changes over time (versions, prices, APIs, settings, people in roles) must be phrased with its reference date, e.g. "As of 2026-06, the latest version is 1.27". Stable facts need no date.

## 4. Knowledge Base File Structure (KBxxxx.md)

Every knowledge file follows this exact section order:

1. Metadata block at the very top, as plain lines:
   ID: KBxxxx
   Title: short descriptive title
   Created: YYYY-MM-DD
   Updated: YYYY-MM-DD
   Tags: comma-separated lowercase tags
2. Summary: a short paragraph describing what knowledge this file holds.
3. Index: a table of contents listing the knowledge sections of the file, one line per section.
4. Sources: one line per source. Typically raw files that were ingested (and may already be deleted), or "Session with user YYYY-MM-DD".
5. Related: one line per related file (KB or LL), with the file name and a few words on why it is related. KB files may reference LL files and vice versa.
6. The actual knowledge content, organized in sections exactly as listed in the Index.

## 5. Lessons Learnt File Structure (LLxxxx.md)

Identical structure to KB files (metadata, summary, index, sources, related, content).
The difference is the origin: lessons come from experience during sessions, not from documents.
A lesson should capture: the context, what was attempted, what went wrong or what was discovered, the root cause if known, and the rule to follow in the future.
Sources for lessons are usually "Session with user YYYY-MM-DD".

## 6. Index Files (knowledge_base/index.md and lessons_learnt/index.md)

Each index file starts with a short paragraph explaining itself, then lists every file in the folder:

- One line per file, in alphabetical order (which equals numerical order given the naming scheme).
- Format of each line: KBxxxx.md - brief one-line description of the file's topic and contents.
- Every KB/LL file in the folder MUST appear in the index. The index must never list files that do not exist.

Index maintenance rule: whenever a KB or LL file is created, or its topic/scope meaningfully changes, update its index line in the same operation. Routine enrichment that does not change the topic does not require an index update.

## 7. Raw File Ingestion Workflow

When the user places files in raw_knowledge_files/ and asks for ingestion:

1. Convert each raw file to Markdown with MarkItDown (see the ingest-raw-knowledge skill) and save the snapshot in raw_markdowns/ as <original_filename>.md. Snapshots are permanent.
2. Read each raw file fully, using both the direct reading and the MarkItDown snapshot, and extract ALL information and knowledge from it.
3. For pdf, pptx, docx and xlsx files, also extract the visual content (rendered pages and embedded images) with the skill's image extraction script, view the images, and capture their knowledge as text. The extracted images are temporary and are deleted with the raw file.
4. Decide placement by topic (see Section 8). Prefer enriching existing KB files over creating new ones.
5. Write or update the KB file(s): update Summary, Index, Sources, Related and the Updated date as needed.
6. Update knowledge_base/index.md if files were created or their topics changed.
7. Record the ingestion in raw_knowledge_files/tracker.md (see Section 9).
8. Delete the raw file (and its extracted images) after successful extraction, snapshot and tracker update.

## 8. Topic Splitting and Enrichment Rules

- Each KB file should capture ONE coherent topic.
- Before creating a new KB file, check knowledge_base/index.md: if a file on that topic already exists, enrich it instead of creating a new file.
- Only create a new KB file when the knowledge genuinely belongs to a topic not yet covered.
- A single raw file may feed several KB files if it covers several unrelated topics.
- Keep files digestible: if a file grows beyond roughly 500 lines, consider splitting it into subtopic files and updating index, tracker and Related sections accordingly.

## 9. Tracker (raw_knowledge_files/tracker.md)

The tracker records every raw file ever ingested, so provenance survives deletion of the raw file.

- One line per ingested raw file.
- Format: original_filename -> KBxxxx[, KByyyy, ...] (YYYY-MM-DD)
- Append new lines at the bottom. Never delete or rewrite old lines.

## 10. Continuous Learning Workflow

Use interactions with the user to grow both memories:

- If files (manuals, documentation, ...) are provided during a session and the user confirms they are correct, ingest them into the knowledge base following Section 7.
- If valuable information is discovered during a session (an error and its fix, a constraint, a working approach, a user preference), record it in lessons_learnt following Sections 5 and 6. Enrich an existing LL file if the topic already exists.
- The objective is to continuously improve knowledge_base and lessons_learnt through the interactions with the user.

## 11. Mandatory Answering Rules

1. Do not hallucinate.
2. If unsure, explicitly state uncertainty.
3. If evidence is missing, say: "I do not know based on the current knowledge base and lessons_learnt."
4. Prefer repository sources over model memory when answering questions.
5. Cite the source files (KBxxxx, LLxxxx) used for each answer.

## 12. Retrieval Protocol

1. Parse question intent and scope.
2. Consult knowledge_base/index.md and lessons_learnt/index.md first to locate candidate files.
3. If conflicting evidence exists, report the conflict and explain which source was chosen and why.

## 13. Confidence Policy

Confidence must always be included in final answers:

- High: direct, consistent evidence from relevant files.
- Medium: partial evidence, some assumptions required.
- Low: weak or outdated evidence, significant uncertainty.

## 14. Out-Of-Scope Handling

If the repository does not contain enough evidence:

- Be explicit that knowledge is incomplete.
- Ask targeted clarifying questions.
- Suggest which knowledge documents should be added.

## 15. Skills

Reusable procedures live in .github/skills/, one folder per skill with a SKILL.md describing when and how to perform the action. Current skills:

- ingest-raw-knowledge   : ingest raw files from raw_knowledge_files/ into the knowledge base (implements Sections 7 to 9).
- capture-lesson-learnt  : record a lesson from the current session into lessons_learnt/ (implements Sections 5, 6 and 10).
- validate-memory        : check repository consistency (naming, indexes, no tables, metadata, sections, tracker) and fix reported errors.
- dreaming               : memory consolidation pass; merge overlaps, fix drifted summaries/indexes/links, split oversized files, then validate.

When performing one of these actions, follow the corresponding skill. If a skill and this file ever disagree, this file wins; fix the skill.



