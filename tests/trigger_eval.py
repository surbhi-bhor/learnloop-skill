"""Check that the installed learnloop skill triggers on the right requests.

Runs each query through `claude -p` in an empty folder and watches the stream
for the first tool call. A query counts as triggered when that call is the
Skill tool loading learnloop (or a Read of its SKILL.md). The process is
killed at the first tool call, and Notion, Bash and file-writing tools are
disallowed, so nothing is written anywhere.

Windows-safe replacement for skill-creator's run_eval.py, which uses
select() on pipes (not supported on Windows) and tests a temporary copy that
would compete with the installed skill.

Usage: python tests/trigger_eval.py [--runs N] [--workers N] [--out results.json]
"""

import argparse
import json
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SKILL = "learnloop"
EVAL_SET = Path(__file__).parent / "trigger_queries.json"
BLOCKED = ["Bash", "PowerShell", "Write", "Edit", "NotebookEdit", "mcp__claude_ai_Notion", "Agent"]


def run_once(query, cwd, timeout):
    cmd = ["claude", "-p", query, "--output-format", "stream-json", "--verbose",
           "--disallowedTools", *BLOCKED]
    process = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                               stdin=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
    timer = threading.Timer(timeout, process.kill)
    timer.start()
    first_tool = None
    try:
        for line in process.stdout:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") != "assistant":
                continue
            for item in event.get("message", {}).get("content", []):
                if item.get("type") == "tool_use":
                    first_tool = (item.get("name"), item.get("input", {}))
                    break
            if first_tool:
                break
    finally:
        timer.cancel()
        if process.poll() is None:
            process.kill()
        process.wait()
    if not first_tool:
        return False, "no tool call"
    name, tool_input = first_tool
    if name == "Skill" and SKILL in str(tool_input.get("skill", "")):
        return True, f"Skill({tool_input.get('skill')})"
    if name == "Read" and SKILL in str(tool_input.get("file_path", "")):
        return True, "Read SKILL.md"
    detail = tool_input.get("skill") or tool_input.get("query") or ""
    return False, f"{name}({detail})"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--out")
    args = parser.parse_args()

    queries = json.loads(EVAL_SET.read_text(encoding="utf-8"))
    cwd = tempfile.mkdtemp(prefix="lta-trigger-")
    jobs = [(q, r) for q in queries for r in range(args.runs)]

    started = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        outcomes = list(pool.map(lambda job: run_once(job[0]["query"], cwd, args.timeout), jobs))

    results = {}
    for (q, _), (triggered, detail) in zip(jobs, outcomes):
        entry = results.setdefault(q["query"], {"should_trigger": q["should_trigger"], "runs": []})
        entry["runs"].append({"triggered": triggered, "first_tool": detail})

    correct = 0
    sys.stdout.reconfigure(encoding="utf-8")
    for query, entry in results.items():
        rate = sum(r["triggered"] for r in entry["runs"]) / len(entry["runs"])
        ok = (rate >= 0.5) == entry["should_trigger"]
        correct += ok
        expected = "TRIGGER" if entry["should_trigger"] else "skip   "
        tools = "; ".join(r["first_tool"] for r in entry["runs"])
        print(f"{'PASS' if ok else 'FAIL'}  expect {expected}  rate {rate:.0%}  [{tools}]  {query[:70]}")
    print(f"\n{correct}/{len(results)} correct in {time.time() - started:.0f}s")

    if args.out:
        Path(args.out).write_text(json.dumps(results, indent=2), encoding="utf-8")
    return 0 if correct == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
