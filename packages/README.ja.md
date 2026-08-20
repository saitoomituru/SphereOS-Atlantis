# 6xx共有packages

`packages/`はPresentationとHostから再利用する6xx共有責務の鍛造棚です。

| package | 責務 | 現在地 |
|---|---|---|
| `reincarnation-lean-kernel` | World／Fold／task／lease／OAE／receiptの最小意味伝達保証 | `NOT IMPLEMENTED` |
| `fold-access-mapper` | Git／Issue／branch／workspaceをFAM探索木へ投影 | `SCAFFOLDED` |
| `provider-adapters` | 既存CLI検出、capability記録、opaque結果搬送 | `SCAFFOLDED` |

このdirectoryの存在はruntime、SDK package、binary distributionの完成を意味しません。既存Sourceを移す前に
[m.6xx.1 Dev Roadmap](../docs/status/m6xx-dev-roadmap.ja.md#3-source移設規則)のmigration手順を通します。
