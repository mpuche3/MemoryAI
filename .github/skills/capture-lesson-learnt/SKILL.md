---
name: capture-lesson-learnt
description: 'Record a lesson learnt from the current session into lessons_learnt/ as an LLxxxx.md file. Use when an error and its fix, a constraint, a working approach, or a user preference is discovered, or when the user says "remember this", "capture this lesson", or "do not make this mistake again".'
---

# Capture Lesson Learnt

Persist experience gained during a session into lessons_learnt/, following the conventions in AGENTS.md (which is binding; re-read it if in doubt).

## When to Use

- Something was attempted and failed for a non-obvious reason, and the cause or fix is now known.
- A constraint, working approach, or user preference was discovered during the session.
- The user explicitly asks to remember or capture something as a lesson.

## Procedure

1. Read lessons_learnt/index.md to see which lesson topics already exist.
2. Decide placement:
   - If an LL file already covers the topic, ENRICH it (add a new section, update Index, Summary, Updated date).
   - Otherwise create a new LL file with the next free LLxxxx number (4 digits, sequential, never reused).
3. Write the lesson with the exact structure required by AGENTS.md Section 5, starting new files from [the LL template](./assets/template.md):
   metadata block (ID, Title, Created, Updated, Tags), Summary, Index, Sources, Related, then the content sections exactly as listed in the Index.
   - The content of each lesson must capture: the context, what was attempted, what went wrong or was discovered, the root cause if known, and the rule to follow in the future.
   - Sources line is usually "Session with user YYYY-MM-DD".
   - Cross-link related KB and LL files in Related (both directions when meaningful).
   - If the lesson conflicts with an existing lesson or KB file, do NOT overwrite it: flag a contradiction (see the contradictions skill and AGENTS.md Section 11).
   - NEVER use Markdown tables. Plain "Key: value" lines, no YAML fences inside LL files.
   - If a file would exceed roughly 500 lines, split by subtopic.
4. Update lessons_learnt/index.md if a file was created or its topic changed: one line per file, alphabetical order, format "LLxxxx.md - brief description".
5. Confirm to the user what was recorded and where.

## Quality Bar

- Record rules, not anecdotes: the future-facing rule is the most important part.
- Be specific enough that a future session can apply the lesson without extra context.
- Do not duplicate knowledge that belongs in knowledge_base/; link to the KB file instead.
