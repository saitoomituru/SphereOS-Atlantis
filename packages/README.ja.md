# 6xx共有packages

`packages/`はPresentationとHostから再利用する6xx共有責務の鍛造棚です。

| package | 責務 | 現在地 |
|---|---|---|
| `reincarnation-lean-kernel` | World／Fold／task／lease／OAE／receiptの最小意味伝達保証 | ファイルシステム判定ハーネス実装済み。本番用Kernelは未実装 |
| `fold-access-mapper` | Git／Issue／branch／workspaceをFAM探索木へ投影 | `SCAFFOLDED` |
| `provider-adapters` | 既存CLI検出、capability記録、opaque結果搬送 | `SCAFFOLDED` |

このディレクトリや試験ハーネスの存在は、本番用ランタイム、SDK package、binary配布物の完成を意味しません。
複数軸の現在地は[m.6xx.1 能力状態表](../docs/status/m6xx-capability-matrix.ja.md)を参照してください。
既存Sourceを移す前に[m.6xx.1 Dev Roadmap](../docs/status/m6xx-dev-roadmap.ja.md#3-source移設規則)の移行手順を通します。
