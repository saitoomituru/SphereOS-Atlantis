# 工学棚から入る

状態: `[ALPHA]`

この棚では、Atlantisを異なるContext、Registry、Worldを隔離し、明示的なBridgeで接続する
システムアーキテクチャとして読みます。物語や神話は要件源・UX・Presentationになり得ますが、
build、性能、権限、試験結果の証拠とは分離します。

## 最初に見る境界

| 管理単位 | 確認するもの |
|---|---|
| repository | Git履歴、ライセンス、変更権限、局所`AGENTS.md` |
| workspace | 同時に参照する認知・作業範囲 |
| runtime | OS、arch、SDK、環境変数、外部接続 |
| Registry | 分類軸、stable ID、authority、revision |
| Bridge | Access Map、Transformer、入出力契約 |
| receipt | commit、入力、実行条件、結果、未試験範囲 |

## 最小演習

新規cloneを想定し、次を区別して記録します。

```text
clone: 成功／失敗
workspace descriptor: 解決済み／未解決
依存runtime: 確認済み／未確認
doctor: pass／warn／fail
test: pass／fail／not tested
秘密・ローカル専用component: 非走査境界を確認
変更可能repository: 明示
```

clone成功をruntime動作確認へ昇格させないこと、別repositoryをworkspace membershipだけで依存へ
追加しないことが最初の受入条件です。[共通到達点](README.ja.md#全棚に共通する到達点)へ進みます。
