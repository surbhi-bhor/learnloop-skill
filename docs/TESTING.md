# Validation plan

Run this after the build is reviewed. Status on 2026-10-24: section 1 passes
(17 tests), the trigger eval passed 16 of 16 on an earlier description, and
sections 2 to 5 still need real sessions and learner data.

## 1. Local scripts

From the project root:

```powershell
python -m pytest -q          # or: python -m unittest discover tests
python tools/package_skill.py
```

`tools/package_skill.py` must report OK before any upload. Optional, and costly
because it starts one Claude session per query:
`python tests/trigger_eval.py --runs 2` checks which requests load the skill.

Then run the metrics reporter with a temporary synthetic bundle that matches
`learnloop/references/metrics-plan.md`. Confirm the output labels
insufficient data `Not measured`; never use the synthetic report as learner
evidence.

## 2. Skill activation

Open a fresh session in each supported surface from this project folder:

- Codex: ask to save a learning topic and confirm `AGENTS.md` routes to
  `learnloop/SKILL.md` before Notion access.
- Claude Code: ask to teach and then capture a concept; confirm `CLAUDE.md` and
  the skill workflow load.
- Gemini CLI: use `/skills list` if installed as a skill, or ask a learning
  request in the project and confirm `GEMINI.md` is followed.
- Chat surface without skill loading: use the paste-in prompt and confirm it
  asks for a learner verdict before recording flagged struggle.

Do not save synthetic test content to the live Learning Log.

## 3. Capture quality gate

Use three learner-annotated stuck chats and one control chat. Mark the learner's
stuck moments before running capture. Record the learner's verdict for every
flag. Calculate precision and recall only after the full set is processed.
Targets: at least 80% precision, at least 70% recall, and zero confirmed flags
on the control chat.

## 4. Notion workflow

With the private workspace configured, verify setup references each database
and view correctly. On a test topic, inspect the study note, relation links,
weak-spot verdict, practice rubric, next review date, and Skill Map behavior.
Delete test rows after inspection unless the learner wants to retain them.

## 5. User-specific gates

- Fill Profile fields only with learner-provided facts and confirm the chosen
  teaching style.
- Supply a target job description and confirm that Skill Map stores short
  evidence phrases rather than the full description.
- Attempt a practice item and a due review; confirm results and next dates.
- Build metric input only from reviewed records and compare it with source
  counts before sharing.

## Exit decision

Record pass/fail, evidence, and unresolved issues in GitHub Issues. Keep phases
that need user data open until their real-data gates pass.
