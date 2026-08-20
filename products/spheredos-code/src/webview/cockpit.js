'use strict';

const stateElement = document.getElementById('fixture-state');
const cockpitElement = document.getElementById('cockpit');
const vscode = acquireVsCodeApi();

window.addEventListener('message', (event) => {
  const message = event.data;
  if (!message) {
    return;
  }
  if (message.type === 'cockpit.projection') {
    stateElement.textContent = `fixture: ${message.fixtureName} / ${message.projection.tone}`;
    cockpitElement.innerHTML = message.projection.html;
  } else if (message.type === 'cockpit.error') {
    stateElement.textContent = `fixture error: ${message.fixtureName}`;
    cockpitElement.textContent = message.message;
  }
});

vscode.postMessage({ type: 'cockpit.ready' });
