"""Count struggle signals in a normalized transcript.

The model decides meaning (which questions are about the same concept, which of
my statements were wrong). This script does the counting, so scores are the
same every run.

Commands:
  markers <transcript.json>
      List user turns that contain explicit struggle phrases. The model reads
      this before grouping questions into concepts.

  score <transcript.json> <concepts.json>
      Score each concept the model grouped. concepts.json looks like:
      {"concepts": [{"concept": "idempotent loads",
                     "user_turns": [3, 7, 11],
                     "misconceptions": [{"turn": 7, "said": "...", "correction": "..."}],
                     "hints_needed": 0}]}

  Use "-" to read from stdin when files cannot be written: "markers -" reads
  the transcript, and "score -" reads {"transcript": ..., "concepts": ...}.

Output is JSON on stdout. See references/struggle-rubric.md for what each
signal means and how the score is used.
"""

import json
import re
import sys
from pathlib import Path

SIMPLIFY_RE = re.compile(
    r"\b(simpler|simplify|simple terms|plain (english|words|terms|language)|eli5"
    r"|like i'?m (5|five|new|a kid)|explain (it |that |this )?(again|differently|another way)"
    r"|give me an? (example|analogy)|another example|break (it|this|that) down|dumb (it|this) down"
    r"|eli10|in layman'?s terms|for a beginner|step by step|slow (it )?down|more slowly)\b",
    re.IGNORECASE,
)
DIRECT_RE = re.compile(
    r"(still (don'?t|do not|can'?t) (get|understand|see)|i'?m (so |still )?(confused|lost)"
    r"|(doesn'?t|does not|still doesn'?t) make sense|makes no sense|i (don'?t|do not) (get|understand)"
    r"|not clicking|doesn'?t click|went over my head|(i'?m )?not following|you lost me|lost me"
    r"|i'?m (still )?stuck|still (unclear|confusing|confused)|(this|that|it)( i|')s (so |really |super )?confusing"
    r"|that makes no sense|no idea what)",
    re.IGNORECASE,
)
# Phrases that often start a re-ask. Informational only: the model decides
# whether a turn really repeats an earlier question.
REASK_RE = re.compile(
    r"\b(again|wait|so (is|does|do|basically|you mean)|how is (this|that|it) different"
    r"|what'?s the difference|difference between|i thought|remind me|one more time"
    r"|are you saying|just to confirm|let me get this straight|correct me if|what do you mean)\b"
    r"|^\s*so\b",  # "So retrying makes it idempotent?" restates an earlier answer
    re.IGNORECASE | re.MULTILINE,
)

REPEAT_THRESHOLD = 3  # same concept asked this many times counts as repeated
HINT_THRESHOLD = 2    # needing this many hints on a check question counts


def load_json(path):
    if path == "-":
        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8")
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def user_turns(transcript):
    return {t["index"]: t for t in transcript["turns"] if t["role"] == "user"}


def find_markers(text):
    hits = {}
    for name, regex in (("simplify", SIMPLIFY_RE), ("direct", DIRECT_RE), ("reask_phrase", REASK_RE)):
        found = [m.group(0) for m in regex.finditer(text)]
        if found:
            hits[name] = found
    return hits


def markers(transcript):
    result = []
    for index, turn in user_turns(transcript).items():
        hits = find_markers(turn["text"])
        if hits:
            result.append({"turn": index, "hits": hits, "text": turn["text"][:200]})
    return {"user_turn_count": len(user_turns(transcript)), "marked_turns": result}


def score_concept(concept, turns_by_index):
    warnings = []
    asked = []
    for index in concept.get("user_turns", []):
        if index in turns_by_index:
            asked.append(index)
        else:
            warnings.append(f"turn {index} is not a user turn; ignored")

    simplify_turns, direct_turns = [], []
    for index in asked:
        hits = find_markers(turns_by_index[index]["text"])
        if "simplify" in hits:
            simplify_turns.append(index)
        if "direct" in hits:
            direct_turns.append(index)

    misconceptions = concept.get("misconceptions", [])
    hints_needed = concept.get("hints_needed", 0)

    signals = {
        "repeated": len(asked) >= REPEAT_THRESHOLD,
        "simplify_request": bool(simplify_turns),
        "wrong_summary": bool(misconceptions),
        "hints_needed": hints_needed >= HINT_THRESHOLD,
        "said_stuck": bool(direct_turns),
    }
    points = sum(signals.values())
    flagged = signals["said_stuck"] or points >= 2
    priority = "high" if flagged and (points >= 3 or (signals["repeated"] and points >= 2)) else (
        "normal" if flagged else "none"
    )

    return {
        "concept": concept["concept"],
        "struggle_score": min(points, 3),
        "flagged": flagged,
        "priority": priority,
        "re_ask_count": max(len(asked) - 1, 0),
        "signals": signals,
        "evidence": {
            "question_trail": asked,
            "simplify_turns": simplify_turns,
            "said_stuck_turns": direct_turns,
            "misconceptions": misconceptions,
            "hints_needed": hints_needed,
        },
        "warnings": warnings,
    }


def score(transcript, concepts):
    turns_by_index = user_turns(transcript)
    results = [score_concept(c, turns_by_index) for c in concepts.get("concepts", [])]
    results.sort(key=lambda r: (not r["flagged"], -r["struggle_score"]))
    return {"concepts": results, "flagged_count": sum(r["flagged"] for r in results)}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) == 2 and argv[0] == "markers":
        output = markers(load_json(argv[1]))
    elif len(argv) == 3 and argv[0] == "score":
        output = score(load_json(argv[1]), load_json(argv[2]))
    elif len(argv) == 2 and argv[0] == "score" and argv[1] == "-":
        combined = load_json("-")
        output = score(combined["transcript"], combined["concepts"])
    else:
        print(__doc__, file=sys.stderr)
        return 2
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
