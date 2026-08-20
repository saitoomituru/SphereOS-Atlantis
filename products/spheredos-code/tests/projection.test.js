'use strict';

const assert = require('node:assert/strict');
const path = require('node:path');
const test = require('node:test');

const {
  DISPLAY_NOT_PROVIDED,
  DISPLAY_UNKNOWN,
  projectFixture,
  renderProjectionHtml
} = require('../src/cockpit-model');
const { FixtureTransport } = require('../src/fixture-transport');

const transport = new FixtureTransport(path.resolve(__dirname, '..'));

function rowValue(projection, sectionTitle, rowLabel) {
  const section = projection.sections.find((item) => item.title === sectionTitle);
  return section?.rows.find((row) => row.label === rowLabel)?.value;
}

test('Kernel rejectを成功toneまたはEffect適用へ変換しない', () => {
  const projection = projectFixture(transport.load('kernel-rejected'));
  const html = renderProjectionHtml(projection);

  assert.equal(projection.tone, 'rejected');
  assert.equal(projection.summary.kernelDecision, 'rejected');
  assert.equal(projection.summary.effectApplied, 'false');
  assert.equal(rowValue(projection, 'Kernel Decision', 'reason'), 'lease-missing');
  assert.doesNotMatch(html, /status-success/);
});

test('provider auth要求をchat回答またはMission failureへ偽装しない', () => {
  const projection = projectFixture(transport.load('provider-auth-required'));

  assert.equal(projection.tone, 'control');
  assert.equal(rowValue(projection, 'Provider', 'process state'), 'provider-interaction');
  assert.equal(rowValue(projection, 'Provider', 'control state'), 'auth-required');
  assert.equal(rowValue(projection, 'Provider', 'chat response'), DISPLAY_NOT_PROVIDED);
  assert.equal(rowValue(projection, 'Task / Lease', 'Mission state'), 'pending-provider-interaction');
  assert.notEqual(rowValue(projection, 'Task / Lease', 'Mission state'), 'failure');
});

test('disconnectをabortまたはデータ消失確定へ変換しない', () => {
  const projection = projectFixture(transport.load('disconnected-recoverable'));

  assert.equal(projection.tone, 'recoverable');
  assert.equal(projection.summary.transportState, 'disconnected');
  assert.equal(projection.summary.taskState, 'recoverable');
  assert.equal(rowValue(projection, 'OAE Transaction', 'aborted'), 'false');
  assert.equal(rowValue(projection, 'GUI Transport / Recovery', 'persisted'), 'unknown');
  assert.equal(
    rowValue(projection, 'GUI Transport / Recovery', 'durable state owner'),
    'spheredos-server-candidate'
  );
});

test('detected・registered・approved・dispatchableを独立表示する', () => {
  const projection = projectFixture(transport.load('kernel-rejected'));

  assert.equal(rowValue(projection, 'Provider', 'detected'), 'true');
  assert.equal(rowValue(projection, 'Provider', 'registered'), 'true');
  assert.equal(rowValue(projection, 'Provider', 'approved'), 'false');
  assert.equal(rowValue(projection, 'Provider', 'dispatchable'), 'false');
});

test('missing fieldをpass・success・committedで補完しない', () => {
  const projection = projectFixture({
    fixtureName: 'missing-fields',
    transport: 'test',
    payload: {}
  });

  assert.equal(projection.tone, 'unknown');
  assert.equal(projection.summary.kernelDecision, DISPLAY_UNKNOWN);
  assert.equal(projection.summary.oaeState, DISPLAY_UNKNOWN);
  assert.equal(projection.summary.effectApplied, DISPLAY_UNKNOWN);
  assert.equal(rowValue(projection, 'Provider', 'chat response'), DISPLAY_NOT_PROVIDED);
});

test('fixture由来HTMLとscriptをescapeする', () => {
  const projection = projectFixture({
    fixtureName: 'escape-probe',
    transport: 'test',
    payload: {
      coordinate: {
        function_series: '<img src=x onerror=alert(1)>',
        presentation: '<script>alert(1)</script>'
      }
    }
  });
  const html = renderProjectionHtml(projection);

  assert.doesNotMatch(html, /<script>/);
  assert.doesNotMatch(html, /<img /);
  assert.match(html, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
  assert.match(html, /&lt;img src=x onerror=alert\(1\)&gt;/);
});
