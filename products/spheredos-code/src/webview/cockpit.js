'use strict';

const stateElement = document.getElementById('fixture-state');
const cockpitElement = document.getElementById('cockpit');

window.addEventListener('message', (event) => {
  const message = event.data;
  if (!message || message.type !== 'cockpit.fixture-selected') {
    return;
  }
  stateElement.textContent = `fixture: ${message.fixtureName}`;
  cockpitElement.textContent = 'projectionを準備中';
});
