# Processes

Sources: AGENTS.md ("Working one step at a time", "Session-level rules", "Git");
INSTRUCTIONS.md §3, §8, §8b, §8c, §8e.

## Step cadence (AGENTS.md)

1. One Synverk card at a time (project key PC). Read the card (and flow, if any) first.
   Where the card and `docs/plans/` disagree, the card wins: say so.
2. Test it yourself; fix obvious errors before handing off.
3. Keep a running list of anything else noticed; flag it, don't silently fix or skip.
4. Hand off in plain language with a "You can test it yourself" section: exact commands
   and what to check for each (§3).
5. Paste check output as a card comment, move the card to review, wait for the
   owner's explicit approval. The agent never approves its own card.
6. Log the step in that day's `.memory/` file.

## Commits (AGENTS.md "Git")

- One commit per approved unit of work (one card, or an explicitly batched group such as PC-2 + PC-3),
  made only after approval, then pushed to `origin`.
- Subject under 72 chars, conventional style (`chore(setup): ...`), self-explanatory. No essay bodies.
- Covers only this commit's diff; never re-lists earlier work.
- No co-author or "generated with" lines for the agent, ever.
- Merging into `main`, force-pushing, tagging, deleting: confirm first, every time.

## New rules from the user (AGENTS.md, replaces §8)

- Add the rule to the invariants doc that owns the topic (not AGENTS.md, not INSTRUCTIONS.md).
- Log it in that day's `.memory/` file under "Rule changes": what, why, how to revert.

## README (§8c)

- Update `README.md` on every step before handoff: new capabilities, file paths, commands.
  Every commit carries an up-to-date README.

## Plans (§8b)

- Only when the user asks for one: deep dive first, then one plan split into small, testable,
  numbered steps (What / Why / How / Verification / Files / Dependencies / Common issues),
  saved under `docs/plans/`. On this project the Synverk cards are the plan.

## `.memory/` daily log (§8e)

- Path: `.memory/<dd-month-yyyy>/tasks.md`, one file per day, appended in order. Git-ignored, never shared publicly.
- Date in words (**21 October 2026**). Times taken from `date` at the moment of writing, never guessed:
  `5:54 PM (UTC+05:00 · 12:54 UTC)`. Command: `date '+%-I:%M %p (UTC%:z'; date -u '+· %H:%M UTC)'`.
- Updated on every chat turn that changes something.
- Layout:

  ```markdown
  # Tasks · 21 October 2026

  <one-line day verdict>

  **Summary: X done · Y approved · Z changed**

  | # | Time | Card | What changed (reversible detail: files, names) | Status |
  | - | ---- | ---- | ---------------------------------------------- | ------ |
  | 1 | 5:51 PM (UTC+05:00 · 12:51 UTC) | PC-1 | ... | ✅ Approved / 🔄 In progress / 👀 In review / ⚠️ Needs changes |

  ## Rule changes
  | Changed in (doc + section) | Why / trigger | To revert |

  ## Flags
  - running list of things noticed but not done
  ```
