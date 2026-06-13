---
name: contradictions
description: 'Flag and resolve contradictions in the memory. Use when ingestion, a new lesson, dreaming or a question reveals that two pieces of stored knowledge disagree, or when the user asks to review, resolve or clear the contradictions queue. Records each conflict in contradictions/ for a human decision, then applies the decision and deletes the file.'
---

# Contradictions

Detect, flag and resolve contradictions in knowledge_base/ and lessons_learnt/, following AGENTS.md Section 11 (binding). The agent never silently overwrites conflicting knowledge or picks a winner on its own; it flags the conflict for a human maintainer.

## When to Use

- Flagging: during ingestion, lesson capture, dreaming or answering, when stored knowledge disagrees with new knowledge or with itself.
- Resolving: when the user asks to review, resolve or clear the contradictions queue.

## Flagging a Contradiction

1. Confirm it is a real conflict, not two facts that are both true under a different scope or at different dates. If they are compatible, prefer date-stamping or scoping both claims in the KB file instead of flagging.
2. Create a new file contradictions/cd-<slug>.md from [the template](./assets/template.md), the slug naming the conflicting topic in lowercase kebab-case (e.g. cd-k8s-rollback-window.md).
3. Fill in: Involves (the files or sources), Summary, both Conflicting Claims with exact sources, Analysis with confidence, and Suggested Resolutions.
4. Do not lose information: the file preserves both claims. Optionally add a one-line "Contradiction flagged: see cd-<slug>" note to the Related section of each involved KB/LL file.
5. Tell the user a contradiction was flagged and where.

## Resolving Contradictions

1. List the cd-<slug>.md files in contradictions/. For each, read it and the files it Involves.
2. Present the contradiction and the suggested resolutions to the user and ask for a decision. The decision is the human's to make.
3. Apply the chosen resolution to the affected KB/LL files: correct the wrong claim, or date-stamp/scope both claims if they are time-bound. Update the Updated date and, if the topic changed, the index.
4. Remove any "Contradiction flagged: see cd-<slug>" note from the involved files' Related sections.
5. Delete contradictions/cd-<slug>.md. The resolution is preserved by the edits to the KB/LL files and the git commit message.
6. Run the validate-memory skill and report what was resolved.

## Cautions

- Never resolve a contradiction by guessing. If the user is unavailable, leave the file in place.
- Never delete a contradiction file without first applying its resolution to the memory.
- Keep contradiction files out of indexes and never cite them as evidence; they are a queue, not knowledge.
