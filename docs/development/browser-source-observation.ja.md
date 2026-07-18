# Web原典観測・手元ブラウザ退避契約

状態: `[ALPHA]` / `SAFARI MCP SMOKE TESTED` / `BROWSER CONTAINER NOT IMPLEMENTED`

## 1. 目的

Web検索、SaaS connector、手元browser、直接HTTP、将来のbrowser containerを、同じ「Webを見た」へ
潰さずに使い分けます。手元browser経路は、検索indexやSaaS cacheの更新待ちを避け、利用者が現在使っている
環境から原典を観測するための退避経路です。

Atlantisはアンチウイルス、EDR、法務判断器、検閲保証サービスではありません。ページを開けたこと、OSの
防御機能が有効なこと、SaaSが応答したことのいずれも、内容の安全・適法・正確・最新を単独では証明しません。

## 2. 観測クラス

| 観測クラス | 証明できる範囲 | 証明しない範囲 |
|---|---|---|
| `INDEXED_SNAPSHOT` | 検索／SaaS面が返したsnapshot | 原典の現在状態、vendor内部処理 |
| `HTTP_OBSERVED` | 応答status、headers、取得bytes／hash | JavaScript実行後DOM、origin revision |
| `BROWSER_OBSERVED` | final URL、title、DOM等のbrowser観測 | 安全性、正しさ、origin freshness |
| `ORIGIN_REVISION_MATCH` | 指定revision／artifactと取得物の一致 | 内容の正しさ、将来も同じであること |

`BROWSER_OBSERVED`へ到達しても「検疫済み」「安全」「最新」へ自動昇格しません。cache、CDN、DNS、proxy、
service workerの影響は別の観測対象です。

## 3. browser resolver

公開・非認証ページのread-only観測では、次の順でbackendを解決します。

1. Registryまたはsession内に利用者が選んだbackend poolがあれば読む。
2. 各backendへ副作用のないcapability probeを行う。
3. 未指定なら、利用可能な手元browser群を示し、session初回に一度だけ利用者へ選択を求める。
4. 選択されたpool内で、同じ権限・data-flowのbackendをstickyに使う。
5. transport障害時は、同じ匿名read-only契約のbackendへだけfailoverし、receiptへ残す。

ログイン済みsession、Cookie、extension、form入力、download、upload、書込み、新domain、機微data送信へ
権限が広がる場合は、初回同意を流用しません。切替backendが別account状態または別data-flowを持つ場合も
再確認します。

2026-07-18時点の手元観測ではSafari MCPが公開ページのread-only観測に成功しました。Chrome MCPは
複数client／session競合が疑われる接続失敗を観測したため、利用可能backendへ自動退避する設計対象とし、
原因確定または恒久互換を宣言しません。

## 4. local観測とSaaS contextの境界

手元browserでページを実行する場合、第三者pageのscript実行主体は原則として利用者host上のbrowserです。
ただし、MCPが返したURL、DOM、本文、screenshot、要約材料をcoding agentへ渡せば、その返却物はSaaS側の
session contextへ入ります。「手元browserを使った」だけで処理全体がlocal-onlyになるわけではありません。

local-onlyが必要な案件では、本文やDOMをSaaSへ返さず、手元で判定した最小receiptまたはhashだけを返す
別profileが必要です。このprofileはまだ実装していません。

SaaS providerは自らのserviceを自社policyで管理でき、利用者組織は自らのlocal資産を組織policyで管理できます。
connector接続だけを理由に、一方の規則を相手側資産へ暗黙継承しません。双方を満たせない案件は
[ガバナンス適用域とWorld Visa](../architecture/governance-scope-and-world-visa.ja.md)に従い、そのoperationだけを
`scoped_avoid`へ落とします。

## 5. 利用者選定のhost検疫・防御デッキ

Atlantisは、利用者が選定したノイマン型計算機のOS、browser、endpoint製品、network製品を置換しません。
既存の検疫・防御動作を邪魔せず、必要な場合は次を別slotとして宣言・観測します。特定OS、製品、vendorを
標準デッキとして強制しません。

| slot | 役割例 | Atlantisの扱い |
|---|---|---|
| `browser_security` | 詐欺サイト警告、download制御 | 設定状態を宣言可能。効力を保証しない |
| `os_anti_malware` | OS標準の検出・除去 | 存在と観測時点を記録。完全防御を主張しない |
| `endpoint_security` | 任意のAV／EDR | 利用者が選ぶ。Atlantisは競合を避ける |
| `dns_or_web_filter` | DNS、proxy、URL filter | 経路として記録。正確性を保証しない |
| `intrusion_prevention` | logとfirewallを使う侵入抑止 | malware scannerと同一視しない |
| `privacy_relay` | IP／DNS等のprivacy保護 | antivirusや適法性判定と同一視しない |

どのslotへ何を採用し、どの組合せを十分とするかは、利用者の自由な選定と利用者側の運用責任です。
各検疫・防御製品の機能、欠陥対応、保証範囲は、その供給者が提示する仕様、契約、support境界に従います。
Atlantisは供給者の責任を肩代わりせず、利用者の選択責任も奪いません。

Atlantisが契約するのは、既存防御を意図的に無効化しないこと、製品種別を混同しないこと、未観測の導入・
稼働・効力を有効と偽らないことです。防壁デッキの強度、安全性、完全性は保証しません。

## 6. receipt

```yaml
schema_version: 0.1.0
observation_class: BROWSER_OBSERVED
requested_url: string
final_url: string
browser_backend: string
browser_session_mode: anonymous-read-only | authenticated | unknown
http_status: integer | unknown
title: string | unknown
artifact_hash: string | none
origin_revision: string | none
origin_revision_match: true | false | unknown
observed_at_system: RFC3339
clock_source: string
clock_calibration: calibrated | unverified | unknown
defense_deck_declared: []
defense_deck_verified: false
content_returned_to_saas: none | metadata | excerpt | dom | screenshot
cache_state: string | unknown
mutations_performed: false
governance_receipt_ref: string | none
limitations: []
```

防御機能は、利用者が導入しているという宣言と、そのversion／稼働を実測した証拠を分けます。観測不能なら
`unknown`または`defense_deck_verified: false`のまま返します。

## 7. 実験証跡の配置

特定host、OS、browser、検疫製品、取得hash、外部URLの実測結果は、この抽象契約へ固定しません。
2026-07-18の手元Safari MCP試験と、そのhostで参照したApple系機能の証跡は
[Web検証ブラウザをコンテナ結界へ封印するブレストnote](../../note/20260718-1648__Web検証ブラウザをコンテナ結界へ封印するブレスト.ja.md)
へ保存します。

正本仕様が保持するのは、backend、権限、data-flow、防壁デッキ、clock、hash／revision、限界をreceiptへ
分離する契約だけです。実験hostで選ばれていた製品をAtlantisの推奨構成または必須依存へ昇格しません。

## 8. offline検査と将来のコンテナ結界

`atlantis links`はMarkdownのrepository内pathと見出しanchorだけをnetworkなしで検査します。外部URLの
現在状態は手元browser receiptと分離します。

将来のSelenium／headless Chromium profileは、標準Venvや通常のVS Code環境からbrowser executionを分け、
壊れた時の破棄単位を作るための「コンテナ結界」です。完全防御ではなく、Docker／Podman実build、権限、
mount、egress、cleanupの試験もまだ完了していません。

実装待機列は[Web検証ブラウザ・コンテナ結界 移管票](../../note/transfer_plan/web-browser-container-barrier.ja.md)、
設計履歴は[ブレストnote](../../note/20260718-1648__Web検証ブラウザをコンテナ結界へ封印するブレスト.ja.md)を参照してください。
