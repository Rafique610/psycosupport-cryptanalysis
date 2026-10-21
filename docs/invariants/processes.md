# Processes

> Draft from AGENTS.md (PC-1). Fill in from INSTRUCTIONS.md after PC-3.

## Step cadence

1. One Synverk card at a time (project key PC). Read the card (and flow, if any) first.
2. Test it yourself; fix obvious errors before handing off.
3. Keep a running list of anything else noticed; flag it, don't silently fix or skip.
4. Hand off in plain language with exact verification commands.
5. Paste check output as a card comment, move the card to review, wait for the
   owner's explicit approval. The agent never approves its own card.
6. Log the step in that day's `.memory/` file.

## Commits

- One commit per approved unit of work, made only after approval, then pushed to `origin`.
- Subject under 72 chars, conventional style (`chore(setup): ...`). No essay bodies.
- No co-author or "generated with" lines for the agent.
- Merging into `main`, force-pushing and tagging need a yes each time.

## `.memory/` daily log

- Path: `.memory/<dd-month-yyyy>/tasks.md` (e.g. `.memory/21-october-2026/tasks.md`). Git-ignored.
- Times: real clock (`date`), 12-hour format with local time zone and UTC.
- Entry format:

  ```markdown
  ## <hh:mm AM/PM TZ> (<HH:MM UTC>) · <card ref>: <card title>
  - Status: in progress | in review | approved
  - Done: <what changed>
  - Notes: <flags, decisions, rule changes (what, why, how to revert)>
  ```

## README

- `README.md` holds the project purpose and a Setup section; update it when setup steps change.

## ADRs

- TODO from INSTRUCTIONS.md.
