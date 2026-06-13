---
name: dreaming
description: 'Memory consolidation pass over knowledge_base/ and lessons_learnt/, like dreaming consolidates memories during sleep. Use when the user asks to dream, consolidate, clean up, reorganize or do maintenance on the memory. Merges overlapping content, fixes drifted summaries and indexes, repairs Related links, splits oversized files and validates the result.'
---

# Dreaming (Memory Consolidation)

Periodic maintenance pass that keeps the memory healthy, like dreaming consolidates memories during sleep. Repeated enrichment causes drift: overlapping content across files, summaries that no longer match the content, stale Related links, files growing past digestible size. Dreaming repairs that drift. Follow the conventions in AGENTS.md (which is binding).

## When to Use

- The user asks to "dream", consolidate, clean up or reorganize the memory.
- After many ingestions or lesson captures (roughly every 10).

## Procedure

1. Read knowledge_base/index.md and lessons_learnt/index.md fully.
2. Look for topic overlap at the index level: files whose descriptions suggest the same or strongly overlapping topics. Read those files fully.
3. For each KB/LL file (or at least those touched since the last dreaming pass):
   - Check the Summary still matches the actual content; rewrite it if it drifted.
   - Check the Index lists exactly the sections present, in order; fix mismatches.
   - Check Related links point to existing files and still make sense; add missing links (both directions), remove dead or irrelevant ones.
   - Check for content duplicated in another file: keep it in the file where it belongs topically, replace the duplicate with a Related reference.
   - If two files disagree on a fact (not just overlap in topic), do NOT silently choose one: flag a contradiction (see the contradictions skill).
   - If two files genuinely cover one topic, merge into the file with the broader or more established slug, leave nothing behind, and remove the emptied file from its index. Record the merge in the kept file's Sources ("Merged from kb-<slug>, YYYY-MM-DD"). If any other file referenced the removed slug, repoint it.
   - If a file exceeds roughly 500 lines, split it by subtopic into new kb-<slug>.md files, updating index, Related and (for KB files) adding a note to Sources.
   - Refresh date-stamped volatile facts that are known to be outdated; if outdated but the current value is unknown, mark the line with "(possibly outdated as of YYYY-MM-DD)".
   - Tighten verbose content: make it denser without losing information (AGENTS.md Section 3, rule 7), and drop any general knowledge the model already knows (rule 6).
   - Update the Updated date of every modified file.
4. Update both index.md files to reflect any creations, merges, splits or topic changes.
5. If any merge or split changed where ingested content lives, do NOT rewrite old tracker.md lines (it is append-only); instead append a correction line, e.g.:
   correction: kb-old-topic merged into kb-new-topic (YYYY-MM-DD)
6. Run the validate-memory skill and fix every error.
7. Report to the user: files merged, split, rewritten or relinked, and anything suspicious left untouched.

## Cautions

- Dreaming reorganizes; it must never lose knowledge. When merging or splitting, verify every content section survived somewhere.
- Do not delete or weaken lessons in lessons_learnt/ just because they seem old: lessons stay valid until proven wrong.
- When in doubt about a merge, leave the files separate and report the doubt to the user instead.
- Prefer many small dreaming passes over one huge restructuring. If a pass would touch more than about ten files, propose the plan to the user before acting.
- Commit (or let the user commit) before a large pass, so everything is reversible.
