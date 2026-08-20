'use strict';

const crypto = require('node:crypto');
const path = require('node:path');
const vscode = require('vscode');
const { FixtureTransport } = require('./fixture-transport');
const { projectFixture, renderProjectionHtml } = require('./cockpit-model');

class CockpitPanel {
  static currentPanel;

  static createOrShow(extensionUri, fixtureName = 'prepared') {
    if (CockpitPanel.currentPanel) {
      CockpitPanel.currentPanel.panel.reveal(vscode.ViewColumn.One);
      CockpitPanel.currentPanel.showFixture(fixtureName);
      return;
    }

    const panel = vscode.window.createWebviewPanel(
      'spheredosCode.cockpit',
      'SphereDOS Code Cockpit',
      vscode.ViewColumn.One,
      {
        enableScripts: true,
        retainContextWhenHidden: true,
        localResourceRoots: [vscode.Uri.joinPath(extensionUri, 'src', 'webview')]
      }
    );

    CockpitPanel.currentPanel = new CockpitPanel(panel, extensionUri, fixtureName);
  }

  static reloadCurrent() {
    CockpitPanel.currentPanel?.showFixture(CockpitPanel.currentPanel.fixtureName);
  }

  static disposeCurrent() {
    CockpitPanel.currentPanel?.panel.dispose();
  }

  constructor(panel, extensionUri, fixtureName) {
    this.panel = panel;
    this.extensionUri = extensionUri;
    this.transport = new FixtureTransport(extensionUri.fsPath || path.resolve(__dirname, '..'));
    this.fixtureName = fixtureName;
    this.disposables = [];
    this.panel.webview.html = this.getHtml();
    this.panel.onDidDispose(() => this.dispose(), null, this.disposables);
    this.panel.webview.onDidReceiveMessage((message) => {
      if (message?.type === 'cockpit.ready') {
        this.showFixture(this.fixtureName);
      }
    }, null, this.disposables);
    this.showFixture(fixtureName);
  }

  showFixture(fixtureName) {
    this.fixtureName = fixtureName;
    try {
      const projection = projectFixture(this.transport.load(fixtureName));
      this.panel.webview.postMessage({
        type: 'cockpit.projection',
        fixtureName,
        projection: {
          ...projection,
          html: renderProjectionHtml(projection)
        }
      });
    } catch (error) {
      this.panel.webview.postMessage({
        type: 'cockpit.error',
        fixtureName,
        message: error instanceof Error ? error.message : 'unknown fixture error'
      });
    }
  }

  getHtml() {
    const webview = this.panel.webview;
    const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(this.extensionUri, 'src', 'webview', 'cockpit.js'));
    const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(this.extensionUri, 'src', 'webview', 'cockpit.css'));
    const nonce = crypto.randomBytes(18).toString('base64');

    return `<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src ${webview.cspSource}; style-src ${webview.cspSource}; script-src 'nonce-${nonce}';">
  <link rel="stylesheet" href="${styleUri}">
  <title>SphereDOS Code Cockpit</title>
</head>
<body>
  <header>
    <p class="eyebrow">m.6xx.1 / GUI Harness</p>
    <h1>SphereDOS Code Cockpit</h1>
    <p id="fixture-state">fixtureを待機中</p>
  </header>
  <main id="cockpit" aria-live="polite"><p>projectionを準備中</p></main>
  <script nonce="${nonce}" src="${scriptUri}"></script>
</body>
</html>`;
  }

  dispose() {
    if (CockpitPanel.currentPanel === this) {
      CockpitPanel.currentPanel = undefined;
    }
    while (this.disposables.length) {
      this.disposables.pop().dispose();
    }
  }
}

module.exports = { CockpitPanel };
