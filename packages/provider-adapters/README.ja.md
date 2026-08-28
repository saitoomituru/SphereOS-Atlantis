# Provider Adapters

状態: `[SCAFFOLDED]` `[OFFLINE OBSERVATION HARNESS IMPLEMENTED]` `[NATIVE INVOCATION NOT IMPLEMENTED]`

Codex、Claude、Gemini、Grok、Ollama、将来のthird-party CLI等を、各provider固有CUIのまま検出・起動し、
結果をWorker Envelopeへ渡すBridge候補です。

DOSはproviderのinstall、auth、payment、quota、activationを所有しません。非chat状態、refusal、control出力、
opaque payloadを成功回答へ丸めずUserへ返します。既存Sourceは[`agents/`](../../agents/)と
[`atlantis_cli/agent.py`](../../atlantis_cli/agent.py)です。

## m.6xx異種agent実験足場

Issue #26向けに、Claude Code、Gemini CLI、Grok CLIを起動せず検出し、明示指定した対象repositoryの
branch、HEAD、dirty件数、local upstream refとの距離だけを観測するoffline harnessを追加しました。

- shell入口: [`scripts/m6xx-agent-orchestration.sh`](../../scripts/m6xx-agent-orchestration.sh)
- 実装: [`atlantis_cli/experiment.py`](../../atlantis_cli/experiment.py)
- 実験契約: [`experiments/m6xx-agent-orchestration/contract.json`](../../experiments/m6xx-agent-orchestration/contract.json)
- test: [`tests/test_experiment.py`](../../tests/test_experiment.py)
- 研究note: [SphereDOS 0.6xx異種agent native orchestration実験](../../docs/research/2026-08-28-spheredos-m6xx-foldnic-hage-agent-orchestration-ja.md)

```bash
scripts/m6xx-agent-orchestration.sh doctor \
  --target-root fold-nic=/absolute/path/to/fold-nic \
  --target-root edohage-tubo=/absolute/path/to/EDOHAGE-TUBO \
  --json

scripts/m6xx-agent-orchestration.sh snapshot \
  --target-root fold-nic=/absolute/path/to/fold-nic \
  --record-local \
  --json
```

`--record-local`はraw prompt／outputを収集せず、sanitized JSONだけをignore済み`.atlantis/`へ保存します。
対象repositoryは変更しません。ただしAtlantis側のgenerated stateは作るため、完全なread-only commandでは
ありません。`doctor`、`snapshot`、`plan`はmodelを起動せず、`run`は`NOT IMPLEMENTED`で終了します。

このharnessをprovider実行、認証、session resume、process supervisor、clean-room採用、Server常駐、
製品runtimeとして数えません。別名toolを新設せず、既存`atlantis_cli.agent`とBuddy action gateを
extendし、実験固有部分だけをadapterとして追加しました。
