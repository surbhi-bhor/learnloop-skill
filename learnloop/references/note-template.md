# Note template

The note is a real study note on the topic, not a summary of the chat. A chat
is usually a trail of partial answers; the user should be able to open the note
weeks later and learn the topic from it without rereading the conversation. Use
the chat as the spine (what they asked, where they got stuck, the examples that
worked) and fill the gaps a learner needs to understand the topic properly.

Make the topic itself understandable. Do not leave the page as a list of what
the chat said or questions about what the learner should research next. Explain
the key mechanism and include a worked example with its result. Fill essential
gaps with established facts, marking each added section or bullet "Beyond the
chat" as described below. If a topic is too broad for one useful note, narrow
it to the topic actually discussed and state the scope.

Keep it tight: complete, not long. A small topic may need one screen; a large
one more. Cut anything that does not help the user understand or use the topic.

Write in Notion-flavored Markdown. Do not repeat the topic as a heading at the
top; it is the page title. Notion saves ordinary HTML tags such as `<details>`
as literal text, so use only the Notion tags shown here (`<callout>`,
`<toggle>`, `<span color>`).

## Flagged topic (user confirmed "Stuck")

The stuck block goes first, because it is the most useful part of the note when
the user comes back.

```markdown
<callout icon="🧱" color="red_bg">
**Where I got stuck**

- **My question trail:** <the user's questions on this concept, quoted briefly, in order>
- **Misconception:** <what the user believed, quoted, and why it is wrong>. Leave out if none.
- **What finally clicked:** <the explanation or example after which the questions stopped>
- **Rule to remember:** <one sentence>
</callout>

<callout icon="🔁" color="yellow_bg">
**Asked before** (only when "Seen before" found a repeat; one line per repeat)

- **<concept>:** you asked this on <date> in <link to that Learning Log page>.
  Times stuck: <n>. Last time, what clicked: "<What clicked from that row>".
  This time, what was different: <one line>.
</callout>

<callout icon="⚡" color="blue_bg">
**In 30 seconds:** <the whole idea in 2 or 3 plain sentences>

**Why it matters for <target role>:** <one sentence>
</callout>

## Key idea
<2 to 4 sentences in plain words: what it is and why it matters>

## Picture it
<always include at least one visual; see "Visual aids" below. One line under
it saying what to notice in the picture.>

## How it works
<the mechanism, step by step. For code topics: plain words first, then a code
snippet with its real output under it, one idea per snippet. For concepts: a
concrete worked example with real-looking data. Add a second visual here when
a step is easier to see than to read, such as a before/after table.>

## When to use it, and when not
<the decision: which situations call for it, the alternatives, the trade-off>

## Gotchas
- <common mistakes and edge cases, max 4>

## Check yourself
1. <a question with no story or analogy in it, testing the idea itself>
2. <a "what happens if" question>
3. <an applied question on a realistic case>

<toggle>
Answers

1. ...
2. ...
3. ...
</toggle>

## Apply it now

<callout icon="🎯" color="green_bg">
**Where this shows up in <target role>:** <2 or 3 concrete tasks on the job,
from the Profile and role pack, tied to the learner's past roles where the
Profile supports it. Put <span color="gray">Beyond the chat</span> in front of
each task the chat did not discuss; this is required, not optional.>
</callout>

**In production**

- **How teams actually use it:** <the common real-world setup, and how often
  it is used compared with simpler alternatives. Say when a simpler option is
  usually enough, for example at the learner's project scale.>
- **What breaks:** <one realistic failure, told as a short incident:
  symptom, cause, how it was found, the fix. Label it "Typical scenario", not
  a real case, unless the chat or a source describes a real one.>
- **How you would notice:** <the check, alert, test or metric that catches
  the failure early, such as a row-count reconciliation or freshness alert.>

Mark every line here "Beyond the chat" unless the chat covered it. Claims
about how common a practice is need a cited source when browsing is
available; otherwise add "(unverified)" after the claim. For more depth,
offer a `reality` card.

**Interview questions** (also saved to the Practice Bank)

| # | Question | Difficulty | Why <role> asks it |
|---|---|---|---|
| 1 | ... | Foundational | ... |
| 2 | ... | Intermediate | ... |
| 3 | ... | Advanced | ... |

**30-minute drill for today:** <one small task on realistic data, with what
"done" looks like>

**Mini-project:** <one project that uses the topic and, when the Profile names
a portfolio project, extends it; 1 to 3 sentences>

**Teach it back:** <one prompt asking the learner to explain the idea in their
own words; graded later by `practice`>

## Cheat sheet

<a short table or list of the syntax, commands or rules worth remembering;
skip it for purely conceptual topics>
```

## Normal topic

Same as above without the "Where I got stuck" block.

## Visual aids

Every note has a "Picture it" section, because many learners understand a
picture faster than a paragraph and recognize it faster when reviewing. Pick
the visual that matches the shape of the idea:

| The idea is... | Use |
|---|---|
| A process or pipeline | mermaid `flowchart LR` |
| Messages between parts (client, server, database) | mermaid `sequenceDiagram` |
| Something that changes state (retry, job status) | mermaid `stateDiagram-v2` |
| Tables and keys, data models | mermaid `erDiagram` |
| Classes or object structure | mermaid `classDiagram` |
| A comparison of options | a table with one column per option |
| Data before and after an operation | two small tables, "Before" and "After" |
| Memory, indexes, positions (lists, arrays, pointers) | a text diagram in a code block, such as `[10][20][30]` with index labels under it |
| A broad topic with sub-ideas | a mermaid `flowchart TD` concept map, the topic at the top |

Rules for visuals:

- Use fenced `mermaid` code blocks; Notion renders them as diagrams. Keep each
  diagram under about 12 nodes with short labels, so it stays readable.
- A text diagram goes in a plain code block or one tagged `text`, never a
  programming language such as `javascript`, which colors it as code. Use a
  text diagram only for memory and positions; data moving between machines
  (executors, partitions, consumers) is a process, so draw it in mermaid.
- The visual must show the real mechanism with real-looking values, not
  decoration. If an analogy is used, label the diagram with the real terms.
- When the learner was stuck, draw the visual around the exact point of
  confusion, for example the step where a retry duplicates rows.
- Use mermaid syntax that renders on its own: quote labels that contain
  brackets, parentheses or colons, such as `A["load(day=1)"]`.
- If the output will not be rendered (plain chat with no Markdown), keep the
  mermaid block anyway and add the text-diagram version under it.

## Extra formats

The full note above is always written, because the learner wants a detailed
note whatever else they pick. A chosen format is added as an extra section
after "Check yourself", not instead of the note:

- **Table**: `## Comparison table`, one table of the concepts (for example list
  vs tuple vs set), with rows for what each is, when to use it, and the cost.
- **Quiz**: `## Quiz`, 5 to 8 questions, mixed recall, "what happens if" and
  applied, answers inside a `<toggle>`.
- **Flashcards**: `## Flashcards`, 8 to 12 cards, each a `<toggle>` whose title
  is the question and whose body is the answer, so the answer stays hidden
  until clicked (a two-column table shows answers at a glance and defeats
  recall). The first line inside the toggle is its title; the answer must come
  before `</toggle>`, or Notion shows it outside the toggle:

  ```
  <toggle>
  Which table is copied to every executor?

  The small side. The big table stays split into partitions.
  </toggle>
  ```

If the learner picks none, write the detailed note only. Set the `Format`
property to the extra format, or Detailed when there is none.

## Formatting rules

- Lead with the 30-second callout so the page is useful even if it is the
  only part read, then the visual, so the shape of the idea comes before the
  detail.
- Put long worked examples inside a `<toggle>` when a section runs past one
  screen, so the page stays easy to scan.
- Use the headings exactly as in the template, so every note has the same
  shape and the learner always knows where to look.

## Rules

- Build the note from the whole conversation, not only the last answer.
- Quote the user's own words in the question trail and misconception. The
  point is to recognize their own confusion later.
- Mark what goes beyond the chat. Put `<span color="gray">Beyond the chat</span>`
  at the start of any section or bullet the conversation did not cover, so the
  user knows which parts they have not actually studied yet. Most notes should
  still be mostly built from the chat.
- Stick to well-established facts when filling gaps. If you are not sure of
  something, leave it out rather than guess; the note becomes a reference the
  user trusts.
- If the chat itself said something wrong, correct it in the note and say
  briefly that the chat's version was wrong.
- If the chat ended before a question was answered, answer it in the note and
  mark it Beyond the chat.
