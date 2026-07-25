# 贈与コモンズlineageと局所World拡張

状態: `[CANONICAL-CANDIDATE]` `[IMPLEMENTED-ALPHA]`
stable ID: `contract://atlantis/gift-commons-lineage@1`
制定authority: SphereOS Atlantis repository
適用scope: `lineage/contract.json`、`atlantis lineage`、Role／Flavor profile、World extension
上流方針: ZeroRoomLab-manifest `docs/operations/gift-commons-lineage-and-local-world-extension.ja.md`

## 1. 目的

Atlantisは、作者、先行思想、code、神話、信仰、詩、生活様式との関係を、
許可証か犯罪票の二値databaseへ潰さず記録する。

既定は`open-gift-commons-non-exclusive`である。lineageは非競合なrespectと探索のreceiptであり、
所有権、本人性、権威、公式性、API capability、価値rankを生成しない。

Atlantis coreは著作権管理system、宗派の教義庁、本人認証局、marketplace審査部を内包しない。
同時に、個々のasset、配布場所、provider契約、適用法令の条件が消えるとも主張しない。
対象App／integrator／World operatorが、自分の配布・運用scopeへ責任を持つ。

## 2. lineage graph

machine contractは[`lineage/contract.json`](../../lineage/contract.json)を正本とする。

relation:

```text
authored-by / conceived-by / coded-by / practiced-by / observed-by /
derived-from / forked-from / inspired-by / structurally-similar-to /
independent-convergence / homage-to / reinterprets
```

dimension:

```text
byte / code / algorithm / architecture / philosophy /
imagination / poem / faith / lifestyle / aesthetic
```

同じsourceに対して複数relation、複数dimensionを持てる。`structurally-similar-to`は
構造一致の観測であって、copy、独占権、優先順位の自動判定ではない。
`observer_ref`と`claim_scope_ref`を持ち、後から別観測を追加できる。

## 3. asset metadata

receiptは次を要求する。

```text
asset_id
author
source_refs
revision
scope_ref
declared_license
reference_kind
designation
distribution
public_manifest_presence
```

`declared_license`はsource側の宣言を記録する文字列であり、validatorが法的有効性を認証した
という意味ではない。未確認は`unknown`を使える。

### 3.1 aliasとpayload

```text
alias-only
original-payload
third-party-payload
mixed
```

神名、作品名、人物名、宗派名、Role名だけをroute hintとして参照する場合と、
台詞、設定、画像、音声、3D model、weight等のpayloadを運ぶ場合を分離する。
名前だけでpayload同梱へ推定せず、payloadをalias表示で隠さない。

### 3.2 designationとdistribution

designation:

```text
origin / official / compatible / inspired / fan-made / self-authored / unknown
```

distribution:

```text
public / local-only / private / selected-world
```

designationは来歴、distributionは配布状態であり、同じ軸ではない。
`official`は選択scopeの制定authority参照を必要とし、全Worldの公認へ拡張しない。
`compatible`は自己申告で、Origin認定markではない。local-only／private receiptは
`public_manifest_presence=not-required`を正例とし、public repository欠損へ変換しない。

## 4. Role negative contract

すべてのreceiptは次をfalseで宣言する。

```text
identity
authority
api_capability
official_partnership
religious_representation
rights_verdict
```

特定Roleが別contractによる権限を必要とする場合、その権限はRole名から生成せず、
capability／authority／provider bindingを別receiptで解決する。

Raphaelという名前を書いてもroot権限、宗派代表、外部APIは降ってこない。
「天使だから管理者権限です」は神学的にもUnix的にも雑である。

## 5. 狭いproprietary extension

商用App、SaaS、社内asset、provider契約、閉鎖Worldを拒否しない。
proprietary scopeは次のいずれかへ局所化する。

```text
app-local / integrator-local / world-local
```

負例:

- proprietary `open-core`
- `propagates_to_core=true`
- `captures_existing_commons=true`
- `captures_unrelated_worlds=true`
- public receiptへの`api_key`、`token`、`password`等の値

credentialは`secret://...`形式の外部参照だけを受け付ける。validatorはsecret storeへ接続しない。
第三者App／integratorは契約、料金、独自claim、保証、SLAへ責任を持つ。coreはopen extension point、
unmount、fork、alternate Worldを保持する。

## 6. conflictとSemantic Stop

asset競合の停止scopeは`none`または`selected-route`である。

```text
semantic-stop
  -> selected read／presentation／publish／load／execute routeを停止
  -> unmount | replacement | fork | alternate-world
```

asset lineage validatorはglobal stopを生成しない。capability、security、物理安全、法域等の別scopeで
広い停止が必要な場合は、そのauthority、fact scope、根拠を別contractへ記録する。

これは「危険を無視する」意味ではない。城門の事故で大陸全体を停電させる雑なblast radiusを拒否する。

## 7. CLI

contractと同梱fixtureを検証する。

```console
python3 -B -m atlantis_cli lineage validate --json
```

呼出側が明示したreceipt一件だけを検査する。

```console
python3 -B -m atlantis_cli lineage inspect \
  --receipt lineage/fixtures/gift-commons-pass.json \
  --json
```

出力は、rights adjudication、network access、mutation、implicit repository scanを
すべて`false`で返す。

## 8. positive／negative fixture

positive:

- public gift commons
- public Manifestを要求しないlocal-only asset
- coreを囲い込まない狭いcommercial integrator

negative:

- Roleからidentity／authority／API capability／宗派代表性を生成
- proprietary extensionによるopen core／既存commons／別World capture
- raw secret
- asset競合によるglobal stop

## 9. takedown／replacement／fork／alternate World

receiptは、unmount、replacement、fork、alternate Worldのrouteを持つ。
異議が来た場合、target asset、distribution、World、claimant、sourceを解決し、
選択routeを止めてから対象scopeの判断へ進む。

validatorはtakedown要求の法的正しさを裁定せず、削除も実行しない。Git履歴、研究記録、
別Worldを一括焼却する機能も持たない。

## 10. 実装境界

| 対象 | 状態 |
|---|---|
| human-readable contract | `IMPLEMENTED_ALPHA` |
| machine contract | `IMPLEMENTED_ALPHA` |
| explicit receipt validator | `IMPLEMENTED_ALPHA` |
| positive／negative fixture | `IMPLEMENTED_ALPHA` |
| repository asset scan | `NOT IMPLEMENTED` |
| asset auto-mount／priority merge | `NOT IMPLEMENTED` |
| pointer config (`Atlantis.json`等) | `NOT IMPLEMENTED` |
| rights／identity／religious adjudication | `NOT IMPLEMENTED` |
| marketplace／billing gateway | `NOT IMPLEMENTED` |

pointer、loader、priority、signature、cache、FAM migrationは
[#10 明示profileからpointer config／asset loaderへ進むUser Gate](https://github.com/saitoomituru/SphereOS-Atlantis/issues/10)
へ残す。

## 11. 下流波及票

- ZeroRoomLab-manifest: asset metadataとgift-commons policyを制定し、foldlogへUser Gate receiptを保存
- third-party Manifest: 自分が明示するasset receiptと局所World scopeを保持
- third-party App／integrator: provider契約、課金、独自asset、保証、SLAを自分のscopeで保持
- Atlantis core: explicit validator、non-inference、unmount／fork／alternate routeを保持
