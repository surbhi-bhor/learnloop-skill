# Metrics plan

This is a measurement contract, not a report of results. Populate metrics only
from dated records in the Learning Log and Weak Spots databases or from a
baseline measured by the learner. Do not infer values from missing fields.

## Input bundle for the local report

Export or assemble a JSON file with this shape, then run
`python scripts/metrics_report.py <bundle.json> [--out report.json]` from the
skill directory. Provide no names, conversation text, or Notion page IDs.

```json
{
  "baseline": [{"topic": "idempotent loads", "manual_minutes": 18}],
  "learning_log": [{
    "topic": "idempotent loads",
    "minutes_to_log": 4.5,
    "flagged": true,
    "flag_verdict": "Stuck",
    "teach_back_result": "Passed",
    "first_style": "Plain language first",
    "styles_tried": 1,
    "review_due": true,
    "review_result": "Passed",
    "eligible_for_application": true,
    "applied": false
  }],
  "weak_spots": [{
    "confirmed": true,
    "flagged_on": "2026-01-01",
    "resolved_on": "2026-01-08"
  }],
  "annotations": {
    "annotated_stuck_moments": 3,
    "detected_stuck_moments": 2
  }
}
```

Rows in this example only document the schema; they are not project results.
Match the `topic` value exactly across baseline and Learning Log rows; topics
without a match are excluded from time-saved calculations.
Set `flagged` true for a flag shown to the learner even if they later mark it
`Just exploring`. `review_due` identifies a due retrieval attempt, and
`review_result` records the actual result.

| Metric | Definition | Minimum data | Limitation |
|---|---|---|---|
| Time saved | Sum of manual baseline minutes minus LearnLoop `Minutes to log` for matched topics | At least 3 topics timed in both workflows | Logging time excludes time spent answering clarification questions |
| Flag precision | Confirmed Stuck flags / all flags shown | At least 3 annotated stuck chats plus 1 control chat | Requires learner verdicts; a synthetic fixture is not evidence |
| Flag recall | Learner-annotated stuck moments detected / all annotated stuck moments | Same annotated set as precision | Depends on the learner's pre-run annotations |
| Teach-back pass rate | Passed teach-backs / attempted teach-backs | Dated practice attempts and fixed pass criteria | Self-grading can be lenient; keep the required points visible |
| Delayed recall | Passed due reviews / due reviews attempted | At least one full review interval | Report after the interval; skipped reviews are not passes |
| Style first-win rate | Per style: topics passed with that style as the only style tried / topics where it was the first style | `first_style`, `styles_tried` and a teach-back result per topic | Needs 3 topics per style. A pass after switching styles counts against the first style, so later styles cannot collect earlier styles' wins |
| Weak-spot resolution time | Resolved date minus flagged date | Confirmed weak spots with both dates | Report median after multiple resolved records; one record is descriptive only |
| Application rate | Topics marked Applied / topics eligible for application | User-confirmed Applied values | Do not count suggested projects as completed application |

## Collection rules

- Preserve the source rows and date range behind every summary.
- Keep counts and denominators together; show `n/N` with percentages.
- Mark missing or insufficient data as `Not measured`.
- Do not publish private study content or personal metrics without the learner's
  explicit choice.
- The current Notion setup does not include a metrics history database or
  automatic extraction. The local report script accepts an explicit JSON bundle;
  prepare that bundle from user-reviewed aggregates and retain the source
  locally. A later Notion-backed extraction would need consent and retention
  rules before it is added.
