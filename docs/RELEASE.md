# Release readiness

This is a release preparation record. The project is not published and this
workspace does not currently have a Git repository or remote.

## Prepared

- User-facing overview and setup guidance: `README.md`.
- Skill, local scripts, reference schemas, Codex/Claude/Gemini adapters, an
  OpenAI skill manifest, and a paste-in prompt.
- Local Notion configuration is excluded by `.gitignore`.
- Transcript fixture directory and generated Python bytecode are excluded.
- Open validation gates and assumptions are tracked in GitHub Issues.
- Metrics definitions and minimum sample sizes are in
  `learnloop/references/metrics-plan.md`.
- The runbook for the next validation step is in `TESTING.md`; its local
  script checks pass, and the real-session and learner-data checks are open.
- `tools/package_skill.py` validates and builds the upload zip; use `--public`
  so the zip leaves out `config.local.json`.

## Scope comparison checked 2026-10-23

- OpenAI's `notion-knowledge-capture` skill structures conversation material
  in Notion. The project here adds a learner-confirmed struggle workflow and a
  learning-to-application loop.
- `generic-tutor` provides topic tutoring, spaced repetition, interview drills,
  and job-gap integration; `tutor-skills` generates an Obsidian study vault and
  quizzes against it. These are adjacent projects with different storage and
  workflows.
- This comparison supports only a description of scope. It does not establish
  uniqueness, adoption, or user demand.

References:

- [OpenAI Notion knowledge capture](https://github.com/openai/skills/tree/main/skills/.curated/notion-knowledge-capture)
- [generic-tutor](https://github.com/alienz-dev/generic-tutor)
- [tutor-skills](https://github.com/bevibing/tutor-skills)
- [Vercel Skills command documentation](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)
- [Gemini CLI context files](https://geminicli.com/docs/cli/gemini-md/)
- [OpenAI skills guide](https://developers.openai.com/api/docs/guides/tools-skills)

## Before a public release

1. Create or identify the intended public GitHub repository and confirm the
   license and attribution.
2. Review tracked files and remove any personal data, transcript exports,
   private Notion IDs, and generated caches.
3. Validate installation and activation in fresh Codex and Gemini CLI sessions;
   check ChatGPT skill installation and Notion connectivity in the intended
   environment.
4. Complete the real-chat baseline and parser checks in `TESTING.md`.
5. Choose a license and add its exact text; no license is assumed here.
5a. Attach the
   `--public` zip (`learnloop-public.zip`) to a GitHub release, and run `npx skills add surbhi-bhor/learnloop-skill`
   in a fresh machine or account to confirm it finds `learnloop/` and that
   first use finds or creates the Notion workspace without a config file.
6. Publish only after these checks and the release destination are confirmed.
