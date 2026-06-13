# Contradictions

This folder is a maintainer queue, not a source of knowledge. Each file here records one contradiction the agent found inside the memory (knowledge_base/ or lessons_learnt/) or between incoming knowledge and what is already stored. Contradictions are surfaced here so a human maintainer can decide how to resolve them.

When this folder contains only this README, there are no open contradictions.

## Files

- cd-<slug>.md : one open contradiction, named in lowercase kebab-case after the conflicting topic, e.g. cd-k8s-rollback-window.md. These files are transient and deleted once resolved.
- These files never appear in any index and are never cited as evidence in answers.

## File Format

Plain lines and sections, no Markdown tables:

- Metadata: ID, Title, Created, Involves.
- Summary: what contradicts what.
- Conflicting Claims: each claim with its exact source.
- Analysis: why they conflict and the agent's confidence.
- Suggested Resolutions: options for the maintainer.

## Lifecycle

1. The agent detects a contradiction and creates a cd-<slug>.md file here. It never silently overwrites conflicting knowledge.
2. A human maintainer reviews it and decides the resolution.
3. The agent applies the decision to the affected KB/LL files.
4. The cd-<slug>.md file is deleted. The resolution lives in the corrected files and the git commit, not in this folder.

See the contradictions skill (.github/skills/contradictions/) for the step-by-step procedure.
