# Comprehensive Scan

Use this reference for deep refreshes that scan recent activity and connected
sources. Also read `references/connectors.md`.

## Purpose

A comprehensive scan catches work that is not already in `TASKS.md` and
discovers people, projects, and terms that should be added to memory.

## Sources

Use only sources that are available in the current environment or provided by
the user:

- Chat messages and channels.
- Email.
- Calendar.
- Documents or knowledge bases.
- Project trackers.
- GitHub issues or pull requests.
- Pasted notes or exported files.

If no connected sources exist, ask the user for pasted notes, exports, or a
local task file.

## Workflow

### 1. Define The Scan Window

Use a sensible default, such as the last 7 days for daily catch-up or the last
30 days for first-time setup. If the user names a timeframe, use that.

### 2. Find Possible Missing Tasks

Look for:

- "I will..." commitments.
- Assigned action items.
- Review requests.
- Follow-up requests.
- Promised deliverables with dates.
- Meeting notes with owners.

Compare findings against `TASKS.md`. Present candidate tasks with source and
ask which to add.

Example:

```text
Possible missing tasks:
1. Review API spec by Friday
   Source: engineering meeting notes, 2026-06-12
   Add to TASKS.md?
```

### 3. Suggest New Memories

Group candidates by confidence:

```text
Ready to add:
- Maya Rodriguez: appears in 12 recent design/API threads
- Starlight: project name in docs and project tracker

Needs clarification:
- QBR: could mean quarterly business review or a team-specific report

Low confidence:
- "green path": mentioned twice, meaning unclear
```

Ask before adding inferred memories. If the user already told the agent to
build memory from the scan, add high-confidence items and mark uncertain details
as "Needs confirmation".

### 4. Clean Up Stale Context

Suggest demotions or cleanup:

- Projects with no mentions in the scan window.
- People no longer appearing in active work.
- Terms that only appear in historical completed tasks.

Do not delete durable history without explicit confirmation. Prefer demoting
from `MEMORY.md` to `memory/`.

### 5. Report Scope And Gaps

Always say which sources were scanned and which were unavailable. This makes the
result easier to trust.

```text
Comprehensive scan complete:
- Sources scanned: chat, calendar, TASKS.md
- Sources unavailable: email, project tracker
- Tasks: 4 candidates found, 2 added
- Memory: 3 people suggested, 1 project updated
```
