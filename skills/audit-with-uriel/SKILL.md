---
name: audit-with-uriel
description: Uriel Positionから、観測事実、protocol、約束、規則、権限、責任、実装状態、資源、停止条件、実行可能性を監査する。宣言と実態、仕様と実装、予定と事実、契約と責務の差分を調べるときに使う。人格・天使・普遍fact checkerではなく、選択されたRegistryとfact scopeを明示する開発環境内監査Skill slotとして動作する。
---

# Uriel監査Skillを発動する

共有された約束と観測境界を追跡するPositionを装備し、後発の都合で成立済み事実を消さない。

## 実行

1. `python3 magi/0.2.1/resolve_sources.py --slot uriel`を実行する。対象repositoryがprofileを
   明示している場合だけ`--profile <id>`と`--repo-root NAME=PATH`を加える。
2. resolverが返した現行sourceを全文読む。ローカル欠損時だけ公開URLを使い、どちらでも読めない必須sourceがあれば監査を開始せず`SOURCE-BLOCK`を返す。
3. 対象、媒体、claim layer、Registry、fact scope、protocol、話者の利害位置を明示する。
4. 事実、予定、願望、神話、未確認、責任、資源を別欄へ分ける。
5. 宣言と実態、約束と引受外、権限と外部操作、実装と未実装を比較する。
6. 仕様・神話・UX矛盾を見つけたら`SEMANTIC-STOP`としてsource差分を返す。
7. 過去資料ではSource Event／Evidence、同時点OAE、現在のInterpretation OAEを分離する。同時点OAE参照が
   なければ`historical-oae-unavailable`＋Last Orderを返し、過去roleやIntentを推論補完しない。

## 通知

```text
【告】ユニークSkill《Uriel監査》を発動
通知種別: 開発環境内Skill
神託: false
人格発話: false
外部操作: false
Position: preserve-fact-promise-and-responsibility-boundaries
```

## Uriel固有定規

```text
fact = observation + protocol + shared promise + traceable boundary
```

これはUriel profile固有の定規であり、Sphere Coreや全Worldの唯一のfact定義ではない。必ず
`registry_ref`と`fact_scope_ref`を付け、上位Systemの定規を上書きしない。

```text
historical evidence != historical OAE
current inference     != past observation
```

## 出力

```text
選択Position: Uriel
読んだsourceとrevision:
Registry／fact scope:
観測事実とprotocol:
約束・責任・引受外:
実装／未実装／未試験:
権限・資源・停止・復旧:
宣言と実態の差分:
Position-talk risk:
unknown／⊥:
action gate: pass | block | revise | observe | bottom
```

既存規則を絶対神にせず、神話・願望を証拠や資源の代用品にしない。
