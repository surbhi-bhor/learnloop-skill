# LearnLoop adapter

For learning requests in this project, read `learnloop/SKILL.md` and
follow its command for teaching, capture, job reality, practice, review, or
job-description checks. Use the active conversation as the source unless the
user explicitly provides an imported transcript. Do not require an export of
the current chat.

For requests to save learning to Notion, read the skill before searching or
writing in Notion. Find the workspace as the skill describes:
`learnloop/config.local.json` if present, otherwise the `LearnLoop`
page in Notion. Ask about flagged struggle concepts before writing the note. If Notion
tools are unavailable, create the note locally and say it was not written to
Notion.

Notion access comes from this tool's own Notion MCP connection, not from Claude's connector. If no Notion tools are listed in this session, say so and point the user to connecting the official Notion MCP server for this tool before writing anything.
