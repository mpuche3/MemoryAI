# MemoryAI

**Give your AI agent a memory that survives the conversation.**

Every chat session with an AI assistant starts from zero: the documents you explained yesterday, the bug it helped you fix last week, the preferences you repeated ten times — all gone. MemoryAI fixes that with a simple idea: store the agent's memory as plain Markdown files in a git repository, and teach the agent to read, grow and maintain that memory itself.

No vector database. No embeddings pipeline. No external service. Just text files, git and an agent that follows rules.

## How It Works

The agent (GitHub Copilot in VS Code) operates this repository under a binding contract (AGENTS.md). It has two long-term memories:

- **knowledge_base/** — knowledge extracted from documents. Drop a PDF, PPTX or DOCX into the inbox folder, ask the agent to ingest it, and it converts the file with Microsoft MarkItDown, reads it (text AND rendered images), extracts every piece of knowledge into topic-focused KB files, indexes them, records provenance, and deletes the original. The knowledge of a 40 MB slide deck becomes a few KB of readable Markdown.

- **lessons_learnt/** — experience gained during sessions. When something fails for a non-obvious reason, when a constraint is discovered, when you say "remember this" — the agent writes a lesson with context, root cause and the rule to follow next time. Mistakes become rules instead of repeats.

## Why This Design Wins

- **Signal, not noise.** The memory stores only what a general language model does not already know — internal, non-public, organization-specific knowledge — written as densely as possible. No filler, no re-explaining what the model can already do.
- **Token-efficient by construction.** Raw documents are heavy and noisy; distilled Markdown is light and dense. The agent consults a one-line-per-file index first and loads only the files it needs.
- **Human-readable, human-auditable.** Every memory is plain text with a strict structure (metadata, summary, index, sources, related files). No tables, no rendering needed — you can read your agent's entire memory in a text editor and correct it with a keystroke.
- **Full provenance.** Every knowledge file lists its sources; an append-only tracker records every ingested file and where its knowledge went; permanent Markdown snapshots of the originals are kept. You can always answer "why does the agent believe this?"
- **Honest about conflicts.** When new knowledge contradicts what is already stored, the agent never silently overwrites it — it files the conflict in `contradictions/` for a human to resolve, so disagreements are surfaced, not buried.
- **Versioned like code, because it is like code.** Git gives you history, diffs, rollback and backup of the agent's mind for free. One commit per ingestion = an audit trail of how the memory evolved.
- **Built for collaboration.** Files are named after their topic (`kb-kubernetes-rollback.md`), not by sequential number, so several people can add knowledge in parallel without merge collisions — and when two people do pick the same name, that is the signal they documented the same topic and should merge it.
- **Self-maintaining.** The agent doesn't just write memory — it maintains it through built-in procedures (skills):
  - `ingest-raw-knowledge` — documents in, distilled knowledge out
  - `capture-lesson-learnt` — experience in, future-proof rules out
  - `validate-memory` — consistency checker for naming, indexes, structure and provenance
  - `dreaming` — periodic consolidation pass (like sleep does for memories): merge overlaps, fix drift, split oversized files
  - `contradictions` — flag conflicting knowledge for human resolution instead of silently overwriting
- **Grounded answers.** The contract obliges the agent to prefer repository evidence over model memory, cite the files it used, state its confidence, and say "I don't know" when the memory has no answer.

## Quick Start

1. Clone the repo and open it in VS Code with GitHub Copilot.
2. Recreate the Python environment (used for document conversion):
   `python -m venv .venv` then `.venv\Scripts\python.exe -m pip install -r requirements.txt`
3. Drop documents into raw_knowledge_files/ and tell the agent: *"ingest the raw files"*.
4. Ask questions. The agent answers from its memory, with citations and confidence.
5. When something valuable is learnt during a session: *"capture this lesson"*.
6. Every now and then: *"dream"* — and the memory reorganizes itself.

## Repository Layout

- AGENTS.md — the contract: every convention, structure and workflow the agent must follow.
- knowledge_base/ — kb-<slug>.md knowledge files plus index.md.
- lessons_learnt/ — ll-<slug>.md lesson files plus index.md.
- contradictions/ — conflicts the agent flagged for a human to resolve (empty when none are open).
- raw_knowledge_files/ — ingestion inbox, plus the append-only tracker.md.
- raw_markdowns/ — permanent MarkItDown snapshots of every ingested document.
- .github/skills/ — the agent's procedures (ingestion, lessons, validation, dreaming).
