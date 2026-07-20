# Examples

## Example A — Enrich Architecture from a ChatGPT share (Notion)

**User:** Enrich Architecture based on `https://chatgpt.com/share/...`

**Agent:**

1. Target = `notion` (default).
2. Run `python scripts/extract_chatgpt_share.py <url>`.
3. `notion-fetch` hub + thin topic pages.
4. Update existing topics; create only if missing (e.g. synthesis page).
5. Cite share URL; reorder hub; update Reading Path if needed.
6. Reply with Notion links.

## Example B — Same flow to Obsidian

**User:** Put this ChatGPT share into my Obsidian Architecture vault at `~/Notes`.

**Agent:**

1. Target = `obsidian`; `vault_path` = `~/Notes`.
2. Extract share → portable markdown draft.
3. Find/create notes under `Architecture/` with `[[wikilinks]]`.
4. Update MOC / Reading Path note.
5. Reply with file paths (no Notion XML in vault files).

## Example C — Book chapter notes

**User:** Summarize Building Microservices chapter by chapter into the wiki and link topics.

**Agent:**

1. Create `Building Microservices — Chapter Notes` under the hub (Notion page or Obsidian note).
2. Each chapter: summary + Related links (`<mention-page>` or `[[...]]`).
3. Link from Recommended Books / Reading Path.
4. Do **not** rename topic titles to “Ch.5 …”.

## Example D — Pasted discussion, no URL

1. Extract durable bullets; discard filler.
2. Search wiki for matching titles.
3. Prefer update over create.
4. Source: “Captured from pasted chat (no share URL)” unless provided.

## Example E — Conflict: chat contradicts wiki

1. Do not silently overwrite.
2. Surface conflict or add “Open question / alternative view” with source cited.
3. Prefer principles / prefer-avoid pages for deltas.

## Example F — Dual-write (when asked)

1. One portable draft.
2. Notion adapter + Obsidian adapter.
3. Report both destinations and any drift.
