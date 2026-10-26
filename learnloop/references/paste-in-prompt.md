# Paste-in prompt for chat apps without skill loading

Paste this into a learning conversation when the app cannot load the
LearnLoop skill automatically:

> Use this conversation as the source. Do not ask me to export the active chat.
> Identify the topic and the explanations or examples that were actually
> covered. If the topic is ambiguous, ask which topic I mean.
>
> Score my struggle by hand, concept by concept. Group my messages by the
> concept they ask about and number them. For each concept, mark each of these
> five signals true or false:
> 1. Repeated: I asked about it 3 or more times, in any wording.
> 2. Simplify: I asked for a simpler explanation, an example or analogy, "like
>    I'm 5", "in layman's terms", "step by step", "break it down", or to explain
>    again.
> 3. Wrong summary: I stated something false as my own understanding (quote it
>    and give the correction).
> 4. Hints: I needed 2 or more hints on a check question (usually false).
> 5. Said stuck: I said "I still don't get it", "I'm confused", "I'm lost", "not
>    following", "doesn't make sense", "I'm stuck", or similar.
>
> Score = number of true signals, capped at 3. Flag a concept when the score is
> 2 or more, or when "Said stuck" is true. Count only what is in my messages;
> if unsure whether a phrase counts, leave the signal false and say so. Show me
> one table: Concept | My messages | Repeated | Simplify | Wrong summary | Hints
> | Said stuck | Score | Flagged. Asking many questions can mean curiosity, so
> before writing anything, ask about all flagged concepts in one message
> whether I was stuck or just exploring. Also
> ask whether I want a Comparison table, Quiz or Flashcards added; the detailed
> note is always written. Then write a complete study note using the
> conversation as its spine. Right after the summary, add a "Picture it"
> section with at least one visual that shows the real mechanism: a mermaid
> diagram (flowchart for a process, sequence diagram for messages, state
> diagram for status changes, ER diagram for tables), a comparison table, or a
> before/after table, plus a plain text diagram under it if mermaid will not
> render here. Draw it around the point where I got stuck, if I did. Then mark added teaching material as "Beyond the chat," and preserve
> only the turns needed for the question trail. For each concept I confirmed as
> stuck, start the note with a "Where I got stuck" box: what confused me, the
> explanation that finally worked, and my wrong summary with its correction.
> End the note with a gray line "Scored by hand, not by script". Save the note to my Learning
> Log if a connected Notion tool and configured database are available. If not,
> give me the finished note here and clearly say it was not saved to Notion.
>
> My target role is: [fill in, for example senior data engineer]. End the note
> with an "Apply it now" section: where this topic shows up in that role; an
> "In production" part with how teams actually use it (and when a simpler
> option is enough), one realistic failure (symptom, cause, fix, labeled as a
> typical scenario) and how you would notice it; 3
> interview questions for that role with difficulty and why they are asked
> (well-known patterns only), a 30-minute drill for today, one mini-project,
> and one teach-back prompt. Then offer me one next step, such as trying the
> drill now.
