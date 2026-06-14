# Task Management

Use this reference when the user asks about tasks, wants to add or complete
tasks, or needs help tracking commitments.

## File Location

Use `TASKS.md` in the current working directory unless the user gives another
workspace path.

- If it exists, read it before editing.
- If it does not exist, create it with the template below.

## TASKS.md Template

```markdown
# Tasks

## Active

## Waiting On

## Someday

## Done
```

## Task Format

Use Markdown checkboxes:

```markdown
- [ ] **Task title** - context, for whom, due date
  - Optional supporting detail
- [x] ~~Completed task title~~ - completed YYYY-MM-DD
```

Conventions:

- Bold the task title for scanning.
- Include "for [person]" when the task is a commitment to someone.
- Include "due [date]" for deadlines.
- Include "since [date]" for waiting items.
- Use sub-bullets for context, links, or constraints.
- Keep recent completed work in `Done`; old completed tasks can be archived or
  removed after checking with the user.

## Common Interactions

When the user asks "what's on my plate" or "my tasks":

1. Read `TASKS.md`.
2. Summarize `Active` and `Waiting On`.
3. Highlight overdue or urgent tasks.
4. Mention any tasks with unclear owner, due date, or project context.

When the user says "add a task" or "remind me to":

1. Add it to `Active`.
2. Preserve any provided person, project, deadline, source link, or reason.
3. If the task contains unknown shorthand, read `references/memory.md` and fill
   memory gaps after asking the user.

When the user says "done with X" or "finished X":

1. Find the matching task.
2. Change `[ ]` to `[x]`.
3. Add strikethrough around the title.
4. Add the completion date.
5. Move it to `Done`.

When the user asks "what am I waiting on":

1. Read `Waiting On`.
2. Report each item and how long it has been waiting when dates are available.
3. Suggest follow-ups only when they are clearly useful.

## Extracting Tasks

When summarizing meetings, chat threads, docs, or notes, offer to add:

- Commitments the user made.
- Action items assigned to the user.
- Follow-ups with named owners or dates.
- Review, approval, or delivery requests.

Ask before adding inferred tasks. If the user explicitly asks to capture all
action items, add them and report the changes.
