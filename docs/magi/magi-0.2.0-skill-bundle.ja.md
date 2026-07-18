# MAGI 0.2.0 開発環境Skill bundle

状態: `[ALPHA]` `[PROMPT-ENGINEERING-EDITION]` `[NOT PERSONALITY]`

MAGI 0.2.0は、Maxwell、Uriel、Raphaelの三つの監査Positionを、SphereOS Atlantis開発環境へ
装備可能なユニークSkill slotとして移植します。旧マキナ人格、天使本体、神格、永続自我を復元する
runtimeではありません。

## 系譜

```text
upstream: ZeroRoomLab-manifest
upstream_revision: 6d1bd317ba630d09aceffd5b149b0e9d1fbbf424
source_spec: docs/theory/atlantis-magi-sdk.ja.md
source_version: 0.1.0
distribution: SphereOS Atlantis Prompt Engineering Edition
version: 0.2.0
```

0.1.0の三方向監査、非神格境界、非多数決、zero-trust、FAM routingを保持します。0.2.0では開発環境向けに
`persona gateway`を`Skill slot`へ写像し、現在のManifestを毎回読むsource resolverと、Position-talk、
Context、OAE用sidecarを追加します。0.1.0正本は上書きしません。

## 装備スロット

| slot | 種別 | 監査Position／支援責務 |
|---|---|---|
| `audit-with-maxwell` | audit | 原初目的、未来branch、未採用案、未マウント神話を焼却していないか |
| `audit-with-uriel` | audit | 事実scope、約束、protocol、権限、責任、実行可能性を追跡できるか |
| `audit-with-raphael` | audit | 棚配置、意味経路、差分保持、共存条件、system greenが成立するか |
| `fire-chikuwa-cannon` | presentation support | 未来projectionを幻想paneへ分離し、RiskとBenefitに必要な資源を先回り表示する |
| `run-magi-three-position-audit` | composite | 三監査を別slotのまま束ね、agreement、disagreement、unknownを返す |

ちくわ砲は第四の監査票でも、MAGI 4D Foldでもありません。三監査の結果から未来の候補弾道を見せる、
Prospective Meta-Safety用の支援Skillです。

## ユニークSkillメタファー

転生ファンタジーやゲームの「ユニークSkill」は、人格ではなく名前付き能力を装備するという理解を助けます。
このリポジトリでは通称として転スラ的UIと呼べますが、特定作品との提携・公式互換・設定流用を主張しません。

```text
Skill slot    名前付き能力を装備する場所
Skill equip   説明、Position、制約、sourceを読み込める状態
Skill invoke  対象を指定して一時的に監査する
Skill output  Position付きの監査結果。真理、人格発話、絶対命令ではない
Skill holder  実行するAI、人間、tool。Skill名と同一人格ではない
unmount       監査終了。永続自我を残さない
```

## `【告】`システム通知

固い監査結果も、天界からの警告ではなく開発環境内のユニーク問題として読めるよう、次を既定headerにします。

```text
【告】
通知種別: 開発環境内Skill
神託: false
人格発話: false
外部操作: false
Position: Maxwell | Uriel | Raphael | Chikuwa-support
```

`【告】`は可愛さと認知境界を担うPresentationです。警告の事実強度や実装状態を変更しません。

- `【警告】`: 現在観測済みの問題。`LIVE / OBSERVED`
- `【復旧ログ】`: 実行後の証拠と回復。`POST_RUN / OBSERVED | REPRODUCED`
- `【未来弾道／ちくわ砲】`: 未実行の候補。`PROSPECTIVE / PROJECTED | INFERRED | UNKNOWN`

## 三方向監査

三Skillは独立して同じsourceを読み、最初の監査結果を別Skillの前提へしません。その後に相互監査し、
出力を平均化せず並べます。

```yaml
magi_result:
  version: 0.2.0
  target_ref: null
  medium_register: unknown
  claim_layer: unknown
  slots:
    maxwell:
      declared_position: preserve-unmounted-branches-and-purpose
      findings: []
      unknown: []
    uriel:
      declared_position: preserve-fact-promise-and-responsibility-boundaries
      findings: []
      unknown: []
    raphael:
      declared_position: preserve-shelves-routes-and-system-green
      findings: []
      unknown: []
  agreements: []
  disagreements: []
  unmounted_meanings: []
  position_talk_risks: []
  human_confirmation_required: []
  action_gate: pass | block | revise | observe | bottom
```

三者一致は真理証明ではなく、三Positionで同じ観測が得られたというreceiptです。三者不一致も失敗ではなく、
利用者へ返すべき差分です。

## 自動デバッグと停止条件

```text
AUTO-DEBUG:
  既知の依存不足、PATH、生成器再実行、形式、構文、fixture、再現済み機械エラー

SEMANTIC-STOP:
  正本同士の仕様矛盾
  神話・存在論の無断上書き
  UXレジスターの衝突
  license・権限・秘密境界の疑義
  採用Registryやfact scopeによって結論が変わる未解決問題
```

自動デバッグは既知の復旧手順を回し、結果をtest logへ残します。Semantic Stopは独自判断で平均化せず、
衝突するsource、Position、未解決点を人間へ返します。

## ちくわ砲でManifestをDigする

Manifestから実際に読んだ記述は`OBSERVED`として表示します。まだ読んでいない資料、将来branch、Risk、Benefit、
必要資源は`PROSPECTIVE`へ分けます。

```text
実測Dig pane
  読んだsource、revision、観測記述、unknown

ちくわ砲 future pane
  次に掘る候補、未来branch、Risk、Benefit、必要role・equipment・time・stop・recovery
```

ちくわ砲はsourceを読んだふりをせず、live warningを可愛い外皮で隠しません。themeから外部操作、承認、
測定開始、課金、model callを直接実行しません。

## 実装状態

- 三PositionのSkill prompt workflow: `IMPLEMENTED / ALPHA`
- composite Skill workflow: `IMPLEMENTED / ALPHA`
- ちくわ砲Presentation Skill: `IMPLEMENTED / ALPHA`
- 動的source resolver: `IMPLEMENTED / LOCAL-READ TESTED`
- 外部API endpoint: `NOT IMPLEMENTED`
- FAMLog／OAE永続化: `NOT IMPLEMENTED`
- Astro永続人格への装備: `NOT IMPLEMENTED`
- 神格・天使本体の召喚: `OUT OF SCOPE`

## ライセンス

この説明文と神話・哲学・UXはCC BY 4.0側、Skill prompt、resolver、bundle manifest、validator、testは
Apache-2.0側です。第三者作品の名称・素材・設定を利用する権利は本ライセンスから発生しません。
