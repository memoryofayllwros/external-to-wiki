# Wiki reference

Defaults for the `external-to-wiki` workspace. Update when hubs or vaults move.

## Active target

| Key | Default | Notes |
|-----|---------|--------|
| `wiki.target` | `notion` | Set to `obsidian` when the user asks for Obsidian or a vault path |

## Notion (current)

### Hub

| Role | URL |
|------|-----|
| Architecture hub | `https://app.notion.com/p/3a1d27761991805d82e1e20dbddaa584` |
| Reading Path | `https://app.notion.com/p/3a2d27761991818ea272e532e637686b` |
| Recommended Books | `https://app.notion.com/p/3a2d277619918052afe4ea9e91f5851b` |
| Capability vs DDD vs Microservices | `https://app.notion.com/p/3a2d2776199181d0be93d44930b50b1c` |
| Building Microservices — Chapter Notes | `https://app.notion.com/p/3a2d2776199181deb826e9e2ed25a97c` |

Always `notion-fetch` the hub before writing — child order and URLs may change.

### Hub sections

```text
Start here
Core concepts
Platform
Code & data design
Integration patterns
Principles & reading
```

### MCP

- Server: `plugin-notion-workspace-notion`
- Auth with `mcp_auth` if `needsAuth`
- Avoid duplicate `Notion` in `~/.cursor/mcp.json` when the plugin already provides the server

### Write tips

- Leaf pages: `replace_content` OK for full rewrites
- Hubs: keep all child `<page url="...">` tags; relocate to reorder
- Sibling links: `<mention-page url="https://app.notion.com/p/..."/>`
- Code: fenced `plain text` or `python`

## Obsidian (optional / future)

Fill in when integrating a vault:

| Key | Value |
|-----|--------|
| `obsidian.vault_path` | _(unset — ask user or set here)_ |
| `obsidian.hub_folder` | e.g. `Architecture/` |
| `obsidian.index_note` | e.g. `Architecture/README.md` or `Architecture/Architecture.md` |
| `obsidian.reading_path` | e.g. `Architecture/Reading Path.md` |

### Conventions when writing Obsidian

- Related: `[[Note Name]]` or `[[path/Note Name]]`
- Source: YAML `source: <url>` and/or a `## Source` section
- Do not emit Notion XML (`<mention-page>`, `<callout>`, `<page url>`)
- Callouts (optional): Obsidian `> [!note]` / `> [!info]` syntax if the vault uses it

### Dual-write (later)

If the user asks to keep Notion and Obsidian in sync:

1. Produce one portable markdown draft
2. Write Notion via MCP adapter
3. Write Obsidian via vault adapter
4. Report both destinations

Until `obsidian.vault_path` is set, only use Obsidian when the user supplies a vault path in the request.

## Core topics (shared names)

| Topic | Notes |
|-------|--------|
| Business Capability-based Architecture | What the business sells / composes |
| Domain-Driven Design (DDD) | Model behavior, not tables |
| Bounded Context | Language + data ownership |
| Microservices | Deployment strategy, not the goal |
| Platform Vision | Capability marketplace |
| Product Intelligence as Source of Truth | Reusable Product capability |
| Repository Pattern / DIP | Code boundaries |
| API vs Event / Event-driven vs ES / Read Model | Integration |
| Architecture Principles | Prefer / avoid checklist |

Search before creating — names may already exist on either target.
