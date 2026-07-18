---
name: fire-chikuwa-cannon
description: ちくわ砲のProspective Meta-Safety Positionから、未実行の未来RiskとBenefit、必要な人員・装備・時間・停止権限・復旧能力を、現在の警告と混ざらない幻想・ゲームpaneへ表示する。Manifestの詳細をDigして次の探索branchを親しみやすく案内するときに使う。live incidentを隠さず、予測・予知・外部操作・個人責任scoreを生成しない支援Skill slotとして動作する。
---

# ちくわ砲を発射する

ちくわの穴から未来を見る。いま燃えている火は非常灯で照らし、まだ燃えていない候補だけを未来弾道へ置く。

## 実行

1. `python3 magi/0.2.0/resolve_sources.py --slot chikuwa-cannon`を実行する。
2. resolverが返した現行sourceを全文読む。ローカル欠損時だけ公開URLを使い、どちらでも読めない必須sourceがあれば発射せず`SOURCE-BLOCK`を返す。
3. 情報を`LIVE`、`POST_RUN`、`PROSPECTIVE`へ分類する。
4. 実際に読んだManifest記述は`OBSERVED`としてsourceとrevisionを示す。
5. 次に掘る候補、未来branch、Risk、Benefit、必要資源だけを幻想paneへ置く。
6. themeから外部操作、承認、課金、model call、測定を開始しない。

## 通知

```text
【告】支援Skill《ちくわ砲》を装填
通知種別: 開発環境内Skill
神託: false
人格発話: false
外部操作: false
Position: prospective-meta-safety-support
```

## 三pane

| scope | evidence | 表示 |
|---|---|---|
| `LIVE` | `OBSERVED` | 枯れた警告。止める・退避する・復旧する |
| `POST_RUN` | `OBSERVED / REPRODUCED` | 証拠、ログ、部分成果、再発防止 |
| `PROSPECTIVE` | `PROJECTED / INFERRED / UNKNOWN` | ちくわ砲の未来弾道 |

## 出力

```text
【実測Dig】
読んだsourceとrevision:
LIVEの事実・警告:
POST_RUNの証拠:
unknown:

【未来弾道／ちくわ砲】
次に掘る候補:
期待Benefit:
候補Risk:
必要role／equipment／effort／time:
必要なstop authority／recovery readiness:
実行前確認:
```

円、確率、損害額、個人責任scoreを捏造しない。RiskとBenefitを両方示し、使命感で資源不足を埋めない。
