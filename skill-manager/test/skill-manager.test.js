import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import test from 'node:test';

import {
  computeFolderHash,
  discoverSkills,
  parseSource,
  sanitizeSkillName,
  selectSkills,
} from '../bin/skill-manager.js';

test('parseSource supports generic ssh git remotes', () => {
  const parsed = parseSource('git@git.example.com:team/skills.git#main');
  assert.equal(parsed.type, 'git');
  assert.equal(parsed.url, 'git@git.example.com:team/skills.git');
  assert.equal(parsed.ref, 'main');
});

test('parseSource supports self-managed GitLab tree URLs', () => {
  const parsed = parseSource('https://gitlab.example.com/group/sub/repo/-/tree/main/skills/backend');
  assert.equal(parsed.url, 'https://gitlab.example.com/group/sub/repo.git');
  assert.equal(parsed.ref, 'main');
  assert.equal(parsed.subpath, 'skills/backend');
});

test('parseSource supports GitHub shorthand skill selectors', () => {
  const parsed = parseSource('owner/repo@backend');
  assert.equal(parsed.url, 'https://github.com/owner/repo.git');
  assert.equal(parsed.skillFilter, 'backend');
  assert.equal(parsed.lockSource, 'owner/repo');
});

test('discoverSkills reads frontmatter names', async () => {
  const root = await mkdtemp(join(tmpdir(), 'skill-manager-test-'));
  const skillDir = join(root, 'skills', 'backend');
  await mkdir(skillDir, { recursive: true });
  await writeFile(
    join(skillDir, 'SKILL.md'),
    '---\nname: backend\ndescription: Backend work\n---\n\n# Backend\n'
  );
  const skills = await discoverSkills(root);
  assert.equal(skills.length, 1);
  assert.equal(skills[0].name, 'backend');
  assert.equal(skills[0].description, 'Backend work');
});

test('folder hash changes when file content changes', async () => {
  const root = await mkdtemp(join(tmpdir(), 'skill-manager-test-'));
  await writeFile(join(root, 'SKILL.md'), '---\nname: one\n---\n');
  const before = await computeFolderHash(root);
  await writeFile(join(root, 'extra.md'), 'changed\n');
  const after = await computeFolderHash(root);
  assert.notEqual(before, after);
});

test('selectSkills requires disambiguation unless all is requested', () => {
  const skills = [
    { name: 'one', path: '/tmp/one' },
    { name: 'two', path: '/tmp/two' },
  ];
  assert.throws(() => selectSkills(skills, { requested: [], all: false, yes: false }));
  assert.equal(selectSkills(skills, { requested: [], all: true, yes: false }).length, 2);
  assert.equal(selectSkills(skills, { requested: ['one'], all: false, yes: false })[0].name, 'one');
});

test('sanitizeSkillName keeps filesystem-safe names', () => {
  assert.equal(sanitizeSkillName('My Skill!'), 'my-skill');
});
