"""Build an evidence-labeled metrics report from a local JSON data bundle.

Usage:
  python metrics_report.py <bundle.json> [--out report.json]

The script reads local exports only; it does not connect to Notion or transmit
learner data. See references/metrics-plan.md for the input schema and caveats.
"""

import argparse
import json
import math
import statistics
import sys
from datetime import date
from pathlib import Path


def _date(value, field):
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be an ISO date (YYYY-MM-DD): {value!r}") from exc


def _rows(bundle, key):
    rows = bundle.get(key, [])
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError(f"{key} must be a list of objects")
    return rows


def _ratio(numerator, denominator, minimum=1):
    if denominator < minimum:
        return {"status": "Not measured", "value": None,
                "n": numerator, "denominator": denominator,
                "reason": f"needs at least {minimum} observations"}
    return {"status": "Measured", "value": round(numerator / denominator, 4),
            "n": numerator, "denominator": denominator}


def build_report(bundle):
    if not isinstance(bundle, dict):
        raise ValueError("the JSON bundle root must be an object")
    baseline = _rows(bundle, "baseline")
    learning = _rows(bundle, "learning_log")
    weak_spots = _rows(bundle, "weak_spots")

    baseline_by_topic = {row.get("topic"): float(row["manual_minutes"])
                         for row in baseline if row.get("topic")
                         and row.get("manual_minutes") is not None}
    logged_by_topic = {row.get("topic"): float(row["minutes_to_log"])
                       for row in learning if row.get("topic")
                       and row.get("minutes_to_log") is not None}
    if len(baseline_by_topic) != sum(bool(row.get("topic")) and row.get("manual_minutes") is not None for row in baseline):
        raise ValueError("baseline has duplicate topic entries")
    if len(logged_by_topic) != sum(bool(row.get("topic")) and row.get("minutes_to_log") is not None for row in learning):
        raise ValueError("learning_log has duplicate topic entries")
    baseline_minutes = list(baseline_by_topic.values())
    logged_minutes = list(logged_by_topic.values())
    if any(not math.isfinite(value) or value < 0 for value in baseline_minutes + logged_minutes):
        raise ValueError("minute values must be finite non-negative numbers")

    flagged = [row for row in learning if row.get("flagged") is True]
    confirmed_stuck = sum(row.get("flag_verdict") == "Stuck" for row in flagged)
    precision = _ratio(confirmed_stuck, len(flagged))

    annotations = bundle.get("annotations", {})
    if not isinstance(annotations, dict):
        raise ValueError("annotations must be an object")
    annotated = annotations.get("annotated_stuck_moments", 0)
    detected = annotations.get("detected_stuck_moments", 0)
    if (not isinstance(annotated, int) or isinstance(annotated, bool)
            or not isinstance(detected, int) or isinstance(detected, bool)):
        raise ValueError("annotation counts must be integers")
    if annotated < 0 or detected < 0 or detected > annotated:
        raise ValueError("annotation counts must satisfy 0 <= detected <= annotated")
    recall = _ratio(detected, annotated)

    teach_attempts = [row for row in learning
                      if row.get("teach_back_result") in ("Passed", "Needs work")]
    teach_passed = sum(row.get("teach_back_result") == "Passed" for row in teach_attempts)
    teach_rate = _ratio(teach_passed, len(teach_attempts))

    due_attempts = [row for row in learning if row.get("review_due") is True
                    and row.get("review_result") in ("Passed", "Needs work", "Failed")]
    due_passed = sum(row.get("review_result") == "Passed" for row in due_attempts)
    delayed_recall = _ratio(due_passed, len(due_attempts))

    durations = []
    for row in weak_spots:
        if row.get("confirmed") is not True or not row.get("resolved_on"):
            continue
        start = _date(row.get("flagged_on"), "weak_spots.flagged_on")
        end = _date(row.get("resolved_on"), "weak_spots.resolved_on")
        if start and end:
            if end < start:
                raise ValueError("resolved_on cannot precede flagged_on")
            durations.append((end - start).days)
    resolution = ({"status": "Measured", "median_days": statistics.median(durations),
                  "n": len(durations)} if len(durations) >= 2 else
                 {"status": "Not measured", "median_days": None, "n": len(durations),
                  "reason": "needs at least 2 confirmed resolved weak spots"})

    # Credit a style only when it was the first one used on a topic. The last
    # style tried before a pass would otherwise collect wins that earlier
    # explanations earned.
    style_counts = {}
    for row in learning:
        style = row.get("first_style")
        if not style or row.get("teach_back_result") not in ("Passed", "Needs work"):
            continue
        styles_tried = row.get("styles_tried", 1)
        if not isinstance(styles_tried, int) or isinstance(styles_tried, bool) or styles_tried < 1:
            raise ValueError("styles_tried must be a positive integer")
        won = row.get("teach_back_result") == "Passed" and styles_tried == 1
        wins, total = style_counts.get(style, (0, 0))
        style_counts[style] = (wins + won, total + 1)
    style_win_rate = {style: _ratio(wins, total, minimum=3)
                      for style, (wins, total) in sorted(style_counts.items())}

    eligible = [row for row in learning if row.get("eligible_for_application") is True]
    applied = sum(row.get("applied") is True for row in eligible)

    time_saved = None
    matched_topics = sorted(set(baseline_by_topic) & set(logged_by_topic))
    if len(matched_topics) >= 3:
        matched_baseline = sum(baseline_by_topic[topic] for topic in matched_topics)
        matched_logged = sum(logged_by_topic[topic] for topic in matched_topics)
        time_saved = {"status": "Measured",
                      "baseline_minutes": round(matched_baseline, 1),
                      "logged_minutes": round(matched_logged, 1),
                      "minutes_saved": round(matched_baseline - matched_logged, 1),
                      "matched_topics": len(matched_topics)}
    else:
        time_saved = {"status": "Not measured", "minutes_saved": None,
                      "baseline_topics": len(baseline_minutes), "logged_topics": len(logged_minutes),
                      "matched_topics": len(matched_topics),
                      "reason": "needs at least 3 topics timed in both workflows"}

    return {
        "report_date": date.today().isoformat(),
        "source": "local JSON bundle; no Notion connection used",
        "metrics": {
            "time_saved": time_saved,
            "flag_precision": precision,
            "flag_recall": recall,
            "teach_back_pass_rate": teach_rate,
            "delayed_recall": delayed_recall,
            "weak_spot_resolution_median_days": resolution,
            "application_rate": _ratio(applied, len(eligible)),
            "style_first_win_rate": style_win_rate,
        },
        "privacy": "Report contains aggregates only. Review before sharing.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", help="local JSON export using metrics-plan.md schema")
    parser.add_argument("--out", help="write report JSON to this path")
    args = parser.parse_args(argv)
    try:
        bundle = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
        report = build_report(bundle)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    output = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(output + "\n", encoding="utf-8")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
