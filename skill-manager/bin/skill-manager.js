#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { execFile } from 'node:child_process';
import { constants as fsConstants } from 'node:fs';
import {
  access,
  cp,
  lstat,
  mkdir,
  mkdtemp,
  readFile,
  readdir,
  rm,
  symlink,
  writeFile,
} from 'node:fs/promises';
import { homedir, tmpdir } from 'node:os';
import {
  basename,
  dirname,
  isAbsolute,
  join,
  relative,
  resolve,
  sep,
} from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const VERSION = '0.1.0';
const LOCAL_LOCK_FILE = 'skills-lock.json';
const GLOBAL_LOCK_FILE = '.skill-lock.json';
const GLOBAL_LOCK_VERSION = 3;
const LOCAL_LOCK_VERSION = 1;

const home = homedir();
const xdgConfig = process.env.XDG_CONFIG_HOME || join(home, '.config');
const xdgState = process.env.XDG_STATE_HOME || null;
const codexHome = process.env.CODEX_HOME?.trim() || join(home, '.codex');
const claudeHome = process.env.CLAUDE_CONFIG_DIR?.trim() || join(home, '.claude');

const AGENTS = {
  universal: {
    displayName: 'Universal',
    projectDir: '.agents/skills',
    globalDir: join(home, '.agents', 'skills'),
  },
  codex: {
    displayName: 'Codex',
    projectDir: '.agents/skills',
    globalDir: join(codexHome, 'skills'),
  },
  'claude-code': {
    displayName: 'Claude Code',
    projectDir: '.claude/skills',
    globalDir: join(claudeHome, 'skills'),
  },
  cursor: {
    displayName: 'Cursor',
    projectDir: '.agents/skills',
    globalDir: join(home, '.cursor', 'skills'),
  },
  'gemini-cli': {
    displayName: 'Gemini CLI',
    projectDir: '.gemini/skills',
    globalDir: join(home, '.gemini', 'skills'),
  },
  opencode: {
    displayName: 'OpenCode',
    projectDir: '.opencode/skills',
    globalDir: join(xdgConfig, 'opencode', 'skills'),
  },
  amp: {
    displayName: 'Amp',
    projectDir: '.agents/skills',
    globalDir: join(xdgConfig, 'agents', 'skills'),
  },
  'github-copilot': {
    displayName: 'GitHub Copilot',
    projectDir: '.agents/skills',
    globalDir: join(home, '.github-copilot', 'skills'),
  },
  goose: {
    displayName: 'Goose',
    projectDir: '.config/goose/skills',
    globalDir: join(xdgConfig, 'goose', 'skills'),
  },
  windsurf: {
    displayName: 'Windsurf',
    projectDir: '.windsurf/skills',
    globalDir: join(home, '.windsurf', 'skills'),
  },
  zed: {
    displayName: 'Zed',
    projectDir: '.zed/skills',
    globalDir: join(home, '.config', 'zed', 'skills'),
  },
};

const HELP = `Usage: skill-manager <command> [options]

Commands:
  add <source>          Install skills from a git repo or local path
  use <source>          Print one skill's SKILL.md without installing
  list, ls              List installed skills
  find [query]          Search installed skill locks
  remove, rm <skills>   Remove installed skills
  check [skills...]     Check installed skills for updates
  update [skills...]    Update installed skills (alias: upgrade)
  init [dir]            Create a starter SKILL.md
  doctor                Verify local prerequisites

Common add options:
  -g, --global          Install globally instead of into this project
  -a, --agent <agent>   Target agent: codex, claude-code, cursor, universal, ...
  -s, --skill <name>    Install a specific skill; use "*" for all
  --all                 Install all discovered skills
  --copy                Copy files (default; accepted for skills compatibility)
  --symlink             Symlink installed skill folders
  -y, --yes             Non-interactive confirmation
  --full-depth          Search the full repository for SKILL.md files
  -l, --list            Show discovered skills without installing
  -p, --project         Limit update/check/list/remove to project scope
  --json                Emit JSON

Sources:
  owner/repo
  github:owner/repo
  gitlab:group/subgroup/repo
  https://git.example.com/group/repo.git#branch
  git@git.example.com:group/repo.git#branch
  https://gitlab.example.com/group/repo/-/tree/main/skills/foo
  /local/path/to/skills
`;

class CliError extends Error {
  constructor(message, code = 1) {
    super(message);
    this.code = code;
  }
}

function mainArgs(argv) {
  return argv.slice(2);
}

async function main(argv = process.argv) {
  const args = mainArgs(argv);
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log(HELP);
    return;
  }
  if (args[0] === '--version' || args[0] === '-v') {
    console.log(VERSION);
    return;
  }

  const leadingOptions = [];
  while (args[0] === '--json') {
    leadingOptions.push(args.shift());
  }

  const command = args.shift();
  args.push(...leadingOptions);
  switch (command) {
    case 'add':
    case 'a':
    case 'install':
      await commandAdd(args);
      break;
    case 'use':
      await commandUse(args);
      break;
    case 'list':
    case 'ls':
      await commandList(args);
      break;
    case 'find':
      await commandFind(args);
      break;
    case 'remove':
    case 'rm':
      await commandRemove(args);
      break;
    case 'check':
      await commandUpdate(args, { dryRun: true });
      break;
    case 'update':
    case 'upgrade':
      await commandUpdate(args, { dryRun: false });
      break;
    case 'init':
      await commandInit(args);
      break;
    case 'doctor':
      await commandDoctor(args);
      break;
    case 'experimental_install':
      await commandRestore(args);
      break;
    default:
      throw new CliError(`Unknown command: ${command}\n\n${HELP}`);
  }
}

function parseOptions(args, spec = {}) {
  const positionals = [];
  const options = {
    agents: [],
    skills: [],
    json: false,
    global: false,
    yes: false,
    copy: false,
    symlink: false,
    all: false,
    list: false,
    fullDepth: false,
    project: false,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--') {
      positionals.push(...args.slice(i + 1));
      break;
    }
    if (arg === '-g' || arg === '--global') {
      options.global = true;
    } else if (arg === '-p' || arg === '--project') {
      options.project = true;
    } else if (arg === '-y' || arg === '--yes') {
      options.yes = true;
    } else if (arg === '--json') {
      options.json = true;
    } else if (arg === '--copy') {
      options.copy = true;
    } else if (arg === '--symlink') {
      options.symlink = true;
    } else if (arg === '--all') {
      options.all = true;
      options.skills.push('*');
      options.agents.push('*');
      options.yes = true;
    } else if (arg === '-l' || arg === '--list') {
      options.list = true;
    } else if (arg === '--full-depth') {
      options.fullDepth = true;
    } else if (arg === '-a' || arg === '--agent') {
      const value = args[++i];
      if (!value) throw new CliError(`Missing value for ${arg}`);
      options.agents.push(...value.split(',').filter(Boolean));
    } else if (arg.startsWith('--agent=')) {
      options.agents.push(...arg.slice('--agent='.length).split(',').filter(Boolean));
    } else if (arg === '-s' || arg === '--skill') {
      const value = args[++i];
      if (!value) throw new CliError(`Missing value for ${arg}`);
      options.skills.push(value);
    } else if (arg.startsWith('--skill=')) {
      options.skills.push(arg.slice('--skill='.length));
    } else if (arg === '--force') {
      options.force = true;
    } else if (arg === '--silent') {
      options.silent = true;
    } else if (arg.startsWith('-') && !spec.allowUnknown) {
      throw new CliError(`Unknown option: ${arg}`);
    } else {
      positionals.push(arg);
    }
  }

  return { positionals, options };
}

async function commandDoctor(args) {
  const { options } = parseOptions(args);
  const git = await commandExists('git');
  const nodeOk = Number(process.versions.node.split('.')[0]) >= 18;
  const result = {
    ok: git && nodeOk,
    version: VERSION,
    node: process.versions.node,
    git,
    lockFiles: {
      local: join(process.cwd(), LOCAL_LOCK_FILE),
      global: getGlobalLockPath(),
    },
    supportedAgents: Object.keys(AGENTS),
  };
  if (options.json) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }
  console.log(`skill-manager ${VERSION}`);
  console.log(`node: ${result.node}`);
  console.log(`git: ${git ? 'found' : 'missing'}`);
  console.log(`local lock: ${result.lockFiles.local}`);
  console.log(`global lock: ${result.lockFiles.global}`);
  if (!result.ok) throw new CliError('doctor failed');
}

async function commandAdd(args) {
  const { positionals, options } = parseOptions(args);
  const sourceInput = positionals[0];
  if (!sourceInput) throw new CliError(`Missing required argument: source\n\n${HELP}`);

  const resolved = await resolveSource(sourceInput);
  const workspace = await materializeSource(resolved);
  try {
    const discovered = await discoverSkills(workspace.root, {
      subpath: resolved.subpath,
      fullDepth: options.fullDepth,
    });
    const selected = selectSkills(discovered, {
      requested: [...options.skills, ...(resolved.skillFilter ? [resolved.skillFilter] : [])],
      all: options.all || options.skills.includes('*'),
      yes: options.yes,
    });

    if (options.list) {
      return outputSkills(selected.length ? selected : discovered, options.json);
    }

    if (selected.length === 0) {
      throw new CliError(`No skills found in ${sourceInput}`);
    }

    const agents = resolveAgents(options.agents);
    const scope = options.global ? 'global' : 'project';
    const lockUpdates = [];

    for (const skill of selected) {
      for (const agent of agents) {
        const destination = getInstallDir(agent, scope, skill.name);
        if (options.symlink && workspace.kind === 'local') {
          await installSymlink(skill.path, destination);
        } else {
          await installCopy(skill.path, destination);
        }
      }

      const skillPath = toPosix(join(relative(workspace.root, skill.path), 'SKILL.md'));
      const hash = await computeFolderHash(skill.path);
      const entry = {
        source: resolved.lockSource,
        sourceType: resolved.type,
        sourceUrl: resolved.url,
        ref: resolved.ref,
        skillPath,
        skillFolderHash: hash,
        computedHash: hash,
      };
      if (scope === 'global') {
        await addGlobalLock(skill.name, entry);
      } else {
        await addLocalLock(skill.name, entry);
      }
      lockUpdates.push({ name: skill.name, hash, skillPath });
    }

    if (options.silent) {
      return;
    }
    if (options.json) {
      console.log(JSON.stringify({ installed: lockUpdates, scope, agents }, null, 2));
      return;
    }
    console.log(`Installed ${selected.length} skill${selected.length === 1 ? '' : 's'} for ${agents.join(', ')}`);
  } finally {
    await workspace.cleanup();
  }
}

async function commandUse(args) {
  const { positionals, options } = parseOptions(args);
  const sourceInput = positionals[0];
  if (!sourceInput) throw new CliError('Missing required argument: source');
  const resolved = await resolveSource(sourceInput);
  const workspace = await materializeSource(resolved);
  try {
    const discovered = await discoverSkills(workspace.root, {
      subpath: resolved.subpath,
      fullDepth: options.fullDepth,
    });
    const selected = selectSkills(discovered, {
      requested: [...options.skills, ...(resolved.skillFilter ? [resolved.skillFilter] : [])],
      all: options.all,
      yes: options.yes,
    });
    if (selected.length !== 1) {
      const names = discovered.map((skill) => skill.name).join(', ');
      throw new CliError(`Select exactly one skill with --skill. Available: ${names}`);
    }
    const skillMd = join(selected[0].path, 'SKILL.md');
    const content = await readFile(skillMd, 'utf8');
    if (options.json) {
      console.log(JSON.stringify({ skill: selected[0], content }, null, 2));
    } else {
      console.log(content);
    }
  } finally {
    await workspace.cleanup();
  }
}

async function commandList(args) {
  const { options } = parseOptions(args);
  const scope = options.global ? 'global' : options.project ? 'project' : 'both';
  const rows = [];
  if (scope === 'project' || scope === 'both') {
    const lock = await readLocalLock();
    for (const [name, entry] of Object.entries(lock.skills)) {
      rows.push({ name, scope: 'project', ...entry });
    }
  }
  if (scope === 'global' || scope === 'both') {
    const lock = await readGlobalLock();
    for (const [name, entry] of Object.entries(lock.skills)) {
      rows.push({ name, scope: 'global', ...entry });
    }
  }
  if (options.json) {
    console.log(JSON.stringify({ skills: rows }, null, 2));
    return;
  }
  if (rows.length === 0) {
    console.log('No installed skills tracked in lock files.');
    return;
  }
  for (const row of rows.sort((a, b) => `${a.scope}:${a.name}`.localeCompare(`${b.scope}:${b.name}`))) {
    const ref = row.ref ? `#${row.ref}` : '';
    console.log(`${row.scope.padEnd(7)} ${row.name.padEnd(28)} ${row.source}${ref}`);
  }
}

async function commandFind(args) {
  const { positionals, options } = parseOptions(args, { allowUnknown: true });
  const query = normalizeName(positionals.join(' '));
  const rows = [];
  const local = await readLocalLock();
  const global = await readGlobalLock();
  for (const [name, entry] of Object.entries(local.skills)) rows.push({ name, scope: 'project', ...entry });
  for (const [name, entry] of Object.entries(global.skills)) rows.push({ name, scope: 'global', ...entry });
  const matches = rows.filter((row) => {
    if (!query) return true;
    return [row.name, row.source, row.skillPath].some((value) => normalizeName(value || '').includes(query));
  });
  if (options.json) {
    console.log(JSON.stringify({ skills: matches }, null, 2));
    return;
  }
  if (matches.length === 0) {
    console.log('No matching installed skills. Registry-backed skills.sh search is not implemented.');
    return;
  }
  for (const row of matches) {
    console.log(`${row.scope.padEnd(7)} ${row.name.padEnd(28)} ${row.source}`);
  }
}

async function commandRemove(args) {
  const { positionals, options } = parseOptions(args);
  const skills = positionals.length ? positionals : options.skills;
  if (skills.length === 0) throw new CliError('Missing skill name to remove');
  const agents = resolveAgents(options.agents);
  const scopes = await resolveUpdateScopes(options);
  const removed = [];

  for (const skill of skills) {
    for (const scope of scopes) {
      for (const agent of agents) {
        await rm(getInstallDir(agent, scope, skill), { recursive: true, force: true });
      }
      if (scope === 'global') {
        if (await removeGlobalLock(skill)) removed.push({ skill, scope });
      } else if (await removeLocalLock(skill)) {
        removed.push({ skill, scope });
      }
    }
  }
  if (options.json) {
    console.log(JSON.stringify({ removed }, null, 2));
  } else {
    console.log(`Removed ${removed.length} lock entr${removed.length === 1 ? 'y' : 'ies'}.`);
  }
}

async function resolveUpdateScopes(options) {
  if (options.global) return ['global'];
  if (options.project) return ['project'];
  const localLock = await readLocalLock();
  if (Object.keys(localLock.skills).length > 0) return ['project'];
  return ['global'];
}

async function commandUpdate(args, { dryRun }) {
  const { positionals, options } = parseOptions(args);
  const requested = new Set([...positionals, ...options.skills].filter(Boolean));
  const scopes = options.global ? ['global'] : options.project ? ['project'] : ['project', 'global'];
  const updates = [];
  const checked = [];
  const skipped = [];

  for (const scope of scopes) {
    const lock = scope === 'global' ? await readGlobalLock() : await readLocalLock();
    for (const [name, entry] of Object.entries(lock.skills)) {
      if (requested.size > 0 && !requested.has(name)) continue;
      if (!entry.skillPath) {
        skipped.push({ name, scope, reason: 'missing skillPath in lock entry' });
        continue;
      }
      try {
        const source = entry.sourceUrl || entry.source;
        const resolved = await resolveSource(source, { ref: entry.ref, lockSource: entry.source });
        const workspace = await materializeSource(resolved);
        try {
          const skillDir = join(workspace.root, dirname(entry.skillPath));
          await assertPath(skillDir);
          const latestHash = await computeFolderHash(skillDir);
          const currentHash = entry.computedHash || entry.skillFolderHash;
          const changed = latestHash !== currentHash;
          checked.push({ name, scope, changed });
          if (changed) {
            updates.push({ name, scope, entry, latestHash, source: resolved });
          }
        } finally {
          await workspace.cleanup();
        }
      } catch (error) {
        skipped.push({ name, scope, reason: error.message });
      }
    }
  }

  if (!dryRun) {
    for (const update of updates) {
      await reinstallLockedSkill(update, options);
    }
  }

  if (options.json) {
    console.log(JSON.stringify({ dryRun, checked, updates, skipped }, null, 2));
    return;
  }
  if (updates.length === 0) {
    console.log('All checked skills are up to date.');
  } else if (dryRun) {
    for (const update of updates) {
      console.log(`${update.scope} ${update.name} has an update`);
    }
  } else {
    console.log(`Updated ${updates.length} skill${updates.length === 1 ? '' : 's'}.`);
  }
  if (skipped.length > 0) {
    for (const item of skipped) {
      console.error(`Skipped ${item.scope} ${item.name}: ${item.reason}`);
    }
  }
}

async function reinstallLockedSkill(update, options) {
  const args = [update.entry.sourceUrl || update.entry.source, '--skill', update.name, '-y', '--silent'];
  if (update.scope === 'global') args.push('-g');
  if (update.entry.ref) args[0] = `${args[0]}#${update.entry.ref}`;
  await commandAdd(args);
}

async function commandRestore(args) {
  const { options } = parseOptions(args);
  const lock = await readLocalLock();
  const entries = Object.entries(lock.skills);
  if (entries.length === 0) {
    console.log('No project skills found in skills-lock.json');
    return;
  }
  for (const [name, entry] of entries) {
    const source = entry.ref ? `${entry.source}#${entry.ref}` : entry.source;
    await commandAdd([source, '--skill', name, '-y', ...(options.global ? ['-g'] : [])]);
  }
}

async function commandInit(args) {
  const { positionals, options } = parseOptions(args);
  const targetDir = resolve(positionals[0] || '.');
  await mkdir(targetDir, { recursive: true });
  const name = sanitizeSkillName(basename(targetDir) || 'new-skill');
  const file = join(targetDir, 'SKILL.md');
  const content = `---\nname: ${name}\ndescription: Describe when this skill should be used.\n---\n\n# ${name}\n\nUse this skill when ...\n\n## Workflow\n\n1. Gather the relevant context.\n2. Follow the project-specific instructions.\n3. Verify the result before finishing.\n`;
  await writeFile(file, content, { flag: 'wx' });
  if (options.json) {
    console.log(JSON.stringify({ created: file }, null, 2));
  } else {
    console.log(`Created ${file}`);
  }
}

function resolveAgents(requested) {
  const values = requested.length === 0 ? ['codex'] : requested;
  if (values.includes('*')) return Object.keys(AGENTS);
  for (const agent of values) {
    if (!AGENTS[agent]) {
      throw new CliError(`Unsupported agent: ${agent}. Supported: ${Object.keys(AGENTS).join(', ')}`);
    }
  }
  return [...new Set(values)];
}

function getInstallDir(agentName, scope, skillName) {
  const agent = AGENTS[agentName];
  const base = scope === 'global' ? agent.globalDir : join(process.cwd(), agent.projectDir);
  return join(base, sanitizeSkillName(skillName));
}

function selectSkills(discovered, { requested, all, yes }) {
  if (discovered.length === 0) return [];
  const cleanRequested = requested.filter(Boolean);
  if (all || cleanRequested.includes('*')) return discovered;
  if (cleanRequested.length > 0) {
    const normalized = new Set(cleanRequested.map(normalizeName));
    const selected = discovered.filter((skill) => {
      return normalized.has(normalizeName(skill.name)) || normalized.has(normalizeName(basename(skill.path)));
    });
    const missing = cleanRequested.filter((name) => {
      return !selected.some((skill) => normalizeName(skill.name) === normalizeName(name) || normalizeName(basename(skill.path)) === normalizeName(name));
    });
    if (missing.length > 0) throw new CliError(`Skill not found: ${missing.join(', ')}`);
    return selected;
  }
  if (discovered.length === 1) return discovered;
  if (yes) return discovered;
  const names = discovered.map((skill) => skill.name).join(', ');
  throw new CliError(`This source contains multiple skills. Specify --skill <name> or --all. Available: ${names}`);
}

function outputSkills(skills, json) {
  if (json) {
    console.log(JSON.stringify({ skills }, null, 2));
  } else {
    for (const skill of skills) {
      console.log(`${skill.name}\t${skill.description || ''}\t${skill.path}`);
    }
  }
}

async function resolveSource(input, overrides = {}) {
  const parsed = parseSource(input);
  const ref = overrides.ref || parsed.ref;
  const lockSource = overrides.lockSource || parsed.lockSource || inputWithoutSelector(input);
  if (parsed.type === 'local') {
    return { ...parsed, ref, lockSource: parsed.url };
  }
  return {
    ...parsed,
    ref,
    lockSource,
  };
}

function inputWithoutSelector(input) {
  const hash = input.indexOf('#');
  const base = hash >= 0 ? input.slice(0, hash) : input;
  const atSkill = base.match(/^([^/]+\/[^/@]+)@(.+)$/);
  return atSkill ? atSkill[1] : base;
}

function parseSource(input) {
  const { base, ref, skillFilter } = splitRefAndSkill(input);
  input = base;

  if (isLocalPath(input)) {
    return { type: 'local', url: resolve(input), localPath: resolve(input), ref, skillFilter };
  }

  const githubPrefix = input.match(/^github:(.+)$/);
  if (githubPrefix) return parseSource(`${githubPrefix[1]}${formatFragment(ref, skillFilter)}`);

  const gitlabPrefix = input.match(/^gitlab:(.+)$/);
  if (gitlabPrefix) return parseSource(`https://gitlab.com/${gitlabPrefix[1]}${formatFragment(ref, skillFilter)}`);

  const atSkill = input.match(/^([^/]+)\/([^/@]+)@(.+)$/);
  if (atSkill && !input.includes(':')) {
    return {
      type: 'git',
      url: `https://github.com/${atSkill[1]}/${atSkill[2]}.git`,
      ref,
      skillFilter: skillFilter || atSkill[3],
      lockSource: `${atSkill[1]}/${atSkill[2]}`,
    };
  }

  const githubTree = input.match(/^https?:\/\/github\.com\/([^/]+)\/([^/]+)\/tree\/([^/]+)(?:\/(.+))?\/?$/);
  if (githubTree) {
    return {
      type: 'git',
      url: `https://github.com/${githubTree[1]}/${githubTree[2].replace(/\.git$/, '')}.git`,
      ref: ref || githubTree[3],
      subpath: githubTree[4] ? sanitizeSubpath(githubTree[4]) : undefined,
      skillFilter,
      lockSource: `https://github.com/${githubTree[1]}/${githubTree[2].replace(/\.git$/, '')}`,
    };
  }

  const gitlabTree = input.match(/^(https?):\/\/([^/]+)\/(.+?)\/-\/tree\/([^/]+)(?:\/(.+))?\/?$/);
  if (gitlabTree) {
    return {
      type: 'git',
      url: `${gitlabTree[1]}://${gitlabTree[2]}/${gitlabTree[3].replace(/\.git$/, '')}.git`,
      ref: ref || gitlabTree[4],
      subpath: gitlabTree[5] ? sanitizeSubpath(gitlabTree[5]) : undefined,
      skillFilter,
      lockSource: `${gitlabTree[1]}://${gitlabTree[2]}/${gitlabTree[3].replace(/\.git$/, '')}`,
    };
  }

  const bitbucketTree = input.match(/^(https?):\/\/bitbucket\.org\/([^/]+)\/([^/]+)\/src\/([^/]+)(?:\/(.+))?\/?$/);
  if (bitbucketTree) {
    return {
      type: 'git',
      url: `${bitbucketTree[1]}://bitbucket.org/${bitbucketTree[2]}/${bitbucketTree[3].replace(/\.git$/, '')}.git`,
      ref: ref || bitbucketTree[4],
      subpath: bitbucketTree[5] ? sanitizeSubpath(bitbucketTree[5]) : undefined,
      skillFilter,
      lockSource: `${bitbucketTree[1]}://bitbucket.org/${bitbucketTree[2]}/${bitbucketTree[3].replace(/\.git$/, '')}`,
    };
  }

  const giteaTree = input.match(/^(https?):\/\/([^/]+)\/([^/]+)\/([^/]+)\/src\/(?:branch|tag)\/([^/]+)(?:\/(.+))?\/?$/);
  if (giteaTree) {
    return {
      type: 'git',
      url: `${giteaTree[1]}://${giteaTree[2]}/${giteaTree[3]}/${giteaTree[4].replace(/\.git$/, '')}.git`,
      ref: ref || giteaTree[5],
      subpath: giteaTree[6] ? sanitizeSubpath(giteaTree[6]) : undefined,
      skillFilter,
      lockSource: `${giteaTree[1]}://${giteaTree[2]}/${giteaTree[3]}/${giteaTree[4].replace(/\.git$/, '')}`,
    };
  }

  const shorthand = input.match(/^([^/:\s]+)\/([^/\s]+)(?:\/(.+))?\/?$/);
  if (shorthand) {
    return {
      type: 'git',
      url: `https://github.com/${shorthand[1]}/${shorthand[2]}.git`,
      ref,
      subpath: shorthand[3] ? sanitizeSubpath(shorthand[3]) : undefined,
      skillFilter,
      lockSource: `${shorthand[1]}/${shorthand[2]}`,
    };
  }

  if (input.startsWith('git@') || input.startsWith('ssh://') || input.endsWith('.git')) {
    return { type: 'git', url: input, ref, skillFilter };
  }

  if (input.startsWith('http://') || input.startsWith('https://')) {
    return { type: 'git', url: `${input.replace(/\/$/, '')}.git`, ref, skillFilter, fallbackUrl: input };
  }

  return { type: 'git', url: input, ref, skillFilter };
}

function splitRefAndSkill(input) {
  const hashIndex = input.indexOf('#');
  if (hashIndex < 0) return { base: input };
  const base = input.slice(0, hashIndex);
  const fragment = input.slice(hashIndex + 1);
  if (!fragment) return { base: input };
  const atIndex = fragment.indexOf('@');
  if (atIndex < 0) return { base, ref: decode(fragment) };
  return {
    base,
    ref: fragment.slice(0, atIndex) ? decode(fragment.slice(0, atIndex)) : undefined,
    skillFilter: fragment.slice(atIndex + 1) || undefined,
  };
}

function formatFragment(ref, skillFilter) {
  if (!ref && !skillFilter) return '';
  return `#${ref || ''}${skillFilter ? `@${skillFilter}` : ''}`;
}

function decode(value) {
  try {
    return decodeURIComponent(value);
  } catch {
    return value;
  }
}

function isLocalPath(input) {
  return isAbsolute(input) || input === '.' || input === '..' || input.startsWith('./') || input.startsWith('../') || /^[a-zA-Z]:[/\\]/.test(input);
}

function sanitizeSubpath(subpath) {
  const normalized = subpath.replace(/\\/g, '/');
  if (normalized.split('/').includes('..')) {
    throw new CliError(`Unsafe subpath: ${subpath}`);
  }
  return normalized;
}

async function materializeSource(source) {
  if (source.type === 'local') {
    await assertPath(source.localPath);
    return { kind: 'local', root: source.localPath, cleanup: async () => {} };
  }
  const dir = await mkdtemp(join(tmpdir(), 'skill-manager-'));
  try {
    await cloneGit(source.url, dir, source.ref);
  } catch (error) {
    if (source.fallbackUrl) {
      await rm(dir, { recursive: true, force: true });
      const fallbackDir = await mkdtemp(join(tmpdir(), 'skill-manager-'));
      await cloneGit(source.fallbackUrl, fallbackDir, source.ref);
      return { kind: 'git', root: fallbackDir, cleanup: () => rm(fallbackDir, { recursive: true, force: true }) };
    }
    await rm(dir, { recursive: true, force: true });
    throw error;
  }
  return { kind: 'git', root: dir, cleanup: () => rm(dir, { recursive: true, force: true }) };
}

async function cloneGit(url, target, ref) {
  const args = ['clone', '--depth', '1'];
  if (ref) args.push('--branch', ref);
  args.push(url, target);
  await execFileAsync('git', args, {
    env: {
      ...process.env,
      GIT_TERMINAL_PROMPT: '0',
      GIT_LFS_SKIP_SMUDGE: '1',
    },
    timeout: Number(process.env.SKILL_MANAGER_CLONE_TIMEOUT_MS || 300000),
  });
}

async function discoverSkills(root, { subpath, fullDepth } = {}) {
  const base = subpath ? join(root, subpath) : root;
  await assertPath(base);
  const results = [];

  if (await isFile(join(base, 'SKILL.md'))) {
    results.push(await readSkill(base));
    return results;
  }

  const likelyContainers = ['', 'skills', '.agents/skills', '.codex/skills', 'agents/skills', 'plugins'];
  for (const container of likelyContainers) {
    const dir = container ? join(base, container) : base;
    if (!(await isDirectory(dir))) continue;
    await collectSkillDirs(dir, results, { maxDepth: container ? 4 : 2 });
  }

  if (results.length === 0 || fullDepth) {
    await collectSkillDirs(base, results, { maxDepth: fullDepth ? 10 : 5 });
  }

  const unique = new Map();
  for (const skill of results) {
    unique.set(resolve(skill.path), skill);
  }
  return [...unique.values()].sort((a, b) => a.name.localeCompare(b.name));
}

async function collectSkillDirs(dir, results, { maxDepth }, depth = 0) {
  if (depth > maxDepth) return;
  if (await isFile(join(dir, 'SKILL.md'))) {
    results.push(await readSkill(dir));
    return;
  }
  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    if (['.git', 'node_modules', 'dist', 'build', '.next', '.turbo'].includes(entry.name)) continue;
    await collectSkillDirs(join(dir, entry.name), results, { maxDepth }, depth + 1);
  }
}

async function readSkill(skillDir) {
  const content = await readFile(join(skillDir, 'SKILL.md'), 'utf8');
  const frontmatter = parseFrontmatter(content);
  const name = sanitizeSkillName(frontmatter.name || basename(skillDir));
  return {
    name,
    description: frontmatter.description || '',
    path: skillDir,
  };
}

function parseFrontmatter(content) {
  if (!content.startsWith('---\n')) return {};
  const end = content.indexOf('\n---', 4);
  if (end < 0) return {};
  const raw = content.slice(4, end).split('\n');
  const result = {};
  for (const line of raw) {
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (match) result[match[1]] = match[2].replace(/^['"]|['"]$/g, '').trim();
  }
  return result;
}

async function installCopy(sourceDir, destination) {
  await rm(destination, { recursive: true, force: true });
  await mkdir(dirname(destination), { recursive: true });
  await cp(sourceDir, destination, {
    recursive: true,
    filter: (src) => !src.split(sep).some((part) => ['.git', 'node_modules'].includes(part)),
  });
}

async function installSymlink(sourceDir, destination) {
  await rm(destination, { recursive: true, force: true });
  await mkdir(dirname(destination), { recursive: true });
  await symlink(sourceDir, destination, 'dir');
}

async function computeFolderHash(skillDir) {
  const files = [];
  await collectFiles(skillDir, skillDir, files);
  files.sort((a, b) => a.relativePath.localeCompare(b.relativePath));
  const hash = createHash('sha256');
  for (const file of files) {
    hash.update(file.relativePath);
    hash.update(file.content);
  }
  return hash.digest('hex');
}

async function collectFiles(baseDir, currentDir, files) {
  let entries;
  try {
    entries = await readdir(currentDir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const entry of entries) {
    const fullPath = join(currentDir, entry.name);
    if (entry.isDirectory()) {
      if (['.git', 'node_modules'].includes(entry.name)) continue;
      await collectFiles(baseDir, fullPath, files);
    } else if (entry.isFile()) {
      files.push({
        relativePath: toPosix(relative(baseDir, fullPath)),
        content: await readFile(fullPath),
      });
    }
  }
}

async function readLocalLock() {
  return readJsonLock(join(process.cwd(), LOCAL_LOCK_FILE), { version: LOCAL_LOCK_VERSION, skills: {} });
}

async function writeLocalLock(lock) {
  await writeJsonLock(join(process.cwd(), LOCAL_LOCK_FILE), lock);
}

async function addLocalLock(name, entry) {
  const lock = await readLocalLock();
  lock.version = LOCAL_LOCK_VERSION;
  lock.skills[name] = compact({
    source: entry.source,
    ref: entry.ref,
    sourceType: entry.sourceType,
    skillPath: entry.skillPath,
    computedHash: entry.computedHash,
  });
  await writeLocalLock(lock);
}

async function removeLocalLock(name) {
  const lock = await readLocalLock();
  const existed = Boolean(lock.skills[name]);
  delete lock.skills[name];
  if (existed) await writeLocalLock(lock);
  return existed;
}

function getGlobalLockPath() {
  if (xdgState) return join(xdgState, 'skills', GLOBAL_LOCK_FILE);
  return join(home, '.agents', GLOBAL_LOCK_FILE);
}

async function readGlobalLock() {
  return readJsonLock(getGlobalLockPath(), { version: GLOBAL_LOCK_VERSION, skills: {} });
}

async function writeGlobalLock(lock) {
  await writeJsonLock(getGlobalLockPath(), lock);
}

async function addGlobalLock(name, entry) {
  const lock = await readGlobalLock();
  lock.version = GLOBAL_LOCK_VERSION;
  const now = new Date().toISOString();
  const existing = lock.skills[name];
  lock.skills[name] = compact({
    source: entry.source,
    sourceType: 'git',
    sourceUrl: entry.sourceUrl,
    ref: entry.ref,
    skillPath: entry.skillPath,
    skillFolderHash: entry.skillFolderHash,
    installedAt: existing?.installedAt || now,
    updatedAt: now,
  });
  await writeGlobalLock(lock);
}

async function removeGlobalLock(name) {
  const lock = await readGlobalLock();
  const existed = Boolean(lock.skills[name]);
  delete lock.skills[name];
  if (existed) await writeGlobalLock(lock);
  return existed;
}

async function readJsonLock(file, empty) {
  try {
    const parsed = JSON.parse(await readFile(file, 'utf8'));
    if (!parsed || typeof parsed !== 'object' || !parsed.skills) return structuredClone(empty);
    return parsed;
  } catch {
    return structuredClone(empty);
  }
}

async function writeJsonLock(file, lock) {
  const sorted = { ...lock, skills: {} };
  for (const key of Object.keys(lock.skills || {}).sort()) {
    sorted.skills[key] = compact(lock.skills[key]);
  }
  await mkdir(dirname(file), { recursive: true });
  await writeFile(file, `${JSON.stringify(sorted, null, 2)}\n`, 'utf8');
}

function compact(object) {
  return Object.fromEntries(Object.entries(object).filter(([, value]) => value !== undefined));
}

function sanitizeSkillName(name) {
  return String(name || 'skill')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9._-]+/g, '-')
    .replace(/^-+|-+$/g, '') || 'skill';
}

function normalizeName(name) {
  return sanitizeSkillName(name);
}

function toPosix(path) {
  return path.split(sep).join('/');
}

async function assertPath(path) {
  try {
    await access(path, fsConstants.F_OK);
  } catch {
    throw new CliError(`Path does not exist: ${path}`);
  }
}

async function isFile(path) {
  try {
    return (await lstat(path)).isFile();
  } catch {
    return false;
  }
}

async function isDirectory(path) {
  try {
    return (await lstat(path)).isDirectory();
  } catch {
    return false;
  }
}

async function commandExists(cmd) {
  try {
    await execFileAsync(cmd, ['--version'], { timeout: 5000 });
    return true;
  } catch {
    return false;
  }
}

function isCliEntrypoint() {
  if (!process.argv[1]) return false;
  const invoked = resolve(process.argv[1]);
  const modulePath = fileURLToPath(import.meta.url);
  return invoked === modulePath || ['skill-manager', 'skill-manager.js'].includes(basename(invoked));
}

if (isCliEntrypoint()) {
  main().catch((error) => {
    const code = error instanceof CliError ? error.code : 1;
    const wantsJson = process.argv.includes('--json');
    if (wantsJson) {
      console.error(JSON.stringify({ error: error.message }, null, 2));
    } else {
      console.error(error.message);
    }
    process.exit(code);
  });
}

export {
  parseSource,
  discoverSkills,
  computeFolderHash,
  sanitizeSkillName,
  selectSkills,
};
