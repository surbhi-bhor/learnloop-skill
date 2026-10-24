# LearnLoop

LearnLoop turns learning conversations into a durable practice loop: capture
the explanation, identify confirmed weak spots, connect concepts to role
requirements, practice retrieval, and review later in Notion.

## What is included

- A portable agent skill in `learnloop/` for teaching, capture, role
  reality, practice, spaced review, and job description checks.
- Transcript parsing and struggle-signal scripts using Python's standard
  library.
- Codex, Claude Code, and Gemini CLI project adapters, an OpenAI skill manifest,
  plus a paste-in prompt for chat surfaces that cannot load a skill.
- Notion schemas and templates for a Learning Log, Weak Spots, Reality Cards,
  Practice Bank, Project Ideas, Evidence Ledger, and Skill Map.

The project has been exercised against a synthetic example. Its scoring rubric,
cross-tool activation, export parsers, and learner-specific style choices still
need validation with real conversations. Role examples are hypotheses until
checked against target job descriptions.

## What `log this` gives you

One command turns the current chat into a Notion study note with: a 30-second
summary, a "Picture it" diagram or visual table, the full explanation with
worked examples, a "Where I got stuck" box
for confirmed weak spots, check-yourself questions with hidden answers, and an
"Apply it now" section (where the topic shows up in your target role,
interview questions, a 30-minute drill, a mini-project, a teach-back prompt).
It also saves the questions to a Practice Bank, the project to Project Ideas,
sets the first review for tomorrow, and offers the next step. Logging the same
topic again updates the note instead of duplicating it.

Run `profile import` once with your resume or LinkedIn text so notes are
personal. Role packs cover data engineering, BI, software, QA/SDET and AI/ML
engineering, with a fallback for any other role.

## Install (any agent)

You need two things: the skill in your agent, and Notion connected to that
agent. No file needs editing. On first use, the skill looks for a
`LearnLoop` page in your Notion and offers to create it if there is none.

| Agent | Install the skill | Connect Notion |
|---|---|---|
| Claude app (web, desktop) | Download `learnloop-public.zip` from [Releases](https://github.com/surbhi-bhor/learnloop-skill/releases). Settings, Capabilities: turn on code execution, upload the zip under Skills | Settings, Connectors, Notion |
| Claude Code | `npx skills add surbhi-bhor/learnloop-skill -a claude-code -g`, or copy `learnloop/` to `~/.claude/skills/` | `claude mcp add --transport http notion https://mcp.notion.com/mcp` |
| Codex | `npx skills add surbhi-bhor/learnloop-skill -a codex -g`, or copy `learnloop/` to your Codex skills folder | Add the Notion MCP server in Codex settings |
| Gemini CLI, Cursor, others | `npx skills add surbhi-bhor/learnloop-skill` and pick your agent | Add the Notion MCP server (`https://mcp.notion.com/mcp`) in that agent |
| ChatGPT or Gemini web | No skill install: paste `learnloop/references/paste-in-prompt.md` into the chat | Notion connector if the app has one; otherwise you get the note in the chat |

Then say "set up learnloop" once (creates the Notion workspace), "profile
import" with your resume (personalizes notes), and after learning anything,
"log this in notion".

Skill folders differ between agent versions; `npx skills add` handles that.
Without Python the skill still works and scores struggle by hand.

## Use in this workspace

Open this folder in a supported coding assistant. The adapters are `AGENTS.md`
for Codex, `CLAUDE.md` for Claude Code, and `GEMINI.md` for Gemini CLI. Ask to
learn a concept, save the current conversation, practice, review, or compare a
supplied job description. Read `learnloop/SKILL.md` for the full workflow.

## Use in the Claude app

1. Build the upload file from the project root: `python tools/package_skill.py`.
   It checks the frontmatter, description length and file encoding, then writes
   `dist/learnloop.zip`. That zip includes `config.local.json`, so keep it
   private; `--public` builds one without it.
2. In the Claude app, open Settings, Capabilities: turn on code execution, then
   upload the zip under Skills and enable it.
3. Connect Notion under Settings, Connectors, using the same Notion account as
   the configured workspace.
4. In a chat, learn a topic and say "log this in notion".

The uploaded skill is a copy. Rebuild and re-upload after every change.

For a chat surface without skill loading, paste
[`learnloop/references/paste-in-prompt.md`](learnloop/references/paste-in-prompt.md)
into the learning conversation.

## Setup

The skill's `setup` workflow creates the private Notion parent page, Profile,
databases, relations, and views. Notion must be connected to the assistant.
Workspace IDs are stored in the ignored local file
`learnloop/config.local.json`; do not share or publish that file.

Scripts require Python 3.11+ and use only the standard library. The local
metrics reporter reads an explicit aggregate JSON bundle and never connects to
Notion; see `learnloop/references/metrics-plan.md` for its schema.

## Privacy and evidence

Conversation transcripts can contain personal information. Keep them local and
only capture the turns needed for a note. Never invent learner history,
achievements, metrics, or job requirements. Keep resume evidence in Draft until
the learner confirms it.

## Project status

Project documents are in `docs/`: [`baseline-log.md`](docs/baseline-log.md) holds the
real-chat baseline used to measure capture accuracy,
[`TESTING.md`](docs/TESTING.md) is the test checklist, and
[`RELEASE.md`](docs/RELEASE.md) is the release checklist.

## Development

```
python -m pytest -q                      # script tests
python tools/package_skill.py --public   # build dist/learnloop-public.zip
```


## License

MIT. See [`LICENSE`](LICENSE).
