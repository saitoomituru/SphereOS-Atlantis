# Provider Adapters

状態: `[SCAFFOLDED]`

Codex、Claude、Gemini、Grok、Ollama、将来のthird-party CLI等を、各provider固有CUIのまま検出・起動し、
結果をWorker Envelopeへ渡すBridge候補です。

DOSはproviderのinstall、auth、payment、quota、activationを所有しません。非chat状態、refusal、control出力、
opaque payloadを成功回答へ丸めずUserへ返します。既存Sourceは[`agents/`](../../agents/)と
[`atlantis_cli/agent.py`](../../atlantis_cli/agent.py)です。
