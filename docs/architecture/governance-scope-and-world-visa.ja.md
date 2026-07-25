# ガバナンス適用域とWorld Visa

状態: `[ALPHA]`

## 1. 芯

Atlantisは、接続したSaaS、上位System、組織、国、Worldの規則を、別の資産へ自動継承しません。
同時に、どれか一つの規則を「世界共通で正しい定規」として採用しません。

一つの操作に複数の適用域が重なる場合は、渡されたRegistryとauthorityを使って、その操作を実行できる
共通範囲を機械的に求めます。共通範囲がない、または必要なauthorityが不明なら、その案件だけを
`scoped_avoid`へ落とします。他の案件、World、connector、資産まで禁止へ巻き込みません。

これは法的判断の自動化ではありません。どの法律、契約、組織規程が実際に適用されるかは、利用者側の
法務・コンプライアンスまたはWorld authorityが制定し、Atlantisはその入力と判断receiptを保持します。

## 2. 混ぜない四つの適用域

| 適用域 | 例 | 制定authority | Atlantisがしないこと |
|---|---|---|---|
| `provider_service_scope` | SaaSの利用規約、model／connector policy | provider | provider規則をlocal資産の法体系へ昇格しない |
| `asset_governance_scope` | 利用者組織の情報管理、契約上の業務範囲 | asset owner／組織 | provider接続だけを理由に上書きしない |
| `jurisdiction_scope` | 処理地、保管地、当事者に関係する法域 | 指定された法務authority | 国境を見て独自に適法・違法を断定しない |
| `world_visa_scope` | ゲーム内role、Companion権限、World間越境条件 | World authority | 現実法、神学、ゲーム規則を暗黙変換しない |

SaaSは自らのserviceと資産を自らのpolicyで拘束できます。利用者組織もlocal資産と業務を自らのauthorityで
拘束できます。connectorを一本つないだことは、どちらかのauthorityが相手側全域を獲得したことを
意味しません。ただし、一つの処理が双方の適用域へ実際に触れるなら、その処理は双方を満たす必要があります。

assetのProvenance、lineage、structural similarityは、`asset_governance_scope`を読み解くsourceには
なり得ますが、それ自体をownership verdict、permission、provider capabilityへ昇格しません。
commercial／private Worldのscopeも、そのWorldからopen coreや無関係なWorldへ自動継承しません。

## 3. 判定契約

```yaml
operation_id: string
operation_scope: string
asset_owner: string | unknown
asset_location: string | unknown
processing_location: string | unknown
data_residency: string | unknown
governance_authorities: []
provider_service_scope: string | none | unknown
asset_governance_scope: string | none | unknown
jurisdiction_scope: string | none | unknown
world_visa_scope: string | none | unknown
governance_match: matched | conflict | unknown
decision: proceed | scoped_avoid | isolate | require_human_review
reason_codes: []
evidence_refs: []
```

初期`reason_codes`候補:

- `contract_scope_out`: 委託、派遣、職務等の制定済み業務範囲外
- `provider_policy_out`: provider service上で許可されない
- `asset_governance_out`: 対象資産のauthorityが許可しない
- `jurisdiction_conflict`: 入力された法域要件を同時に満たせない
- `world_visa_out`: roleまたはCompanionがWorld内／World間の許可範囲外
- `authority_unknown`: 必要な制定authorityまたは適用域が確定していない

`scoped_avoid`は普遍的な違法、悪、不正、虚偽の宣言ではありません。「このauthority集合では、この操作を
この経路で実行しない」という局所的な結果です。代替経路が同じ制約を満たすなら、別operationとして
再評価できます。

## 4. UXの外人ムーブ

停止表示は、正義の演説ではなく、適用域と残りの選択肢を返します。

- 派遣・委託: 「この依頼は制定済みの業務範囲外です。この作業だけ引き受けません。」
- SaaS connector: 「このprovider経路ではpolicy範囲外です。local-only経路または別authorityの確認が必要です。」
- ゲームEntity: 「この行為は現在roleのWorld Visa範囲外です。この行為だけ実行しません。」
- Companion: 「対象Worldへの越境権限がありません。現World内の支援は継続できます。」

「自国の基準が正しいので相手Worldも従え」とは表示しません。どの定規がどのscopeに掛かり、どこで
intersectionが空になったかを返します。

## 5. 処理順序

```text
操作要求
  ↓
対象資産・処理経路・World境界を列挙
  ↓
各authorityが提供したscopeを取得
  ↓
全scopeのintersectionを評価
  ├─ matched → proceed
  ├─ conflict → scoped_avoid または isolate
  └─ unknown → require_human_review
```

`isolate`は、local-only処理、別World、別connector、別data residency等へ経路を分ける判断です。
元要求を勝手に意味変換したり、禁止されたdataを迂回送信したりする許可ではありません。

## 6. Registry変更票

```yaml
stable_id: ATL-GOV-SCOPE-001
old_definition: Atlantis横断の明文化済み契約なし
new_definition: authority別の適用域を混ぜず、共通範囲がない案件だけをscoped_avoidする
change_reason: SaaS接続、local資産、国境、World roleの規則を無断継承しないため
enacting_authority: SphereOS Atlantis 0.2.0設計系列
scope: connector、agent、World、Companion、外部service連携
compatibility: additive-alpha
migration_required: false
tests_or_fixtures: 未実装。構造fixtureを後続で追加する
canonical_revision: 本文を追加したcommit
downstream_propagation: AAE／ASTRO／IBDは採用時に各repositoryで適合票を作る
```

## 7. 受入条件

- provider policyと利用者組織policyを別fieldで保持できる
- provider規則をlocal資産全体へ暗黙継承しない
- local規則をprovider serviceへ普遍的に強制したと表示しない
- conflict時に対象operationだけを`scoped_avoid`へ落とせる
- 判断不能を違法・安全・危険へ捏造せず`unknown`で返せる
- World Visaによる停止と現実法上の停止を同じreason codeへ潰さない
- 代替経路は別operationとして再評価し、元の停止receiptを改変しない

## 8. 関連文書

- [Web原典観測・手元ブラウザ退避契約](../development/browser-source-observation.ja.md)
- [意味と器の二重記述憲章](../charter/meaning-and-vessel-dual-register.ja.md)
- [1.x実行系・SDKエンジニア参入ガイド](1x-sdk-engineering-entrypoint.ja.md)
- [贈与コモンズlineageと局所World拡張](gift-commons-lineage-and-local-extension.ja.md)
