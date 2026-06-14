# Connectors

Use this reference when a workflow can benefit from external context, such as
chat, email, calendar, documents, or project trackers.

## Connector Model

This skill is tool-agnostic. It describes source categories rather than
requiring a specific vendor.

| Category | Examples | Useful for |
| --- | --- | --- |
| Chat | Slack, Microsoft Teams, Discord | Recent context, decisions, action items, nicknames |
| Email | Microsoft 365, Gmail | Formal commitments, announcements, follow-ups |
| Calendar | Microsoft 365, Google Calendar | Meetings, attendees, upcoming obligations |
| Knowledge base | Notion, Confluence, Guru, Coda | Project docs, policies, definitions |
| Project tracker | Asana, Linear, Jira, monday.com, ClickUp | Assigned work, status, owners, due dates |
| Code host | GitHub, GitLab | Issues, pull requests, reviews, milestones |

## How To Use Sources

Before scanning, identify which tools are available in the current environment.
If no connector is available, continue with local files and user-provided
content.

When using connected sources:

- Preserve source links when available.
- Search multiple relevant sources in parallel when the tool environment allows
  it.
- Do not let one failed source block the entire update.
- Explain which sources were checked.
- Ask before writing inferred tasks or memories.

## Source Priority

For current task status, prefer project trackers and recent direct messages.

For decisions, prefer official docs, final design documents, or announcement
emails over mid-thread chat messages.

For shorthand, nicknames, and project codenames, chat and task titles are often
the richest sources, but ask the user when meaning is ambiguous.

For people profiles, use repeated evidence across meetings, messages, and docs.
Avoid storing sensitive personal information that is not needed for work.
