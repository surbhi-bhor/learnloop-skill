# Notion schema

The current setup has a Profile page and seven databases under one parent page:
Learning Log, Weak Spots, Reality Cards, Practice Bank, Project Ideas, Evidence
Ledger, and Skill Map. Keep property names exactly as written here: saved views,
filters, and other commands depend on them.

## Parent page

Title: `LearnLoop`. Created as a private page unless the user names a
destination. It holds the Profile page and seven databases.

## Profile

One private page under the parent page. Use the blank field prompts in
`teaching-styles.md` for roles, prior experience, target role and level,
portfolio, source material, and default style. Do not populate personal facts
without the user's input.

## Learning Log

One row per topic learned. The page body holds the note itself (see
`note-template.md`).

```sql
CREATE TABLE (
  "Topic" TITLE,
  "Date learned" DATE,
  "Format" SELECT('Detailed':blue, 'Table':green, 'Quiz':orange, 'Flashcards':purple),
  "Struggle score" NUMBER COMMENT '0 to 3, from scripts/struggle_score.py',
  "Re-ask count" NUMBER,
  "Flag verdict" SELECT('Not flagged':gray, 'Stuck':red, 'Just exploring':yellow) COMMENT 'Answer to: stuck, or just exploring?',
  "Style used" SELECT('Plain language first':gray, 'New to this topic':blue, 'Like I am 5':green, 'Bridge from my experience':purple, 'Gossip':pink, 'Bollywood':orange, 'Production war story':red, 'My own':brown) COMMENT 'The first style used on this topic',
  "Styles tried" NUMBER COMMENT 'How many styles were used before the topic was understood; 1 if the first worked',
  "Next review" DATE,
  "Last reviewed" DATE,
  "Review count" NUMBER,
  "Teach-back result" SELECT('Not attempted':gray, 'Passed':green, 'Needs work':orange),
  "Confidence" NUMBER COMMENT '1 to 5, set by the user',
  "Applied" CHECKBOX,
  "Minutes to log" NUMBER COMMENT 'From "log this" to the note written',
  "Source tool" SELECT('Claude Code':orange, 'Claude.ai':orange, 'ChatGPT':green, 'Gemini':blue, 'Other':gray),
  "Area" MULTI_SELECT('Python':blue, 'SQL':green, 'Spark':orange, 'Data modeling':purple, 'Pipelines':red, 'BI':pink, 'Testing':yellow, 'AI':brown, 'Other':gray),
  "Source type" SELECT('Chat':gray, 'YouTube':red, 'Article':blue, 'Course':green),
  "Source link" URL
)
```

## Weak Spots

One row per confirmed weak spot. Only topics the user confirms as "Stuck" get a
row here; dismissed flags stay in the Learning Log as "Just exploring" so flag
accuracy can be measured.

Create it after the Learning Log, replacing `<learning_log_ds>` with the Learning
Log data source ID:

```sql
CREATE TABLE (
  "Weak spot" TITLE,
  "Topic" RELATION('<learning_log_ds>', DUAL 'Weak Spots'),
  "Question trail" RICH_TEXT COMMENT 'My questions on this concept, in order',
  "Misconception" RICH_TEXT,
  "What clicked" RICH_TEXT,
  "Rule to remember" RICH_TEXT,
  "Delayed teach-back" SELECT('Not yet':gray, 'Passed':green, 'Failed':red),
  "Status" STATUS('Open':red:to_do, 'Resolved':green:complete),
  "Next review" DATE,
  "Last review" DATE,
  "Review count" NUMBER,
  "Flagged on" DATE,
  "Resolved on" DATE
)
```

`Status` moves to Resolved only after a delayed teach-back passes. Every new
row starts as Open with `Delayed teach-back` = Not yet.

## Reality Cards

One card per topic and target role, with source-backed task and production
context. Follow `reality-cards.md`; leave claims unverified when evidence is not
available.

```sql
CREATE TABLE (
  "Card" TITLE,
  "Topic" RELATION('<learning_log_ds>', DUAL 'Reality Cards'),
  "Role" SELECT('Senior Data Engineer':blue, 'Senior BI / Analytics Engineer':purple, 'Software Engineer':green, 'QA / SDET':yellow, 'AI / ML Engineer':orange, 'Other':gray),
  "Real task" RICH_TEXT,
  "Production failure" RICH_TEXT,
  "Filter or daily" SELECT('Interview filter':orange, 'Daily use':green, 'Both':blue, 'Unclear':gray),
  "Evidence label" SELECT('Widely agreed':green, 'Contested':orange, 'Anecdotal':pink, 'Unverified':gray),
  "Job description phrases" RICH_TEXT,
  "Smallest realistic exercise" RICH_TEXT,
  "Sources" RICH_TEXT,
  "Last verified" DATE
)
```

Create it after the Learning Log and substitute the Learning Log data source ID.
Do not create evidence-bearing cards until claims have supporting sources.

## Practice Bank

One question or drill per row. Define the answer criteria before asking the
learner, then record the attempt and result.

```sql
CREATE TABLE (
  "Question" TITLE,
  "Topic" RELATION('<learning_log_ds>', DUAL 'Practice Bank'),
  "Role" SELECT('Senior Data Engineer':blue, 'Senior BI / Analytics Engineer':purple, 'Software Engineer':green, 'QA / SDET':yellow, 'AI / ML Engineer':orange, 'Other':gray),
  "Difficulty" SELECT('Foundational':green, 'Intermediate':yellow, 'Advanced':red),
  "Type" SELECT('Recall':blue, 'Scenario':orange, 'Interview':purple),
  "Status" STATUS('Ready':blue:to_do, 'Attempted':yellow:in_progress, 'Passed':green:complete, 'Needs work':red:to_do),
  "Key points" RICH_TEXT,
  "Last attempt" DATE,
  "Attempt count" NUMBER,
  "Result" SELECT('Not attempted':gray, 'Passed':green, 'Needs work':orange, 'Failed':red)
)
```

## Project Ideas

One bounded exercise per row, related to the topic it applies.

```sql
CREATE TABLE (
  "Idea" TITLE,
  "Topic" RELATION('<learning_log_ds>', DUAL 'Project Ideas'),
  "Description" RICH_TEXT,
  "Portfolio link" URL,
  "Status" SELECT('Suggested':gray, 'In progress':yellow, 'Completed':green),
  "Date done" DATE
)
```

## Evidence Ledger

One draft or confirmed proof point per row. Only confirm details the learner
has reviewed. Keep missing measurements bracketed.

```sql
CREATE TABLE (
  "Evidence" TITLE,
  "Resume bullet or STAR story" RICH_TEXT,
  "Source project" RELATION('<project_ideas_ds>', DUAL 'Evidence'),
  "Source practice" RELATION('<practice_bank_ds>', DUAL 'Evidence'),
  "Target role" SELECT('Senior Data Engineer':blue, 'Senior BI / Analytics Engineer':purple, 'Software Engineer':green, 'QA / SDET':yellow, 'AI / ML Engineer':orange, 'Other':gray),
  "Status" SELECT('Draft':gray, 'Confirmed':green),
  "Date added" DATE
)
```

## Skill Map

One row per skill and target role. A blank level means the user has not rated
their current capability; it does not prove they lack the skill.

```sql
CREATE TABLE (
  "Skill" TITLE,
  "Role" SELECT('Senior Data Engineer':blue, 'Senior BI / Analytics Engineer':purple, 'Software Engineer':green, 'QA / SDET':yellow, 'AI / ML Engineer':orange, 'Other':gray),
  "Required in target JD" CHECKBOX,
  "Level" SELECT('Beginner':gray, 'Intermediate':blue, 'Advanced':purple, 'Expert':green),
  "Covered by" RELATION('<learning_log_ds>', DUAL 'Skill Map'),
  "Job description evidence" RICH_TEXT,
  "Last checked" DATE
)
```

Store only short requirement phrases and a source or job title, not a full
private job description.

## Saved views (created by `setup` with the create-view tool)

- Learning Log, "Flagged": `Flag verdict` is Stuck.
- Weak Spots, "Open weak spots": `Status` is Open, sorted by `Flagged on`.
- Learning Log, "Due today": `Next review` is on or before today, sorted by
  `Next review` ascending.
- Learning Log, "Learned but never applied": `Applied` is false, sorted by
  `Date learned` ascending.
- Learning Log, "What worked": `Teach-back result` is Passed, grouped by
  `Style used`.
- Skill Map, "Gaps": `Required in target JD` is true and `Level` is empty.

## Finding the workspace

The skill must work for anyone who installs it, with no file to edit. Find the
IDs in this order:

1. `config.local.json` in the skill folder, if it exists (a cache, optional).
2. Otherwise search Notion for a page titled exactly `LearnLoop`. Fetch it;
   its child pages and databases give the Profile page ID and each data
   source ID, matched by the titles in this file. Keep the IDs in memory for
   the rest of the conversation.
3. If no such page exists, this is a new user: say "You don't have a
   LearnLoop workspace in Notion yet. Want me to create one? It takes
   about a minute." and run `setup` on a yes.

If several pages match, use the one that has a `Learning Log` database and say
which one was used. Do not rename the parent page or the databases, because
step 2 finds them by title.

## Local config (optional cache)

When the skill folder is writable (Claude Code, Codex, Gemini CLI), write the
IDs to `config.local.json` after setup or after step 2 above, so later runs
skip the search. In apps where the skill folder is read-only (the Claude app),
skip this; step 2 finds the workspace each time.

```json
{
  "parent_page_id": "...",
  "profile_page_id": "...",
  "learning_log_data_source": "collection://...",
  "weak_spots_data_source": "collection://...",
  "reality_cards_data_source": "collection://...",
  "practice_bank_data_source": "collection://...",
  "project_ideas_data_source": "collection://...",
  "evidence_ledger_data_source": "collection://...",
  "skill_map_data_source": "collection://..."
}
```

This file holds only IDs, never note content. It must not be published with the
skill.
