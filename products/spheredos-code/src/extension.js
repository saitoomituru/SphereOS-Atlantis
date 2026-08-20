'use strict';

const vscode = require('vscode');
const { CockpitPanel } = require('./cockpit-panel');

const FIXTURE_COMMANDS = Object.freeze({
  'spheredosCode.openCockpit': 'prepared',
  'spheredosCode.showPrepared': 'prepared',
  'spheredosCode.showKernelRejected': 'kernel-rejected',
  'spheredosCode.showProviderAuthRequired': 'provider-auth-required',
  'spheredosCode.showDisconnectedRecoverable': 'disconnected-recoverable'
});

function activate(context) {
  for (const [command, fixtureName] of Object.entries(FIXTURE_COMMANDS)) {
    context.subscriptions.push(vscode.commands.registerCommand(command, () => {
      CockpitPanel.createOrShow(context.extensionUri, fixtureName);
    }));
  }

  context.subscriptions.push(vscode.commands.registerCommand(
    'spheredosCode.reloadCockpit',
    () => CockpitPanel.reloadCurrent()
  ));
}

function deactivate() {
  CockpitPanel.disposeCurrent();
}

module.exports = { activate, deactivate };
