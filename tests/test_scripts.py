"""Tests for the Phase 1 scripts. Run with: python -m unittest discover tests"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "learnloop" / "scripts"))

import parse_transcript  # noqa: E402
import struggle_score  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "idempotent_loads_chat.txt"


def transcript_from_fixture():
    title, source, turns = parse_transcript.load_conversations(FIXTURE)[0]
    return {"title": title, "source": source, "turns": parse_transcript.number(turns)}


class PlainTextParsing(unittest.TestCase):
    def test_splits_chatgpt_copy_paste_into_alternating_turns(self):
        transcript = transcript_from_fixture()
        roles = [t["role"] for t in transcript["turns"]]
        self.assertEqual(len(roles), 11)
        self.assertEqual(roles[:4], ["user", "assistant", "user", "assistant"])
        self.assertEqual(transcript["source"], "plain_text")

    def test_inline_and_bold_labels(self):
        turns = parse_transcript.parse_plain_text(
            "**You:** what is a heap?\n**Claude:** A tree where each parent is smaller.\nYou: and a min-heap?"
        )
        self.assertEqual([t["role"] for t in turns], ["user", "assistant", "user"])
        self.assertEqual(turns[0]["text"], "what is a heap?")

    def test_ordinary_colon_lines_stay_in_the_turn(self):
        turns = parse_transcript.parse_plain_text("You: hi\nClaude: Note: this is one turn\nExample: still the same")
        self.assertEqual(len(turns), 2)
        self.assertIn("Example: still the same", turns[1]["text"])


class ExportParsing(unittest.TestCase):
    def write_json(self, data):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(data, handle)
        handle.close()
        self.addCleanup(Path(handle.name).unlink)
        return handle.name

    def test_chatgpt_export_follows_current_branch(self):
        conversation = {
            "title": "Lists",
            "current_node": "c",
            "mapping": {
                "root": {"message": None, "parent": None},
                "a": {"parent": "root", "message": {"author": {"role": "user"}, "content": {"parts": ["what is a list?"]}}},
                "old": {"parent": "a", "message": {"author": {"role": "assistant"}, "content": {"parts": ["abandoned branch"]}}},
                "b": {"parent": "a", "message": {"author": {"role": "assistant"}, "content": {"parts": ["An ordered collection."]}}},
                "c": {"parent": "b", "message": {"author": {"role": "user"}, "content": {"parts": ["thanks"]}}},
            },
        }
        (title, source, turns), = parse_transcript.load_conversations(self.write_json([conversation]))
        self.assertEqual((title, source), ("Lists", "chatgpt_export"))
        self.assertEqual([t["text"] for t in turns], ["what is a list?", "An ordered collection.", "thanks"])

    def test_claude_export_reads_content_blocks(self):
        conversation = {
            "name": "SCD",
            "chat_messages": [
                {"sender": "human", "text": "what is SCD type 2?"},
                {"sender": "assistant", "text": "", "content": [{"type": "text", "text": "It keeps history rows."}]},
            ],
        }
        (title, source, turns), = parse_transcript.load_conversations(self.write_json([conversation]))
        self.assertEqual(source, "claude_export")
        self.assertEqual(turns[1], {"role": "assistant", "text": "It keeps history rows."})

    def test_unknown_json_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_transcript.load_conversations(self.write_json({"foo": 1}))


class StruggleScoring(unittest.TestCase):
    def setUp(self):
        self.transcript = transcript_from_fixture()

    def test_markers_find_simplify_and_said_stuck(self):
        marked = {m["turn"]: m["hits"] for m in struggle_score.markers(self.transcript)["marked_turns"]}
        self.assertIn("simplify", marked[5])
        self.assertIn("direct", marked[7])

    def test_struggling_concept_is_flagged_high(self):
        concepts = {"concepts": [
            {"concept": "idempotent loads", "user_turns": [1, 3, 5, 7],
             "misconceptions": [{"turn": 3, "said": "retrying makes it idempotent", "correction": "retry is safe only if the load is idempotent"}]},
            {"concept": "watermarks", "user_turns": [9]},
        ]}
        result = struggle_score.score(self.transcript, concepts)
        top, other = result["concepts"]
        self.assertEqual(top["concept"], "idempotent loads")
        self.assertTrue(top["flagged"])
        self.assertEqual(top["struggle_score"], 3)
        self.assertEqual(top["priority"], "high")
        self.assertEqual(top["re_ask_count"], 3)
        self.assertFalse(other["flagged"])
        self.assertEqual(other["struggle_score"], 0)
        self.assertEqual(result["flagged_count"], 1)

    def test_said_stuck_alone_flags(self):
        concepts = {"concepts": [{"concept": "merge", "user_turns": [7]}]}
        (only,) = struggle_score.score(self.transcript, concepts)["concepts"]
        self.assertTrue(only["flagged"])
        self.assertEqual(only["struggle_score"], 1)

    def test_assistant_turn_in_grouping_is_ignored_with_warning(self):
        concepts = {"concepts": [{"concept": "x", "user_turns": [2]}]}
        (only,) = struggle_score.score(self.transcript, concepts)["concepts"]
        self.assertEqual(only["evidence"]["question_trail"], [])
        self.assertTrue(only["warnings"])


class MetricsReport(unittest.TestCase):
    def test_documented_example_bundle(self):
        import re
        import metrics_report
        plan = (ROOT / "learnloop" / "references" / "metrics-plan.md").read_text(encoding="utf-8")
        bundle = json.loads(re.search(r"```json\n(.*?)```", plan, re.S).group(1))
        metrics = metrics_report.build_report(bundle)["metrics"]
        self.assertEqual(metrics["time_saved"]["status"], "Not measured")
        self.assertEqual(metrics["flag_recall"]["value"], 0.6667)
        self.assertEqual(metrics["weak_spot_resolution_median_days"]["status"], "Not measured")

    def test_empty_bundle_reports_nothing_as_measured(self):
        import metrics_report
        metrics = metrics_report.build_report({})["metrics"]
        self.assertEqual(metrics.pop("style_first_win_rate"), {})
        self.assertTrue(all(m["status"] == "Not measured" for m in metrics.values()))


class ParserQuotedDialogue(unittest.TestCase):
    def test_same_speaker_inline_label_stays_in_turn(self):
        turns = parse_transcript.parse_plain_text(
            "You: how do chatbots log turns?\nClaude: Each line is tagged.\nAI: hello is how a bot line looks")
        self.assertEqual([t["role"] for t in turns], ["user", "assistant"])
        self.assertIn("AI: hello", turns[1]["text"])

    def test_labels_inside_code_fence_are_ignored(self):
        turns = parse_transcript.parse_plain_text(
            "You: show a transcript\nClaude: Here:\n```\nUser: hi\nAI: hello\n```\nDone.")
        self.assertEqual(len(turns), 2)
        self.assertIn("User: hi", turns[1]["text"])


class WiderMarkers(unittest.TestCase):
    def test_new_struggle_phrases(self):
        self.assertIn("direct", struggle_score.find_markers("sorry, I'm not following"))
        self.assertIn("direct", struggle_score.find_markers("this is so confusing"))
        self.assertIn("simplify", struggle_score.find_markers("explain in layman's terms"))
        self.assertIn("reask_phrase", struggle_score.find_markers("So retrying makes it idempotent?"))

    def test_plain_question_has_no_markers(self):
        self.assertEqual(struggle_score.find_markers("What is a watermark in streaming?"), {})


class StyleFirstWin(unittest.TestCase):
    def test_pass_after_switching_counts_against_first_style(self):
        import metrics_report
        rows = [{"topic": f"t{i}", "first_style": "Gossip", "styles_tried": tried,
                 "teach_back_result": "Passed"} for i, tried in enumerate([1, 1, 2])]
        rows.append({"topic": "t9", "first_style": "Bollywood", "styles_tried": 1, "teach_back_result": "Passed"})
        rate = metrics_report.build_report({"learning_log": rows})["metrics"]["style_first_win_rate"]
        self.assertEqual(rate["Gossip"]["value"], 0.6667)
        self.assertEqual(rate["Bollywood"]["status"], "Not measured")


if __name__ == "__main__":
    unittest.main()
