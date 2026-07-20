# external-to-wiki

Cursor project for personal wiki workflows (Architecture knowledge base).

## Skills

| Skill | Path | Use |
|-------|------|-----|
| **external-to-wiki** | `.cursor/skills/external-to-wiki/` | Extract from ChatGPT / chats → structure → merge into wiki (**Notion** default, **Obsidian**-ready) |

Invoke with `/external-to-wiki` or ask naturally, e.g. “enrich Architecture from this ChatGPT share”.

### Quick extract

```bash
python .cursor/skills/external-to-wiki/scripts/extract_chatgpt_share.py \
  'https://chatgpt.com/share/<id>' --out /tmp/share.md
```

## Prerequisites

- **Notion:** plugin MCP authenticated; avoid a duplicate `Notion` entry in `~/.cursor/mcp.json` if the plugin already provides the server
- **Obsidian:** set `obsidian.vault_path` in `.cursor/skills/external-to-wiki/reference.md`, or pass the vault path in the request
