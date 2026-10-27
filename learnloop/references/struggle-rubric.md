# Struggle rubric

This rubric decides what counts as "stuck". It is the core of the skill, so read
it fully before grouping a conversation.

The split of work is deliberate. You (the model) judge meaning: which questions
are about the same concept, and which of the user's statements were wrong.
`scripts/struggle_score.py` does the counting, so the same grouping always gives
the same score.

## The five signals

| Signal | What to look for | Who detects it |
|---|---|---|
| Repeated | The same concept asked 3 or more times, in any wording. "How does a watermark differ from a checkpoint again?" after two earlier watermark questions. | You group turns; the script counts |
| Simplify request | "Explain it simpler", "give me an example", "like I'm 5", "break it down" | The script, by phrase match on grouped turns |
| Wrong summary | The user restates the idea and gets it wrong, for example "so retrying a failed load makes it idempotent". | You, with the exact quote and the correction |
| Hints needed | The user answers a check question only after two or more hints. | You. Only exists when the assistant asked check questions; past chats usually have none, so leave it at 0 |
| Said stuck | "I still don't get it", "I'm lost", "this doesn't make sense" | The script, by phrase match |

Each true signal is one point; the score is capped at 3. A concept is flagged
when it has 2 or more points, or when the user said they were stuck (that alone
is enough, because the user told you directly).

## Grouping turns into concepts

1. Run `struggle_score.py markers` first. It lists user turns with explicit
   struggle phrases, which are good starting points.
2. Read every user turn. Name concepts at the level a note would be written:
   "idempotent loads", not "data engineering" (too broad) or "the word
   idempotent" (too narrow).
3. Put a turn in a concept when answering it needs that concept. A turn can sit
   in two concepts if it really asks about both, such as "how is a watermark
   different from a checkpoint?".
4. Skip turns that are only logistics ("thanks", "write that as a table").
   Count follow-up requests like "show me the code for that" only if they show
   the user had not understood.
5. Record a misconception only when the user stated something false as their
   own understanding. A question is not a misconception, even a confused one.

Write the result as `concepts.json` (format in the script's docstring) and run
`struggle_score.py score`.

## Manual scoring (when the script cannot run)

Do the same counting the script does, in this order, and write it down as a
table so the learner can check it:

1. List the learner's turns for the concept by number, as in the grouping step.
2. **Repeated:** true if the concept has 3 or more of the learner's turns.
3. **Simplify request:** true if any of those turns asks to simplify, for an
   example or analogy, "like I'm 5", "in layman's terms", "step by step",
   "break it down", or to explain again or differently.
4. **Wrong summary:** true if the learner stated something false as their own
   understanding. Quote it.
5. **Hints needed:** true only if they needed 2 or more hints on a check
   question. Usually false for past chats.
6. **Said stuck:** true if any turn says "I still don't get it", "I'm
   confused", "I'm lost", "not following", "doesn't make sense", "I'm stuck",
   "this is confusing", or similar.
7. Score = number of true signals, capped at 3. Flag the concept when the
   score is 2 or more, or when "Said stuck" is true.
8. `Re-ask count` = the number of the learner's turns on the concept minus 1.

| Concept | Turns | Repeated | Simplify | Wrong summary | Hints | Said stuck | Score | Flagged |
|---|---|---|---|---|---|---|---|---|

Count only what is in the text; when unsure whether a phrase counts, leave the
signal false and mention it. This keeps hand scores close to what the script
would give.

## Curiosity is not struggle

Asking many questions about one topic can mean interest. The score is a
suggestion, never a verdict. For every flagged concept, ask the user:

> | Concept | Score | Evidence |
> |---|---|---|
> | <concept> | <score> | asked <n> times; "<quote>" |
>
> Misconception: "<what the learner said>". <why it is wrong, one line>.
>
> Were you stuck on <concept>, or just exploring?

- "Stuck": write the "Where I got stuck" block and a Weak Spots row.
- "Just exploring": write a normal note and set `Flag verdict` to Just exploring.
  Keep the record, because flag accuracy is measured from these answers.

Ask about all flagged concepts in one message, not one at a time.

## Known limits

- Phrase matching is English only and misses sarcasm or unusual wording. Your
  grouping catches what the phrases miss; the user's verdict catches the rest.
- Very short chats (under 4 user turns) rarely show repetition. Say so instead
  of forcing a flag.
