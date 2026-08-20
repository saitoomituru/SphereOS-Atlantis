'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = path.resolve(__dirname, '..');

test('VS Code commandとdependencyなしHarness契約を公開する', () => {
  const packageJson = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'));
  const commands = packageJson.contributes.commands.map((entry) => entry.command);

  assert.ok(commands.includes('spheredosCode.openCockpit'));
  assert.equal(packageJson.main, './src/extension.js');
  assert.equal(packageJson.dependencies, undefined);
  assert.equal(packageJson.devDependencies, undefined);
});

test('testと生成物をextension packageから除外する', () => {
  const ignore = fs.readFileSync(path.join(root, '.vscodeignore'), 'utf8');
  assert.match(ignore, /node_modules\/\*\*/);
  assert.match(ignore, /tests\/\*\*/);
  assert.doesNotMatch(ignore, /fixtures\/\*\*/);
});

test('Webviewはnonce付きCSPを宣言する', () => {
  const panelSource = fs.readFileSync(path.join(root, 'src', 'cockpit-panel.js'), 'utf8');

  assert.match(panelSource, /Content-Security-Policy/);
  assert.match(panelSource, /default-src 'none'/);
  assert.match(panelSource, /script-src 'nonce-\$\{nonce\}'/);
  assert.match(panelSource, /crypto\.randomBytes/);
});
