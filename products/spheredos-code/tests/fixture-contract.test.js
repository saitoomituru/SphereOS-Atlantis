'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const { FIXTURE_FILES } = require('../src/fixture-transport');

const fixtureRoot = path.resolve(__dirname, '..', 'fixtures');

function load(name) {
  return JSON.parse(fs.readFileSync(path.join(fixtureRoot, FIXTURE_FILES[name]), 'utf8'));
}

test('必須fixtureを固定allowlistで公開する', () => {
  assert.deepEqual(Object.keys(FIXTURE_FILES).sort(), [
    'disconnected-recoverable',
    'kernel-rejected',
    'prepared',
    'provider-auth-required'
  ]);
});

test('全fixtureがEffect未適用と状態機械分離fieldを持つ', () => {
  for (const name of Object.keys(FIXTURE_FILES)) {
    const fixture = load(name);
    assert.equal(fixture.schema_version, '1.0.0', name);
    assert.equal(fixture.effect_applied, false, name);
    assert.equal(typeof fixture.provider.detected, 'boolean', name);
    assert.ok(Object.hasOwn(fixture.provider, 'registered'), name);
    assert.ok(Object.hasOwn(fixture.provider, 'approved'), name);
    assert.ok(Object.hasOwn(fixture.provider, 'dispatchable'), name);
    assert.ok(Object.hasOwn(fixture.oae_transaction, 'committed'), name);
    assert.ok(Object.hasOwn(fixture.gui_transport, 'persisted'), name);
  }
});

test('preparedはexit 0・acceptedでもcommitまたはEffect適用ではない', () => {
  const fixture = load('prepared');
  assert.equal(fixture.provider.exit_code, 0);
  assert.equal(fixture.kernel.decision, 'accepted');
  assert.equal(fixture.oae_transaction.prepared, true);
  assert.equal(fixture.oae_transaction.committed, false);
  assert.equal(fixture.kernel.effect_applied, false);
});

test('kernel-rejectedはlease-missing負例である', () => {
  const fixture = load('kernel-rejected');
  assert.equal(fixture.kernel.decision, 'rejected');
  assert.equal(fixture.kernel.reason, 'lease-missing');
  assert.equal(fixture.kernel.effect_applied, false);
});

test('provider-auth-requiredはprovider controlでchat responseを持たない', () => {
  const fixture = load('provider-auth-required');
  assert.equal(fixture.provider.process_state, 'provider-interaction');
  assert.equal(fixture.provider.control_state, 'auth-required');
  assert.equal(fixture.provider.chat_response, null);
  assert.equal(fixture.effect_applied, false);
});

test('disconnected-recoverableはabortとpersistedを確定しない', () => {
  const fixture = load('disconnected-recoverable');
  assert.equal(fixture.gui_transport.state, 'disconnected');
  assert.equal(fixture.task_lease.task_state, 'recoverable');
  assert.equal(fixture.gui_transport.durable_state_owner, 'spheredos-server-candidate');
  assert.equal(fixture.gui_transport.persisted, 'unknown');
  assert.equal(fixture.oae_transaction.aborted, false);
});
