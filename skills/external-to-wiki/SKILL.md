---
name: external-to-wiki
description: >-
  Extract knowledge from ChatGPT shares, pasted chats, meeting notes, or other
  external sources; structure it; then merge into a personal wiki (Notion today,
  Obsidian-ready). Use when the user asks to enrich a wiki from ChatGPT, ingest
  a share URL, capture a discussion into Architecture / knowledge pages, or sync
  notes to Notion or Obsidian.
---

# External → Wiki

Turn external conversations into durable wiki content. Prefer **enriching existing pages** over creating long dumps. Judgment (where it belongs, what to merge) matters more than raw extraction.

**Targets:** Notion (default, via MCP) · Obsidian (vault markdown — see adapters below).

## When to use

- ChatGPT / Claude share links or pasted transcripts
- “Enrich Architecture / wiki from this discussion”
- Book or article notes that should link into an existing wiki
- Combining multiple sources into one wiki topic
- User names Notion **or** Obsidian as the destination

## Prerequisites

1. Confirm **wiki target**: `notion` (default) or `obsidian` (ask if unclear).
2. Target hub / vault path known — see [reference.md](reference.md).
3. For Notion: MCP authenticated (`plugin-notion-workspace-notion` or equivalent).

## Workflow

Copy and track:

```
Progress:
- [ ] 1. Ingest source
- [ ] 2. Extract & structure
- [ ] 3. Map to wiki
- [ ] 4. Write (update > create)
- [ ] 5. Discoverability
- [ ] 6. Report back
```

### 1. Ingest source

| Source | How |
|--------|-----|
| ChatGPT share URL (`chatgpt.com/share/...`) | Run `python scripts/extract_chatgpt_share.py <url>`. If it fails, ask user to paste export / key sections. |
| Pasted text | Use as-is |
| Existing wiki URL / note path | Fetch / read first; treat as target or secondary source |
| Book / article | Summarize chapter-by-chapter only if asked; otherwise key ideas |

Always keep the **canonical source URL** for citation.

### 2. Extract & structure

Pull only durable knowledge:

- Definitions, hierarchies, principles, prefer/avoid lists
- Decisions and rationale
- Concrete examples tied to the user’s domain
- Reading paths / book chapter maps

Drop: chit-chat, repeated affirmations, UI chrome, “as an AI…” filler.

Structure by type (pick one primary per note/page):

| Type | Shape |
|------|--------|
| Concept | Overview → Definition → Examples → Related |
| Comparison | Table of differences → When to use which |
| Decision | Context → Decision → Rationale → Consequences |
| Chapter notes | Ch.N summary → Related wiki links |
| Index / path | Ordered learning path (numbers live **here**, not in topic titles) |

Produce a **portable markdown draft** first (headings, lists, tables, fenced code). Then adapt to the target (Notion-flavored tags vs Obsidian wikilinks).

### 3. Map to wiki

1. Search / open the hub and candidate pages (Notion MCP or vault `grep` / glob).
2. Classify each chunk:
   - **Update** existing page (default)
   - **Create** child / sibling note only if no good home
   - **Index-only** (link from hub / Reading Path)
3. Never invent IDs or file paths — resolve them from the live wiki.

### 4. Write (update > create)

Use the adapter for the chosen target:

#### Notion adapter

- **Update**: `notion-update-page` (`update_content` / `replace_content`). Preserve existing child `<page url="...">` tags on hubs; move tags by cut/paste — don’t invent `<page>` for pages that already exist as children.
- **Create**: `notion-create-pages` under hub `page_id`. New children append at the end — reorder hub so the tag sits in the right section.
- Related links: `<mention-page url="...">`
- Cite source in a top callout or “Source” line.

#### Obsidian adapter

- Vault root: from user or [reference.md](reference.md) `obsidian.vault_path`.
- **Update**: edit existing `.md` in place; keep YAML frontmatter if present.
- **Create**: new note under the hub folder; use `[[Wiki Links]]` for Related.
- Optional frontmatter: `source`, `updated`, `tags`.
- Prefer plain GitHub-flavored markdown + wikilinks (no Notion-only XML tags).

### 5. Discoverability

After writes:

1. Update hub / MOC / index if new notes were added
2. Update Reading Path / Recommended Books (or Obsidian equivalent) for learning resources
3. Optionally reverse-link from 1–2 key topic pages (“Further reading”)

### 6. Report back

- Pages / notes created or updated (titles + links or paths)
- Target used (`notion` | `obsidian`)
- What was merged vs left out
- Source URL used

## Wiki conventions (this project)

See [reference.md](reference.md).

Hard rules (target-agnostic):

1. **Do not number topic titles** (no “Ch.5 Microservices”). Numbers only on Reading Path / chapter-notes pages.
2. **Merge into existing topics** when the outline already exists; deepen with follow-ups.
3. **Capability → DDD → Microservice (optional)** — keep layers distinct.
4. Prefer Modular Monolith first; microservice = deployment strategy.

## Anti-patterns

- One giant page that duplicates the whole ChatGPT thread
- Creating duplicates without searching first
- Notion: using `<page url>` to “add” an existing child (move the tag instead)
- Obsidian: Notion-only tags (`<mention-page>`, `<callout>`) left in vault files
- Chapter numbers on every wiki title
- Assuming Notion MCP when the user asked for Obsidian (or the reverse)

## Additional resources

- Hub URLs, vault path, adapters: [reference.md](reference.md)
- End-to-end examples: [examples.md](examples.md)
- ChatGPT share extractor: `scripts/extract_chatgpt_share.py`
