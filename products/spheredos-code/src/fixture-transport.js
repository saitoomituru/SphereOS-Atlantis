'use strict';

const fs = require('node:fs');
const path = require('node:path');

const FIXTURE_FILES = Object.freeze({
  prepared: 'prepared.json',
  'kernel-rejected': 'kernel-rejected.json',
  'provider-auth-required': 'provider-auth-required.json',
  'disconnected-recoverable': 'disconnected-recoverable.json'
});

class FixtureTransport {
  constructor(extensionRoot) {
    this.fixtureRoot = path.join(extensionRoot, 'fixtures');
  }

  load(fixtureName) {
    const fileName = FIXTURE_FILES[fixtureName];
    if (!fileName) {
      throw new Error(`未登録fixture: ${fixtureName}`);
    }

    const fixturePath = path.join(this.fixtureRoot, fileName);
    const payload = JSON.parse(fs.readFileSync(fixturePath, 'utf8'));
    return {
      fixtureName,
      transport: 'mock-fixture',
      payload
    };
  }
}

module.exports = { FIXTURE_FILES, FixtureTransport };
