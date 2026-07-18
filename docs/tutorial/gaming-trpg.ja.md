# ゲーム・TRPG棚から入る

状態: `[ALPHA]`

この棚では、Atlantisを複数World、ルール、Entity、セッション、リプレイを扱う基盤として読みます。
ゲーム内の魔王や神は、そのWorld authorityが実在Entityとして登録すれば、そのscopeでは実在します。
現実世界の科学的実在判定へ勝手に持ち出しません。

## 言葉の橋

| ゲーム・TRPGの言葉 | 開発上の接続候補 |
|---|---|
| ワールド／キャンペーン | WorldとRegistry scope |
| PC、NPC、GM、運営 | Agency、role、authority |
| キャラクターシート | Entity Schemaと状態revision |
| ルールブック | Registry、Causality Profile、制約 |
| 判定・行動・イベント | input、Event、Effect、OAE |
| リプレイ・ログ | sourceを保持したFAMLog／receipt |
| クロスオーバー | 明示的なAccess MapとTransformer |

## 最小演習

一つのセッションまたはクエストを選び、次を記録します。

```text
World ID:
採用ルールとrevision:
参加Agency:
開始状態:
行為と判定:
観測されたEffect:
別解釈または仮説:
越境してよい別World:
越境してはいけない範囲:
```

PCとプレイヤー、NPCと運営、物語上の原因とシステム障害を無断で同一化しないことが最初の試験です。
記録できたら[共通到達点](README.ja.md#全棚に共通する到達点)へ進みます。
