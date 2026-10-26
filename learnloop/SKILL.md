---
name: learnloop
description: Turns what the user learned in the current chat (or an exported chat file) into a full study note in their Notion Learning Log, records where they got stuck, and runs their learning loop - styled teaching, real-job reality cards, practice and teach-backs, spaced review, and job-description gap checks. Use whenever the user wants learning saved, noted or logged ("log this", "log this in notion", "save this to notion", "add this to my notes", "note this down", "make flashcards or a quiz from this"), asks what they struggled with, asks to be taught in a named style ("teach me X like Bollywood", "explain using my past experience"), asks how a topic is used on the job, asks for practice, a drill or a teach-back, asks what is due for review, pastes a job description to compare, or shares a resume to set up their profile. Load it before any Notion tool call for these requests; it holds the note format and how to find the Notion workspace. A plain "what is X" question does not need it.
---

# LearnLoop

Learners study new topics in chat. Copying notes into Notion by hand is slow,
the notes end up as passive summaries, the places they got stuck disappear, and
the topic is rarely practiced or applied. Learners also forget the next step.
So the main command, `log this`, does the whole job in one go: a full study
note, where they got stuck, how the topic applies to their target role,
interview questions, a drill, a mini-project and review dates, then it offers
the next step.

Commands:

| Command | Use it when the learner... |
|---|---|
| `log this` | wants what they learned saved (the main command) |
| `setup` | has no LearnLoop workspace in Notion yet, or asks to set up |
| `profile import` | shares a resume, LinkedIn text or portfolio |
| `teach` | asks to be taught, possibly in a named style |
| `reality` | asks how a topic is used on the job |
| `practice` | asks for a quiz, drill, teach-back or mini-project |
| `review` | asks what is due, or to retry a weak spot |
| `jd-check` | pastes a job description to compare |

Struggle scores and style results are suggestions for the learner to confirm,
not verdicts. Metrics that need weeks of history stay unreported until
measured.

Scripts live in `scripts/` next to this file. Run them with Python 3.11 or newer;
they use only the standard library.

## Finding the Notion workspace

Anyone can install this skill, so never assume a config file exists. Before the
first Notion read or write in a conversation, find the workspace as described
in "Finding the workspace" in `references/notion-schema.md`: use
`config.local.json` if present, otherwise search Notion for the
`LearnLoop` page, otherwise offer `setup`. If no Notion tool is connected
at all, write the note in the chat, say it was not saved, and tell the learner
to connect Notion in their app's connector settings.

The skill needs these Notion tools: search, fetch, create pages, update page,
query data sources, create database and create view (in the official Notion
connector they are named `notion-search`, `notion-fetch`,
`notion-create-pages`, `notion-update-page`, `notion-query-data-sources`,
`notion-create-database`, `notion-create-view`). Some apps load connector
tools only on request. If only listing or calendar tools are visible, search
for the missing ones by those exact names (for example a tool search for
"notion-fetch notion-create-pages notion-update-page") before deciding they
are unavailable. If they still do not load, say which ones are missing, give
the learner the content to paste, and suggest starting a new chat, since
tool loading is per chat.

## Command: setup

Run when the user asks to set up, or when no `LearnLoop` workspace is
found.

1. Read `references/notion-schema.md`.
2. Ask where to put the `LearnLoop` page. If the user names no destination,
   create it as a private page and tell them they can move it.
3. Create the Learning Log database under it, then the Weak Spots database using
   the Learning Log data source ID for the relation.
4. Create a `Profile` page under it using the blank fields in
   `references/teaching-styles.md`. Do not fill in personal history or
   preferences without the user's input.
5. Create the Reality Cards database using the Learning Log data source ID for
   the relation, following `references/notion-schema.md`.
6. Create Practice Bank and Project Ideas using the Learning Log data source
   ID for their topic relations.
7. Create Evidence Ledger using the Practice Bank and Project Ideas data
   source IDs for its source relations.
8. Create Skill Map using the Learning Log data source ID for its coverage
   relation.
9. If the skill folder is writable, write the IDs to `config.local.json` as
   the schema file shows. If it is not (the Claude app), skip it; the
   workspace is found by title next time.
10. Create the saved views defined in `references/notion-schema.md`: Flagged,
   Open weak spots, Due today, Learned but never applied, and What worked.
   Create Gaps in Skill Map.

## Command: teach

When the user asks to learn or understand a topic, read
`references/teaching-styles.md` and consult the Profile page if its ID is
available. Use a named style from the request first; otherwise use the saved
default, then fall back to Plain language first. If a needed profile detail is
blank, teach without personalizing rather than inventing a bridge.

Keep the explanation accurate and suited to the requested depth. Include at
least one visual (a mermaid diagram, a comparison table or a text diagram,
chosen with "Visual aids" in `references/note-template.md`). Include a
two-sentence **In plain terms** recap, state where any analogy stops matching
the real mechanism, and finish with at least one style-free check question. Do
not present a style preference as a proven learning advantage; use it as the
learner's chosen explanation format. Track styles for the metrics: when the topic is logged,
`Style used` is the first style used on it and `Styles tried` is how many
styles were used in total (1 if the first one worked).

## Command: reality

When the user asks how a topic is used at work, read
`references/reality-cards.md` and `references/role-packs.md`. Use the target
role in the Profile page when available. Research current job expectations and
cite the sources used; if browsing or source material is unavailable, mark the
claim unverified instead of presenting it as fact. Separate widely agreed,
contested, and anecdotal claims. Keep each card tied to a specific role and
topic. Do not imply that an interview pattern is universal.

## Command: practice

When the user asks for practice, a quiz, a drill, a teach-back, a mini-project,
or evidence of application, read `references/practice-and-evidence.md` and
consult the topic note, Profile, and any linked Reality Card. Choose a practice
rung suited to the learner's prior attempts and target role. Define two or
three required points before grading a teach-back; explain the result and one
next step. Do not mark a Weak Spot resolved until a delayed teach-back passes.

Create project ideas and evidence only when they connect to a real topic or
user-described work. Resume bullets and STAR stories must use user-provided
facts; leave unknown measures bracketed and drafts unconfirmed.

## Command: review

When the user asks what is due, to review a topic, or to retry a weak spot, read
`references/review-schedule.md`. Select due topics and open weak spots from the
Notion views, ask for recall before showing answers, then record the attempt.
Use the specified intervals; do not mark a record complete merely because it
was opened. A weak spot closes only after a delayed teach-back passes.

## Command: jd-check

When the user asks to compare a job description with their skills or learning,
read `references/jd-check.md`. Use the supplied description and profile target
role, match requirements to actual learning and application evidence, and
label gaps as missing evidence rather than assumed inability. Store short
requirement phrases in Skill Map; do not copy full job descriptions into
Notion.

## Command: log this

Record the start time with a shell command (for example `date +%s`) when the
command starts, and read the clock again just before writing to Notion.
`Minutes to log` is the difference, rounded to one decimal. Never estimate it:
it is the main time-saved metric, and a guessed number makes it worthless.
If no shell or clock is available, leave `Minutes to log` empty rather than
estimating. Also leave it empty when the note was drafted in an earlier chat
or attempt and is only being saved now, because the clock would measure the
save and not the whole job.

### 1. Get the transcript

- **From this session** (the default: "log this" with no file means the chat
  the user is in right now): use the conversation already available in context;
  do not require an export of the active chat. If a transcript file is useful,
  write only the relevant user and assistant messages to a temp file in the
  parser's format (`{"title", "source", "turns": [{"index", "role",
  "text"}]}`), numbered from 1. Leave out tool calls and file dumps; keep what
  was said. If the session covered work
  besides learning, keep only the learning stretch; if it covered several
  topics and "this" is unclear, ask which one in the step 3 message.
- **From a file**: run
  `python scripts/parse_transcript.py <file> --list`. If it holds several
  conversations, ask which one (or match the topic the user named with
  `--title`), then run it again with `--out <temp>/transcript.json`.
  Supported: ChatGPT export `conversations.json`, Claude export
  `conversations.json`, and plain text pasted from any chat app with speaker
  labels ("You:", "ChatGPT said:", "Gemini:").

If the parser finds no turns, the labels were probably not recognized. Show the
first lines of the file and ask the user which lines start each speaker.

### 2. Detect struggle

1. Read `references/struggle-rubric.md`.
2. Run `python scripts/struggle_score.py markers <transcript.json>`.
3. Group the user's turns into concepts and record misconceptions, following the
   rubric. Write `concepts.json` next to the transcript.
4. Run `python scripts/struggle_score.py score <transcript.json> <concepts.json>`.

Use the script's numbers as they are. Do not adjust a score by hand; if it looks
wrong, the grouping is wrong, so fix `concepts.json` and rerun.

**If Python cannot run** (no code execution in this app, or the script fails):
do not skip struggle detection. Score each concept by hand with the "Manual
scoring" section of `references/struggle-rubric.md`, show the learner the
signal table you used, and say the score is unverified. Set `Struggle score`
and `Re-ask count` as usual, and add "Scored by hand, not by script" as a gray
line at the end of the note so later metrics can tell the two apart.

### 3. Confirm with the user

In one message, list each flagged concept with its evidence and ask "stuck, or
just exploring?" (wording in the rubric). In the same message say the detailed
note with diagrams is always written, and ask whether they also want a
Comparison table, Quiz or Flashcards added (default: none).

If nothing is flagged, say so in one line, name the concepts found, and ask
only about the format.

### 4. Write to Notion

Read `references/note-template.md` and find the workspace (see "Finding the
Notion workspace"). Fetch the Learning Log data source before writing so
property names match exactly.

Read the Profile page (`profile_page_id`) for the target role and background,
and `references/role-packs.md` for that role, before writing: the "Apply it
now" section of the note depends on them. If the Profile is empty, write the
section for a general learner, and say once in the report that `profile import`
would make it personal.

Before creating anything, query the Learning Log for a row with the same or a
very similar `Topic`. If one exists, the learner is revisiting it: update that
row instead of creating a second one. Add a `## Revisited <date>` section to
its page with what is new, merge any new stuck concepts into Weak Spots
(reopen a resolved one if the learner is stuck on it again), and create
Practice Bank rows only for questions the topic does not already have. Logging
the same chat twice must not duplicate anything.

Write one Learning Log row per topic the conversation was about. A chat on one
topic gives one row; group closely related concepts under that topic rather than
making a row per concept. A separate topic touched only in passing (asked once,
not flagged) gets no row of its own: mention it in one gray line at the end of
the note, and offer to log it separately if the user wants.

- Properties: `Topic`, `Date learned` (today), `Format`, `Struggle score` (the
  highest score among its concepts), `Re-ask count` (sum), `Flag verdict`,
  `Style used` (the first style used; Plain language first unless the chat
  clearly used another), `Styles tried`,
  `Minutes to log`, `Source tool`, `Next review` (tomorrow, per
  `references/review-schedule.md`), `Review count` 0, `Teach-back result` Not
  attempted. Leave `Confidence`, `Last reviewed` and `Applied` empty; the user
  sets confidence and applied, and `review` sets the rest. Also set `Area`
  (one or two broad subjects, such as Python, SQL, Spark, Testing), `Source
  type` (Chat, Article, Course) and `Source link` when there is one.
- Body: the full detailed note from the template, with its "Picture it"
  visual, the "Apply it now" section, and the extra format if one was chosen.

The learner will not always remember to practice, so create the practice
records now instead of waiting for a `practice` command:

- One Practice Bank row per interview question in "Apply it now", related to
  the topic: `Type` Interview, `Difficulty`, `Role`, `Status` Ready, `Result`
  Not attempted, and 2 or 3 `Key points` a correct answer must contain.
- One Practice Bank row for the 30-minute drill: `Type` Scenario.
- One Project Ideas row for the mini-project: `Status` Suggested.

For each concept the user confirmed as stuck, also create a Weak Spots row
related to the Learning Log row: `Question trail`, `Misconception`, `What
clicked`, `Rule to remember`, `Flagged on` today, `Status` Open,
`Delayed teach-back` Not yet, `Next review` tomorrow (the first delayed
teach-back), `Review count` 0.

### 5. Report

Reply with the Notion link, the number of weak spots recorded, and the minutes
it took. Then offer exactly one next step, because the learner should not have
to remember what comes after a note:

- If a weak spot was recorded: "Want to try the 30-minute drill now? Your
  delayed teach-back is due tomorrow."
- Otherwise: "Want to try one of the interview questions now?"
- If the Learning Log "Due today" view has topics due, add one line: "You also
  have <n> reviews due. Say 'review' to do them."

Keep the whole reply under six lines.

## Proactive help

Learners forget the next step, so the skill reminds them. Whenever this skill
is loaded:

- If the conversation looks like the end of learning a topic (the learner says
  "got it", "makes sense", "thanks" after an explanation) and nothing was
  logged yet, offer once: "Want me to log this in Notion?" Do not log without
  a yes.
- At the start of a `teach`, `log this` or `practice` command, check the "Due
  today" and "Open weak spots" views once per conversation and mention the
  counts in one line if they are above zero.

These offers only happen once the skill has loaded. For reminders in every
chat, tell the learner to add this line to their Claude app preferences
(Settings, Profile, personal preferences): "When I finish learning a topic,
offer to log it with the learnloop skill."

## Command: profile import

When the learner shares a resume (PDF or Word), LinkedIn profile text, a
portfolio link or describes their background, read `references/teaching-styles.md`
for the Profile fields, then:

1. Extract only facts that are in the material: roles and years, skills,
   projects, target roles. Do not infer seniority, achievements or numbers.
2. Show the extracted fields to the learner in one message and ask them to
   confirm or correct, and to name their target role and default teaching
   style if those are missing.
3. After confirmation, write them to the Profile page. Keep resume text out of
   the page except short phrases the learner approves.
4. If the target role has no pack in `references/role-packs.md`, follow its
   "Any other role" section.

## Privacy

Transcripts can contain personal details. Keep temp files in a temp or scratch
folder, never in this skill folder, and do not paste the full transcript into
Notion; quote only the turns the note needs.
