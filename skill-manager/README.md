# skill-manager

`skill-manager` is a small, platform-agnostic skill installer inspired by
`vercel-labs/skills`.

The key difference is update detection: this tool never calls the GitHub Trees
API. It checks remote skills by cloning the configured git source and computing
a deterministic SHA-256 hash of the installed skill folder. That makes the
update path work the same way for GitHub, GitHub Enterprise, GitLab.com,
self-managed GitLab, Bitbucket, Gitea, SSH URLs, and ordinary bare git URLs.

## Install

From this repository:

```bash
cd skill-manager
npm link
```

Or run it directly:

```bash
node skill-manager/bin/skill-manager.js --help
```

## Commands

```bash
skill-manager add <source> [options]
skill-manager use <source> [options]
skill-manager list|ls [options]
skill-manager find [query] [options]
skill-manager remove|rm <skill...> [options]
skill-manager check [skill...] [options]
skill-manager update|upgrade [skill...] [options]
skill-manager init [dir]
skill-manager experimental_install
skill-manager doctor
```

Common options accepted for compatibility with `npx skills`:

```text
-g, --global
-a, --agent <agent>
-s, --skill <name>
--all
--copy
--symlink
-y, --yes
--full-depth
-l, --list
-p, --project
--json
```

## Sources

Supported source examples:

```bash
skill-manager add vercel-labs/skills --skill init-project
skill-manager add github:owner/repo#main --all
skill-manager add gitlab:group/subgroup/repo#v1.2.0 --skill linting
skill-manager add https://gitlab.example.com/team/skills.git#main --all
skill-manager add git@git.example.com:team/skills.git#main --skill backend
skill-manager add https://gitlab.example.com/team/skills/-/tree/main/skills/backend
skill-manager add https://bitbucket.org/team/skills/src/main/skills/backend
skill-manager add ./local-skills --all
```

For plain HTTPS repository pages on unknown hosts, `skill-manager` first tries
the `.git` clone URL and falls back to the original URL if needed.

## Lock Files

Project installs write `skills-lock.json` in the current working directory using
the same minimal shape as `vercel-labs/skills` project locks:

```json
{
  "version": 1,
  "skills": {
    "backend": {
      "source": "https://git.example.com/team/skills.git",
      "sourceType": "git",
      "skillPath": "skills/backend/SKILL.md",
      "computedHash": "..."
    }
  }
}
```

Global installs write `.skill-lock.json` under `$XDG_STATE_HOME/skills/` when
set, otherwise under `~/.agents/`.

## Notes

This is intentionally not a clone of the hosted `skills.sh` registry. `find`
and registry-backed discovery are not implemented. The supported surface is the
git and local-path workflow: add, use, list, remove, check, update, init, and
restore from lock files.
