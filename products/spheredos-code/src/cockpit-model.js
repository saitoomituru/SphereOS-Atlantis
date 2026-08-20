'use strict';

const DISPLAY_UNKNOWN = 'unknown';
const DISPLAY_NOT_PROVIDED = 'not provided';
const TONES = new Set(['neutral', 'pending', 'rejected', 'control', 'recoverable', 'success', 'unknown']);

function own(object, key) {
  return object !== null
    && typeof object === 'object'
    && Object.prototype.hasOwnProperty.call(object, key);
}

function displayValue(object, key, missing = DISPLAY_NOT_PROVIDED) {
  if (!own(object, key) || object[key] === null || object[key] === undefined) {
    return missing;
  }
  if (Array.isArray(object[key])) {
    return object[key].length ? object[key].join(', ') : '(empty)';
  }
  if (typeof object[key] === 'object') {
    return JSON.stringify(object[key]);
  }
  return String(object[key]);
}

function section(title, source, fields) {
  const safeSource = source && typeof source === 'object' ? source : {};
  return {
    title,
    rows: fields.map(([label, key, missing]) => ({
      label,
      value: displayValue(safeSource, key, missing)
    }))
  };
}

function selectTone(fixture) {
  const kernel = fixture.kernel || {};
  const provider = fixture.provider || {};
  const transaction = fixture.oae_transaction || {};
  const transport = fixture.gui_transport || {};

  if (kernel.decision === 'rejected') {
    return 'rejected';
  }
  if (transport.state === 'disconnected') {
    return transport.recoverable === true ? 'recoverable' : 'unknown';
  }
  if (provider.process_state === 'provider-interaction') {
    return 'control';
  }
  if (transaction.committed === true && fixture.effect_applied === true) {
    return 'success';
  }
  if (transaction.prepared === true || kernel.decision === 'accepted') {
    return 'pending';
  }
  return 'unknown';
}

function projectFixture(envelope) {
  if (!envelope || typeof envelope !== 'object' || !envelope.payload || typeof envelope.payload !== 'object') {
    throw new TypeError('fixture envelopeが不正です。');
  }

  const fixture = envelope.payload;
  const coordinate = fixture.coordinate || {};
  const worldFold = fixture.world_fold || {};
  const taskLease = fixture.task_lease || {};
  const provider = fixture.provider || {};
  const transaction = fixture.oae_transaction || {};
  const receipt = fixture.receipt || {};
  const kernel = fixture.kernel || {};
  const transport = fixture.gui_transport || {};
  const tone = selectTone(fixture);

  return {
    fixtureName: envelope.fixtureName || DISPLAY_UNKNOWN,
    sourceTransport: envelope.transport || DISPLAY_UNKNOWN,
    tone: TONES.has(tone) ? tone : 'unknown',
    summary: {
      kernelDecision: displayValue(kernel, 'decision', DISPLAY_UNKNOWN),
      taskState: displayValue(taskLease, 'task_state', DISPLAY_UNKNOWN),
      oaeState: transaction.committed === true
        ? 'committed'
        : transaction.prepared === true
          ? 'prepared'
          : transaction.suspended === true
            ? 'suspended'
            : DISPLAY_UNKNOWN,
      transportState: displayValue(transport, 'state', DISPLAY_UNKNOWN),
      effectApplied: displayValue(fixture, 'effect_applied', DISPLAY_UNKNOWN)
    },
    sections: [
      section('Coordinate', coordinate, [
        ['function series', 'function_series', DISPLAY_UNKNOWN],
        ['protocol generation', 'protocol_generation', DISPLAY_UNKNOWN],
        ['presentation', 'presentation', DISPLAY_UNKNOWN],
        ['candidate / implemented boundary', 'implementation_boundary', DISPLAY_UNKNOWN]
      ]),
      section('World / Fold', worldFold, [
        ['world_ref', 'world_ref', DISPLAY_UNKNOWN],
        ['fold_ref', 'fold_ref', DISPLAY_UNKNOWN],
        ['scope', 'scope', DISPLAY_UNKNOWN],
        ['unknown', 'unknown', DISPLAY_UNKNOWN]
      ]),
      section('Task / Lease', taskLease, [
        ['task_id', 'task_id', DISPLAY_UNKNOWN],
        ['task state', 'task_state', DISPLAY_UNKNOWN],
        ['lease state', 'lease_state', DISPLAY_UNKNOWN],
        ['base revision', 'base_revision', DISPLAY_UNKNOWN],
        ['write-set', 'write_set', DISPLAY_UNKNOWN],
        ['artifact claim', 'artifact_claim', DISPLAY_UNKNOWN],
        ['Issue state', 'issue_state', DISPLAY_UNKNOWN],
        ['Mission state', 'mission_state', DISPLAY_UNKNOWN]
      ]),
      section('Kernel Decision', kernel, [
        ['decision', 'decision', DISPLAY_UNKNOWN],
        ['reason', 'reason', DISPLAY_UNKNOWN],
        ['effect_applied', 'effect_applied', DISPLAY_UNKNOWN]
      ]),
      section('Provider', provider, [
        ['provider_id', 'provider_id', DISPLAY_UNKNOWN],
        ['detected', 'detected', DISPLAY_UNKNOWN],
        ['registered', 'registered', DISPLAY_UNKNOWN],
        ['approved', 'approved', DISPLAY_UNKNOWN],
        ['dispatchable', 'dispatchable', DISPLAY_UNKNOWN],
        ['process state', 'process_state', DISPLAY_UNKNOWN],
        ['exit code', 'exit_code', DISPLAY_UNKNOWN],
        ['control state', 'control_state', DISPLAY_UNKNOWN],
        ['auth / quota / refusal / opaque result', 'control_output', DISPLAY_UNKNOWN],
        ['chat response', 'chat_response', DISPLAY_NOT_PROVIDED]
      ]),
      section('OAE Transaction', transaction, [
        ['opened', 'opened', DISPLAY_UNKNOWN],
        ['prepared', 'prepared', DISPLAY_UNKNOWN],
        ['suspended', 'suspended', DISPLAY_UNKNOWN],
        ['committed', 'committed', DISPLAY_UNKNOWN],
        ['aborted', 'aborted', DISPLAY_UNKNOWN],
        ['branched', 'branched', DISPLAY_UNKNOWN]
      ]),
      section('Receipt / Provenance', receipt, [
        ['source', 'source', DISPLAY_UNKNOWN],
        ['process', 'process', DISPLAY_UNKNOWN],
        ['revision', 'revision', DISPLAY_UNKNOWN],
        ['artifact', 'artifact', DISPLAY_UNKNOWN],
        ['observed_at', 'observed_at', DISPLAY_UNKNOWN],
        ['unknown', 'unknown', DISPLAY_UNKNOWN]
      ]),
      section('GUI Transport / Recovery', transport, [
        ['state', 'state', DISPLAY_UNKNOWN],
        ['recoverable', 'recoverable', DISPLAY_UNKNOWN],
        ['durable state owner', 'durable_state_owner', DISPLAY_UNKNOWN],
        ['persisted', 'persisted', DISPLAY_UNKNOWN]
      ]),
      {
        title: 'Authority Boundaries',
        rows: [
          { label: 'GUI is OAE authority', value: 'false' },
          { label: 'GUI is durable state canonical store', value: 'false' },
          { label: 'Provider control output is chat', value: 'false' }
        ]
      }
    ]
  };
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function renderProjectionHtml(projection) {
  const tone = TONES.has(projection.tone) ? projection.tone : 'unknown';
  const summaryItems = Object.entries(projection.summary)
    .map(([label, value]) => `<li><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></li>`)
    .join('');
  const sections = projection.sections.map((item) => {
    const rows = item.rows.map((row) => (
      `<div class="row"><dt>${escapeHtml(row.label)}</dt><dd>${escapeHtml(row.value)}</dd></div>`
    )).join('');
    return `<section><h2>${escapeHtml(item.title)}</h2><dl>${rows}</dl></section>`;
  }).join('');

  return `<div class="status status-${tone}"><span>projection state</span><strong>${escapeHtml(tone)}</strong></div>`
    + `<ul class="summary">${summaryItems}</ul>`
    + `<div class="sections">${sections}</div>`;
}

module.exports = {
  DISPLAY_NOT_PROVIDED,
  DISPLAY_UNKNOWN,
  escapeHtml,
  projectFixture,
  renderProjectionHtml,
  selectTone
};
