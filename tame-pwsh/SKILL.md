---
name: tame-pwsh
description: Reliable Windows PowerShell and PowerShell 7 command execution. Use when Codex needs to run, write, debug, or translate shell commands for Windows, PowerShell 5.1, PowerShell 7+, pwsh, CMD interop, npm/dotnet/git CLIs on Windows, paths with spaces, command redirection, environment variables, JSON handling, or repeated shell failures caused by Bash-vs-PowerShell syntax differences.
---

# Tame pwsh

Use this skill to make Windows shell commands boring: detect the shell, choose valid PowerShell syntax, preserve output, and recover from errors by category instead of trying random variants.

## First Checks

Before issuing or rewriting commands:

- Identify the shell: Windows PowerShell 5.1 is `powershell.exe`; PowerShell 7+ is usually `pwsh`.
- If both Windows PowerShell 5.1 and PowerShell 7+ are available, prefer `pwsh` unless the task needs legacy Windows-only modules, old snap-ins, COM-specific behavior, or exact 5.1 reproduction.
- Check `$ExecutionContext.SessionState.LanguageMode` before using .NET-heavy, COM, reflection, inline C#, or custom class patterns.
- Prefer PowerShell-native syntax when the active shell is PowerShell. Do not paste Bash control flow, env vars, redirection assumptions, glob semantics, or command chaining into PowerShell.
- If a command is copied from Bash docs, translate it before running it.
- Keep scripts and generated commands ASCII unless the task explicitly requires Unicode output.
- For multi-step risky commands, write a short `.ps1` and run it with `-NoProfile -ExecutionPolicy Bypass -File` when that is more reliable than dense one-liners.

## Command Construction

Use these patterns by default:

```powershell
# Paths and executables
& "C:\Program Files\Git\bin\git.exe" status
dotnet build "src\My Project\My Project.csproj"
$out = Join-Path $PWD "logs\build.txt"

# Environment variables
$env:NODE_ENV = "test"
npm test
Remove-Item Env:NODE_ENV

# Command sequencing
cmd1; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
cmd2
```

Rules:

- Quote paths that may contain spaces.
- Use `&` before a quoted executable path.
- Use `$env:NAME`, not `$NAME` or `%NAME%`, for PowerShell environment variables.
- Use `Join-Path` for constructed paths.
- Use cmdlets in scripts: `Remove-Item`, `Copy-Item`, `Move-Item`, `New-Item -ItemType Directory`, `Get-Content`, `Set-Content`.
- Use native CLIs directly for tool commands: `git`, `npm`, `node`, `python`, `dotnet`, `cargo`, etc.
- Check native executable failure with `$LASTEXITCODE`; check PowerShell cmdlet failure with exceptions or `$?`.

Use explicit Windows path patterns:

| Pattern | Use |
| --- | --- |
| Literal path | `C:\Users\User\file.txt` |
| Variable path | `Join-Path $env:USERPROFILE "file.txt"` |
| Relative path | `Join-Path $ScriptDir "data"` |

Use predictable array patterns:

```powershell
$items = @()
$items += $item
$list.Add($item) | Out-Null
```

Prefer PowerShell cmdlets over CMD-style built-ins in scripts:

| Action | Avoid CMD style | Use PowerShell |
| --- | --- | --- |
| Delete | `del /f /q file` | `Remove-Item -Force file` |
| Copy | `copy a b` | `Copy-Item a b` |
| Move | `move a b` | `Move-Item a b` |
| Make directory | `mkdir folder` | `New-Item -ItemType Directory -Path folder` |

Using CLI aliases like `ls`, `cat`, and `cp` is usually fine interactively, but full cmdlets are more robust in scripts.

For dotnet on Windows, choose the build mode intentionally:

| Context | Command | Why |
| --- | --- | --- |
| Fast iteration | `dotnet build --no-restore` | Skip redundant NuGet restore after restore already ran. |
| Clean build | `dotnet build --no-incremental` | Avoid stale build artifacts during verification. |
| Background app | `Start-Process dotnet -ArgumentList 'run' -RedirectStandardOutput output.txt -RedirectStandardError error.txt` | Launch without blocking the shell and keep logs. |

Remember environment variable syntax differs by shell:

| Shell | Syntax |
| --- | --- |
| PowerShell | `$env:VARIABLE_NAME` |
| CMD | `%VARIABLE_NAME%` |

## PowerShell Syntax Traps

Wrap command expressions before using logical operators:

```powershell
if ((Test-Path "a.txt") -or (Test-Path "b.txt")) { "found" }
if ((Get-Item $x) -and ($y -eq 5)) { "ok" }
if (($items) -and ($items.Count -gt 0)) { $items.Count }
```

Avoid these common failures:

- Do not write `if (Test-Path "a" -or Test-Path "b")`; PowerShell treats `-or` as a parameter.
- Do not write `if (Get-Item $x -and $y -eq 5)`; each cmdlet call must be parenthesized before logical operators.
- Do not access `.Count`, `.Length`, or nested properties before null-checking the value.
- Do not rely on implicit nested JSON serialization; use `ConvertTo-Json -Depth 10`.
- Do not embed complex property chains inside strings when the result is brittle; assign first, interpolate second.
- Do not `return` from inside a `try` block when cleanup or consistent exit handling matters.

Use this base script shape:

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

try {
    # work
    Write-Output "[OK] Done"
}
catch {
    Write-Warning "Error: $_"
    exit 1
}
finally {
    # cleanup when needed
}

exit 0
```

Choose error action intentionally:

| Value | Use |
| --- | --- |
| `Stop` | Development and fail-fast scripts. |
| `Continue` | Production scripts or best-effort diagnostics. |
| `SilentlyContinue` | Expected errors only, checked afterward. |

Return after `try`/`catch` when possible; use `finally` for cleanup.

Use ASCII status tokens in scripts:

| Purpose | Use |
| --- | --- |
| Success | `[OK]` or `[+]` |
| Error | `[!]` or `[X]` |
| Warning | `[*]` or `[WARN]` |
| Info | `[i]` or `[INFO]` |
| Progress | `[...]` |

## PowerShell 5.1 vs 7+

Treat version differences as a first-class cause of command failures:

```powershell
$PSVersionTable.PSVersion.ToString()
$PSVersionTable.PSEdition
```

PowerShell 5.1:

- Usually means Windows PowerShell running on .NET Framework.
- Redirection and `Out-File` may produce UTF-16LE logs by default.
- Use explicit encoding when files will be read by cross-platform tools:
  `... 2>&1 | Out-File -Encoding utf8 log.txt`
- Some newer operators and cmdlet parameters are unavailable. If syntax fails unexpectedly, check the version before retrying.

PowerShell 7+:

- Usually means `pwsh` running on modern .NET.
- Native stdout redirection preserves bytes more reliably, especially in 7.4+.
- Prefer normal native redirection unless an encoding problem is observed.

Portable file writing:

```powershell
$data | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 "data.json"
Get-Content "data.json" -Raw | ConvertFrom-Json
```

The original Windows PowerShell-compatible JSON file pattern is also valid:

```powershell
Get-Content "file.json" -Raw | ConvertFrom-Json
$data | ConvertTo-Json -Depth 10 | Out-File "file.json" -Encoding UTF8
```

## Constrained Language Mode

Treat Constrained Language Mode as an execution environment constraint, not a syntax bug:

```powershell
$ExecutionContext.SessionState.LanguageMode
```

If the mode is `ConstrainedLanguage`:

- Prefer built-in cmdlets and native executables over .NET object construction.
- Avoid `Add-Type`, inline C#, reflection, custom classes, arbitrary .NET method calls, and COM automation.
- Avoid assuming `New-Object` works for non-core types.
- Replace .NET file/network/process helpers with cmdlets such as `Get-Content`, `Set-Content`, `Invoke-WebRequest`, `Start-Process`, `Get-Process`, and native CLIs.
- Do not try to bypass CLM. Explain that the host is policy-constrained and choose a permitted implementation path.
- If a command works in FullLanguage but fails in ConstrainedLanguage, report that distinction explicitly before retrying.

Other language modes matter too:

- `FullLanguage`: normal PowerShell behavior.
- `RestrictedLanguage` or `NoLanguage`: avoid script logic; use simple cmdlets/native commands or ask for a less restricted host.

## Long Paths

Windows has a 260-character path limit by default in many legacy tool and host combinations.

- Prefer a shorter worktree or temp path first when tools fail with long-path errors.
- Use the extended path prefix only when the target tool supports it:

```powershell
\\?\C:\Very\Long\Path\...
```

## Redirection and Logs

Choose capture patterns intentionally:

```powershell
# Older Windows PowerShell log conversion
dotnet > "log.txt"
Get-Content "log.txt" | Set-Content -Encoding utf8 "log_utf8.txt"

# Text log with stderr included
npm run test 2>&1 | Out-File -Encoding utf8 "test.log"

# Native redirect, best for pwsh 7.4+ when byte preservation matters
dotnet test > "test.log" 2>&1

# Background process with separate logs
Start-Process dotnet -ArgumentList "run" `
  -RedirectStandardOutput "stdout.log" `
  -RedirectStandardError "stderr.log"
```

If a log is unreadable, suspect encoding before rerunning the expensive command. Re-export it:

```powershell
Get-Content "old.log" | Set-Content -Encoding utf8 "old.utf8.log"
```

## Error Recovery

When a command fails, classify before retrying:

- `The term 'x' is not recognized`: verify PATH, command existence, or use an absolute executable path.
- `A parameter cannot be found that matches parameter name 'or'`: wrap each command expression in parentheses before `-or` or `-and`.
- `Unexpected token`: check for Bash syntax, unescaped quotes, unsupported PowerShell-version syntax, Unicode characters, or hidden Unicode characters.
- `Access to the path is denied`: stop the owning process, adjust permissions, or rerun as Admin when appropriate.
- `Cannot find property` or null-member errors: add null checks before property access.
- `Cannot convert`: check for type mismatch and use `.ToString()` only when string conversion is actually intended.
- Encoding or mojibake: distinguish PowerShell 5.1 UTF-16 output from PowerShell 7 UTF-8/native byte behavior.
- Long path failures: use a shorter worktree path first; use `\\?\C:\...` only when a tool supports it.

After two failed attempts, stop varying syntax blindly. Inspect the exact shell, PowerShell version, working directory, executable resolution, and a minimal reproduction command.

## Boundaries

Use environment-specific validation for real hosts. Stop and ask for clarification when required inputs, permissions, safety boundaries, or success criteria are missing.
