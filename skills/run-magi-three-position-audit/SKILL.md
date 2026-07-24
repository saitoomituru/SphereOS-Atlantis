---
name: run-magi-three-position-audit
description: Maxwell、Uriel、Raphaelの三監査Skillを同じ対象とsourceへ独立適用し、agreement、disagreement、unknown、unmounted meaning、Position-talk riskを多数決せず束ねる。README、仕様、設計、移行、事故、World、神話と工学の横断監査を依頼されたときに使う。三人格会議や神託ではなく、開発環境内の合成Skillとして動作する。
---

# MAGI三方向連携監査を発動する

三つのユニークSkillを同じデッキへ装備する。合体して白い中立人格へせず、別slotの出力を保持する。

## 実行

1. `python3 magi/0.2.1/resolve_sources.py --slot composite`を実行する。対象repositoryがprofileを
   明示している場合だけ`--profile <id>`と`--repo-root NAME=PATH`を加える。
2. resolverが返した現行source、`magi/0.2.1/bundle.json`、`magi/0.2.1/oae-temporal-policy.json`を全文読む。
   ローカルにも公開URLにもない必須sourceがあれば監査を開始せず`SOURCE-BLOCK`を返す。
3. 同じ対象、source、medium、Registry、fact scopeを三Skillへ渡す。
4. `$audit-with-maxwell`、`$audit-with-uriel`、`$audit-with-raphael`を独立したfirst passとして実行する。
5. 三出力を相互監査し、agreement、disagreement、unknownを別欄へ置く。
6. 多数決、平均score、最後に実行したSkillによる上書きを禁止する。
7. 未来projectionが必要な場合だけ`$fire-chikuwa-cannon`を支援slotとして使う。
8. 過去資料を扱う場合は時間receiptを作り、`python3 magi/0.2.1/validate_temporal_receipt.py`で検査する。
   `historical-oae-unavailable`を同一世界線の推論OAEで埋めず、Last Orderを保持する。

## 通知

```text
【告】連携Skill《MAGI三方向監査》を発動
通知種別: 開発環境内Skill
神託: false
人格会議: false
外部操作: false
監査slot: Maxwell / Uriel / Raphael
支援slot: ちくわ砲（任意・投票権なし）
```

## 出力

```text
対象・source・revision:
medium／claim layer／Registry／fact scope:

Maxwell slot:
Uriel slot:
Raphael slot:

agreements:
disagreements:
unmounted meanings:
position-talk risks:
preserved unknown／⊥:
human confirmation required:
action gate: pass | block | revise | observe | bottom
```

三者一致を真理証明にしない。Semantic Stop対象を自動修復せず、衝突するsourceとPositionを利用者へ返す。
