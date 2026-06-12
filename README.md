# MemoryAI

Persistent memory repository for an AI agent (GitHub Copilot in VS Code).

- knowledge_base/ holds knowledge extracted from documents, as KBxxxx.md files plus an index.md.
- lessons_learnt/ holds lessons gained from experience during sessions, as LLxxxx.md files plus an index.md.
- raw_knowledge_files/ is the inbox: drop raw files (pdf, pptx, md, ...) here and ask the agent to ingest them. tracker.md records what was ingested and where it went; raw files are deleted after ingestion.
- raw_markdowns/ keeps a permanent Markdown snapshot of every ingested raw file, generated with Microsoft MarkItDown.
- .github/skills/ holds the skills (step-by-step procedures) the agent uses, such as ingesting raw files and capturing lessons.
- AGENTS.md is the binding contract: all conventions, file structures and workflows are defined there.

All memory is stored as plain Markdown/text, with no tables, so every file reads nicely in raw form.
