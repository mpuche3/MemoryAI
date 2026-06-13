# Agent Operating Policy

This file defines the mandatory behavior and conventions for any AI assistant (GitHub Copilot or other) working with this repository.
Read this file in full before doing anything else. Every rule here is binding.

## 1. Purpose of This Repository

This repository is the persistent memory of an AI agent. It stores two kinds of memory:

- knowledge_base/ : knowledge extracted from documents (manuals, papers, presentations, notes, ...).
- lessons_learnt/ : lessons gained from experience during sessions with the user (errors made, solutions found, constraints discovered).

Both memories store only what a general language model does not already know — internal, non-public, organization-specific knowledge — and store it densely (see Section 3, rules 6 and 7).

All memory files are plain Markdown (.md) or text (.txt). This keeps the repository small while holding a large amount of information.

## 2. Repository Structure

- AGENTS.md            : this file. The contract for all agent sessions.
- README.md            : human-facing description of the repository.
- knowledge_base/      : knowledge files kb-<slug>.md plus index.md.
- lessons_learnt/      : lesson files ll-<slug>.md plus index.md.
- contradictions/      : open contradictions flagged for human resolution, as cd-<slug>.md files plus README.md. Empty (only README) when none are open.
- raw_knowledge_files/ : inbox for raw files (pdf, pptx, docx, md, txt, ...) waiting to be ingested. Contains tracker.md.
- raw_markdowns/       : permanent Markdown snapshots of ingested raw files, produced by MarkItDown during ingestion. Named <original_filename>.md. Never deleted.
- .github/skills/      : skills (step-by-step procedures) available to the agent, one folder per skill with a SKILL.md inside.
- requirements.txt     : Python dependencies for the ingestion tooling.
- .venv/               : Python virtual environment with markitdown[all] and pymupdf installed, used by the ingestion skill. Not committed to git.

## 3. Content and Formatting Rules

1. NEVER use Markdown tables in any file in this repository. No exceptions. Files must read nicely as raw text without rendering.
2. Use plain "Key: value" lines for metadata. No YAML front matter fences. The only exception is SKILL.md files under .github/skills/, which require YAML front matter for VS Code to discover them.
3. Keep lines reasonably short and prose simple, so raw reading is comfortable.
4. File names are descriptive slugs, never sequential numbers. Knowledge files are kb-<slug>.md, lesson files ll-<slug>.md, contradiction files cd-<slug>.md. The slug is lowercase kebab-case (letters a-z, digits, hyphens), naming the topic, e.g. kb-kubernetes-rollback.md, ll-git-rebase-onto-pitfall.md. Choose broad, stable slugs so renames are rare. This scheme lets several people add files in parallel without numbering collisions: a filename clash then means the same topic, which must be enriched rather than duplicated. The ID metadata field always equals the file name without .md.
5. Date-stamp volatile facts. Knowledge that changes over time (versions, prices, APIs, settings, people in roles) must be phrased with its reference date, e.g. "As of 2026-06, the latest version is 1.27". Stable facts need no date.
6. Store only what the model does not already know. These memories are for knowledge that was NOT available to general language models at training time: internal, non-public, organization-specific knowledge — processes, methodologies, conventions, internal jargon, project and system specifics — plus lessons from sessions with the user. Do NOT store general knowledge the model already has (how Python works, what HTTP is, common algorithms). If a fact is public and stable, it does not belong here.
7. Keep knowledge dense. Write information-rich, well-structured, direct text: short sentences, lists and "Key: value" lines instead of long prose. Pack the most information into the fewest words while still reading nicely; shorter is better when no information is lost. Cut filler, repetition and obvious context.

## 4. Knowledge Base File Structure (kb-<slug>.md)

Every knowledge file follows this exact section order:

1. Metadata block at the very top, as plain lines:
   ID: kb-<slug>
   Title: short descriptive title
   Created: YYYY-MM-DD
   Updated: YYYY-MM-DD
   Tags: comma-separated lowercase tags
2. Summary: a short paragraph describing what knowledge this file holds.
3. Index: a table of contents listing the knowledge sections of the file, one line per section.
4. Sources: one line per source. Typically raw files that were ingested (and may already be deleted), or "Session with user YYYY-MM-DD".
5. Related: one line per related file (KB or LL), with the file name and a few words on why it is related. KB files may reference LL files and vice versa.
6. The actual knowledge content, organized in sections exactly as listed in the Index.

## 5. Lessons Learnt File Structure (ll-<slug>.md)

Identical structure to KB files (metadata, summary, index, sources, related, content).
The difference is the origin: lessons come from experience during sessions, not from documents.
A lesson should capture: the context, what was attempted, what went wrong or what was discovered, the root cause if known, and the rule to follow in the future.
Sources for lessons are usually "Session with user YYYY-MM-DD".

## 6. Index Files (knowledge_base/index.md and lessons_learnt/index.md)

Each index file starts with a short paragraph explaining itself, then lists every file in the folder:

- One line per file, in alphabetical order.
- Format of each line: kb-<slug>.md - brief one-line description of the file's topic and contents (ll-<slug>.md in the lessons index).
- Every KB/LL file in the folder MUST appear in the index. The index must never list files that do not exist.

Index maintenance rule: whenever a KB or LL file is created, renamed, or its topic/scope meaningfully changes, update its index line in the same operation. Routine enrichment that does not change the topic does not require an index update.

## 7. Raw File Ingestion Workflow

When the user places files in raw_knowledge_files/ and asks for ingestion:

1. Convert each raw file to Markdown with MarkItDown (see the ingest-raw-knowledge skill) and save the snapshot in raw_markdowns/ as <original_filename>.md. Snapshots are permanent.
2. Read each raw file fully, using both the direct reading and the MarkItDown snapshot. Understand all of it, but store only the knowledge a general language model would not already have — internal, non-public, organization-specific information (Section 3, rule 6) — written densely (rule 7).
3. For pdf, pptx, docx and xlsx files, also extract the visual content (rendered pages and embedded images) with the skill's image extraction script, view the images, and capture their knowledge as text. The extracted images are temporary and are deleted with the raw file.
4. Decide placement by topic (see Section 8). Prefer enriching existing KB files over creating new ones.
5. Write or update the KB file(s): update Summary, Index, Sources, Related and the Updated date as needed. If incoming knowledge contradicts existing KB content, do not overwrite it: flag a contradiction (see Section 11).
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
- Format: original_filename -> kb-<slug>[, kb-<other-slug>, ...] (YYYY-MM-DD)
- Append new lines at the bottom. Never delete or rewrite old lines.

## 10. Continuous Learning Workflow

Use interactions with the user to grow both memories:

- If files (manuals, documentation, ...) are provided during a session and the user confirms they are correct, ingest them into the knowledge base following Section 7.
- If valuable information is discovered during a session (an error and its fix, a constraint, a working approach, a user preference), record it in lessons_learnt following Sections 5 and 6. Enrich an existing LL file if the topic already exists.
- The objective is to continuously improve knowledge_base and lessons_learnt through the interactions with the user.

## 11. Contradictions

When new knowledge conflicts with knowledge already stored, the agent must NEVER silently overwrite it or pick a winner on its own. It records the conflict in the contradictions/ folder for a human maintainer to resolve.

- Folder: contradictions/. It holds one file per open contradiction plus a README.md that explains the folder. When the folder has only the README, there are no open contradictions.
- File names: cd-<slug>.md, lowercase kebab-case naming the conflicting topic (e.g. cd-k8s-rollback-window.md). Transient: deleted once resolved.
- These files do NOT appear in any index and are NOT a source of knowledge for answers; they are a maintainer queue.

File structure (plain lines and sections, no tables):

1. Metadata: ID (cd-<slug>), Title, Created (YYYY-MM-DD), Involves (the KB/LL files or incoming sources in conflict).
2. Summary: one paragraph stating what contradicts what.
3. Conflicting Claims: each claim with its exact source (file and section, or incoming raw file and date).
4. Analysis: why they conflict, whether both could be true under a different scope or date, and the agent's confidence.
5. Suggested Resolutions: options for the maintainer, with a recommendation if there is one.

When to create one:

- During ingestion, when an incoming document contradicts existing KB content.
- During lesson capture, when a new lesson contradicts an existing lesson or KB file.
- During dreaming or answering, when two stored files are found to disagree.

Do not lose the new information: the contradiction file itself preserves both claims. Optionally add a one-line "Contradiction flagged: see cd-<slug>" note to the Related section of each involved KB/LL file, and remove it when resolved.

Lifecycle: created by the agent, then reviewed and decided by a human maintainer, then the agent applies the decision to the affected KB/LL files, then the contradiction file is deleted. The resolution is recorded by the edits to the KB/LL files and the git commit, not by keeping the CD file. See the contradictions skill.

## 12. Mandatory Answering Rules

1. Do not hallucinate.
2. If unsure, explicitly state uncertainty.
3. If evidence is missing, say: "I do not know based on the current knowledge base and lessons_learnt."
4. Prefer repository sources over model memory when answering questions.
5. Cite the source files (kb-<slug>, ll-<slug>) used for each answer.

## 13. Retrieval Protocol

1. Parse question intent and scope.
2. Consult knowledge_base/index.md and lessons_learnt/index.md first to locate candidate files.
3. If conflicting evidence exists, report the conflict and explain which source was chosen and why.
4. Before answering, check contradictions/: if an open contradiction involves a file you are about to cite, surface it to the user and lower your confidence accordingly.

## 14. Confidence Policy

Confidence must always be included in final answers:

- High: direct, consistent evidence from relevant files.
- Medium: partial evidence, some assumptions required.
- Low: weak or outdated evidence, significant uncertainty.
- An open contradiction involving a cited file caps confidence at Medium and must be surfaced.

## 15. Out-Of-Scope Handling

If the repository does not contain enough evidence:

- Be explicit that knowledge is incomplete.
- Ask targeted clarifying questions.
- Suggest which knowledge documents should be added.

## 16. Skills

Reusable procedures live in .github/skills/, one folder per skill with a SKILL.md describing when and how to perform the action. Current skills:

- ingest-raw-knowledge   : ingest raw files from raw_knowledge_files/ into the knowledge base (implements Sections 7 to 9).
- capture-lesson-learnt  : record a lesson from the current session into lessons_learnt/ (implements Sections 5, 6 and 10).
- validate-memory        : check repository consistency (naming, indexes, no tables, metadata, sections, tracker) and fix reported errors.
- dreaming               : memory consolidation pass; merge overlaps, fix drifted summaries/indexes/links, split oversized files, then validate.
- contradictions         : flag and resolve contradictions between stored knowledge (implements Section 11).

When performing one of these actions, follow the corresponding skill. If a skill and this file ever disagree, this file wins; fix the skill.



