"""Normalize an AI chat transcript into a numbered list of turns.

Supported inputs:
  - ChatGPT data export (conversations.json, "mapping" tree)
  - Claude data export (conversations.json, "chat_messages" list)
  - Plain text pasted from any chat app, with speaker labels such as
    "You:", "User:", "ChatGPT said:", "Claude:", "Gemini:"

Output (stdout, JSON):
  {"title": str, "source": str, "turns": [{"index": int, "role": "user"|"assistant", "text": str}]}


Usage:
  python parse_transcript.py <file> [--list] [--title TEXT | --pick N] [--out FILE]
"""

import argparse
import json
import re
import sys
from pathlib import Path

USER_LABELS = ["you", "user", "me", "human"]
ASSISTANT_LABELS = ["chatgpt", "claude", "gemini", "assistant", "ai", "copilot"]

# Matches "You:", "**You:**", "ChatGPT said:", "## Claude", "Gemini:" at line start.
LABEL_RE = re.compile(
    r"^\s*(?:#+\s*)?\**\s*(?P<label>[A-Za-z]+)(?:\s+said)?\s*\**\s*:?\s*\**\s*$"
    r"|^\s*\**(?P<inline>[A-Za-z]+)(?:\s+said)?\**\s*:\s*\**\s*(?P<rest>.*)$"
)


def _role_for(label):
    label = label.lower()
    if label in USER_LABELS:
        return "user"
    if label in ASSISTANT_LABELS:
        return "assistant"
    return None


def parse_plain_text(text):
    turns = []
    current_role, buffer = None, []

    def flush():
        body = "\n".join(buffer).strip()
        if current_role and body:
            turns.append({"role": current_role, "text": body})

    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        match = None if in_fence else LABEL_RE.match(line)
        role = None
        rest = ""
        if match:
            label = match.group("label") or match.group("inline")
            role = _role_for(label)
            rest = match.group("rest") or ""
            # "AI: ..." inside an answer is usually quoted dialogue, not a new
            # speaker, so an inline label only starts a turn when the speaker
            # changes. A label alone on its line ("ChatGPT said:") always does.
            if role and match.group("inline") and role == current_role:
                role = None
        if role:
            flush()
            current_role, buffer = role, ([rest] if rest else [])
        else:
            buffer.append(line)
    flush()
    return turns


def _chatgpt_turns(conversation):
    mapping = conversation.get("mapping", {})
    node_id = conversation.get("current_node")
    chain = []
    while node_id:
        node = mapping.get(node_id, {})
        chain.append(node)
        node_id = node.get("parent")
    turns = []
    for node in reversed(chain):
        message = node.get("message") or {}
        role = (message.get("author") or {}).get("role")
        if role not in ("user", "assistant"):
            continue
        parts = (message.get("content") or {}).get("parts") or []
        text = "\n".join(p for p in parts if isinstance(p, str)).strip()
        if text:
            turns.append({"role": role, "text": text})
    return turns


def _claude_turns(conversation):
    turns = []
    for message in conversation.get("chat_messages", []):
        role = "user" if message.get("sender") == "human" else "assistant"
        text = message.get("text") or ""
        if not text:
            blocks = message.get("content") or []
            text = "\n".join(b.get("text", "") for b in blocks if b.get("type") == "text")
        text = text.strip()
        if text:
            turns.append({"role": role, "text": text})
    return turns


def load_conversations(path):
    """Return a list of (title, source, turns) found in the file."""
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return [(Path(path).stem, "plain_text", parse_plain_text(raw))]

    if isinstance(data, dict):
        data = [data]
    conversations = []
    for conv in data:
        if "mapping" in conv:
            conversations.append((conv.get("title") or "untitled", "chatgpt_export", _chatgpt_turns(conv)))
        elif "chat_messages" in conv:
            conversations.append((conv.get("name") or "untitled", "claude_export", _claude_turns(conv)))
    if not conversations:
        raise ValueError("JSON file is not a recognized ChatGPT or Claude export")
    return conversations


def number(turns):
    return [{"index": i, **turn} for i, turn in enumerate(turns, start=1)]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file")
    parser.add_argument("--list", action="store_true", help="list conversation titles and exit")
    parser.add_argument("--title", help="pick the first conversation whose title contains this text")
    parser.add_argument("--pick", type=int, help="pick conversation by number from --list")
    parser.add_argument("--out", help="write JSON here instead of stdout")
    args = parser.parse_args(argv)

    conversations = load_conversations(args.file)

    if args.list:
        for i, (title, source, turns) in enumerate(conversations, start=1):
            print(f"{i}\t{len(turns)} turns\t{source}\t{title}")
        return 0

    if args.title:
        chosen = [c for c in conversations if args.title.lower() in c[0].lower()]
        if not chosen:
            print(f"No conversation title contains '{args.title}'", file=sys.stderr)
            return 1
        title, source, turns = chosen[0]
    elif args.pick:
        title, source, turns = conversations[args.pick - 1]
    elif len(conversations) == 1:
        title, source, turns = conversations[0]
    else:
        print("File holds several conversations; use --list, then --title or --pick", file=sys.stderr)
        return 1

    result = json.dumps({"title": title, "source": source, "turns": number(turns)}, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(result, encoding="utf-8")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
