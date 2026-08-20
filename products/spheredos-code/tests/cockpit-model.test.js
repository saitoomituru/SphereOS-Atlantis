'use strict';

const assert = require('node:assert/strict');
const path = require('node:path');
const test = require('node:test');

const { projectFixture, renderProjectionHtml } = require('../src/cockpit-model');
const { FixtureTransport } = require('../src/fixture-transport');

const root = path.resolve(__dirname, '..');
const transport = new FixtureTransport(root);

function rowValue(projection, sectionTitle, rowLabel) {
  const section = projection.sections.find((item) => item.title === sectionTitle);
  return section?.rows.find((row) => row.label === rowLabel)?.value;
}

test('preparedはprovider exit 0でもOAE commitへ昇格しない', () => {
  const projection = projectFixture(transport.load('prepared'));

  assert.equal(projection.tone, 'pending');
  assert.equal(projection.summary.oaeState, 'prepared');
  assert.equal(projection.summary.effectApplied, 'false');
  assert.equal(rowValue(projection, 'Provider', 'exit code'), '0');
  assert.equal(rowValue(projection, 'OAE Transaction', 'committed'), 'false');
  assert.equal(rowValue(projection, 'Task / Lease', 'Issue state'), 'closed');
  assert.equal(rowValue(projection, 'Task / Lease', 'Mission state'), 'unknown');
});

test('Cockpit必須sectionとGUI authority境界をprojectionする', () => {
  const projection = projectFixture(transport.load('prepared'));
  const titles = projection.sections.map((item) => item.title);

  assert.deepEqual(titles, [
    'Coordinate',
    'World / Fold',
    'Task / Lease',
    'Kernel Decision',
    'Provider',
    'OAE Transaction',
    'Receipt / Provenance',
    'GUI Transport / Recovery',
    'Authority Boundaries'
  ]);
  assert.equal(rowValue(projection, 'Authority Boundaries', 'GUI is OAE authority'), 'false');
  assert.equal(
    rowValue(projection, 'Authority Boundaries', 'GUI is durable state canonical store'),
    'false'
  );
});

test('HTML projectionはfixture名と状態sectionを描画する', () => {
  const projection = projectFixture(transport.load('prepared'));
  const html = renderProjectionHtml(projection);

  assert.match(html, /status-pending/);
  assert.match(html, /OAE Transaction/);
  assert.match(html, /Receipt \/ Provenance/);
});
