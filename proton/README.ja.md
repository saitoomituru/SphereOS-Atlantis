# Proton.md module棚

このdirectoryは、[`Proton.md Core`](../docs/architecture/proton-md-executable-context-container.ja.md)へ
適合するmachine contract、fixture、salvage moduleを保持します。

## 正本と状態

| 対象 | 状態 | 責務 |
|---|---|---|
| [`contract.json`](contract.json) | `IMPLEMENTED_ALPHA` | Proton.md Core machine contract |
| [`fixtures/`](fixtures/) | `IMPLEMENTED_ALPHA` | validator正負fixture |
| [`modules/FoldAccessMapper.proton.md`](modules/FoldAccessMapper.proton.md) | `BETA CONTRACT` | AQC原典からsalvageしたFAM／Fold実行可能仕様 |
| [`modules/FAMFamily.proton.md`](modules/FAMFamily.proton.md) | `DRAFT FAMILY CONTRACT` | FAM JSON、FAMLog、Composite、JSONP、JSON-LD、OAEの派生・投影責務 |

module文書をloadしただけでは、埋込手続き、外部API、Resolver、model、network、deviceを実行しません。
実行には文書外のauthority、capability、Execution Envelope、OAE Transactionが必要です。

旧AQC repositoryは読み取り専用の歴史アーカイブです。Atlantisへ移植したmoduleは旧原典を上書きせず、
source revisionとhashをlineageとして保持します。
