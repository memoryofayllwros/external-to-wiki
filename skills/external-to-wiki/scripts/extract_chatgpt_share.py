#!/usr/bin/env python3
"""Extract conversation text from a public ChatGPT share URL.

Usage:
  python scripts/extract_chatgpt_share.py https://chatgpt.com/share/<id>
  python scripts/extract_chatgpt_share.py <url> --out /tmp/share.md

Requires network. Share pages are SPAs; content is pulled from embedded
React Router stream payloads when present. If extraction fails, paste
the chat into the agent instead.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_stream_blob(html: str) -> str | None:
    scripts = list(re.finditer(r"<script([^>]*)>(.*?)</script>", html, re.S))
    for match in scripts:
        body = match.group(2)
        if "streamController.enqueue" not in body:
            continue
        payloads = re.findall(
            r"window\.__reactRouterContext\.streamController\.enqueue\((\"(?:\\.|[^\"\\])*\")\)",
            body,
        )
        if not payloads:
            continue
        chunks = [json.loads(p) for p in payloads]
        return "".join(chunks)
    return None


def long_strings_from_blob(blob: str) -> list[str]:
    try:
        data = json.loads(blob)
    except json.JSONDecodeError:
        data = None

    found: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, str):
            if len(node) >= 80 and any(
                k in node
                for k in (
                    "## ",
                    "### ",
                    "Microservice",
                    "DDD",
                    "Capability",
                    "Bounded",
                    "微服务",
                    "领域",
                    "Architecture",
                )
            ):
                found.append(node)
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            for value in node.values():
                walk(value)

    if data is not None:
        walk(data)
    else:
        for raw in re.findall(r"\"((?:\\.|[^\"\\]){80,})\"", blob):
            try:
                text = json.loads(f'"{raw}"')
            except json.JSONDecodeError:
                continue
            if len(text) >= 80:
                found.append(text)

    # Dedupe preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for text in found:
        key = text[:200]
        if key in seen:
            continue
        seen.add(key)
        unique.append(text)
    return unique


def to_markdown(url: str, messages: list[str]) -> str:
    parts = [
        f"# ChatGPT share extract\n",
        f"Source: {url}\n",
        f"Messages/sections found: {len(messages)}\n",
    ]
    for i, text in enumerate(messages):
        parts.append(f"\n---\n\n## Extract {i}\n\n{text.strip()}\n")
    return "".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="ChatGPT share URL")
    parser.add_argument(
        "--out",
        type=Path,
        help="Write markdown to this path (default: stdout)",
    )
    args = parser.parse_args()

    if "chatgpt.com/share/" not in args.url and "chat.openai.com/share/" not in args.url:
        print("Expected a chatgpt.com/share/... URL", file=sys.stderr)
        return 2

    try:
        html = fetch_html(args.url)
    except Exception as exc:  # noqa: BLE001
        print(f"Fetch failed: {exc}", file=sys.stderr)
        return 1

    title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    if title:
        print(f"Title: {re.sub(r'<[^>]+>', '', title.group(1)).strip()}", file=sys.stderr)

    blob = extract_stream_blob(html)
    if not blob:
        print(
            "Could not find embedded conversation stream. "
            "Page may require login or the share format changed. Paste the chat instead.",
            file=sys.stderr,
        )
        return 1

    messages = long_strings_from_blob(blob)
    if not messages:
        print("Stream found but no contentful strings extracted.", file=sys.stderr)
        return 1

    md = to_markdown(args.url, messages)
    if args.out:
        args.out.write_text(md, encoding="utf-8")
        print(f"Wrote {args.out} ({len(messages)} sections)", file=sys.stderr)
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
