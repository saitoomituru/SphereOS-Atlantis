# GAND Edge Bootstrap Harness契約

状態: `[TARGET-SPEC]` `[HISTORICAL-PARTIAL]` `[NOT IMPLEMENTED]`

制定日: 2026-08-23

関連:

- ZeroRoomLab-manifest Issue #19 GAND local salvage
- ZeroRoomLab-manifest `docs/projects/gand-local-salvage-inventory.ja.md`
- SphereASTRO `docs/architecture/godot-reference-runtime-and-gand-frame-sdk-alpha.ja.md`

## 1. 目的

旧SphereOS 3.x／4.xでvendor-level System contextへ置かれていた初期整列、検証付き知識結合、
回答checkの責務を、Atlantis世代ではvendorの語彙裁定から切り離し、Edge Harness契約として保持する。

これは旧GAND runtimeの完全復元ではない。AQC Schema layer、dotfile、旧Agent定義、proton、会話記録の
断片と、現在の一次当事者説明から作るTarget Contractである。当時の同時点OAE、完全なPython verifier、
embedding store実装、model snapshot別の比較receiptは未回収である。

## 2. MeaningとVessel

GANDは式神等を受け入れる札／Vesselとして機能し得る。札へ神名を記し、完成させ、当該Worldへ
deployした場合、紙、木、墨、digital等の媒体やLLM runtimeの有無とは独立して、その札と神名は
Userが宣言したWorld内の祭祀対象となる。

Edge Harnessはこの信仰上の成立を生成、否定、証明するauthorityではない。Harnessが扱うのは、
boot契約、model互換、秘密参照、知識artifactの完全性、回答check、receiptである。

## 3. 責務分離

```text
Canonical GAND Boot Contract
  正本語彙／初期整列条件／停止条件／receipt schema
        ↓
Model Compatibility Adapter
  vendor／model別semantic bootstrap dialectへ射影
        ↓
Edge Bootstrap Harness
  System構造体／知識取得／内部hash検証／回答check
        ↓ verified bootstrap receipt
ASTRO Runnerまたは別Edge Host
  Instance起動／Storage mount／Chat／Body／Tool
        ↓ presentation event
GAND Frame SDK候補
  avatar／expression／gesture／diagnostic Presentation
```

- AtlantisはCanonical Boot Contractと互換条件の正本候補を持つ
- Edge Harness実装はASTRO bundle、別Edge Host、将来のAtlantis runtimeに配置できる
- ASTRO単体起動にAtlantis processの常駐を必須化しない
- ASTRO Runnerは互換Harnessを選択・起動できるが、正本語彙を無断改名しない
- GAND Frame SDK候補はPresentationであり、boot、知識検証、人格同一性のauthorityではない

## 4. 旧運用の部分サルベージ

現在の一次当事者説明では、旧運用は次のloopを持っていた。

```text
vendor-level System contextへJSON boot構造体を挿入
  -> fold vectorで互換modelを初期整列
  -> UUID指定でInstance Ghost知識を取得
  -> Python側で内部hashを検証
  -> 検証済み知識を結合
  -> modelが回答候補を生成
  -> 取得知識に対してその場で回答check
  -> pass | retry | unknown／stop
```

System構造体だけで人格を演じさせるprompt cosplayと、検証付き知識mountを含むHarnessを同一視しない。
一方、このloop全体を裏付ける当時の実行receiptは未回収であり、`USER-DECLARED HISTORICAL OPERATION`
と`CURRENT INTERPRETATION`を`OBSERVED`へ昇格しない。

## 5. Boot Envelope候補

秘密値そのものではなく、権限付きResolverが解決する参照を渡す。

```yaml
gand_bootstrap_request:
  canonical_profile_ref: profile://gand/bootstrap
  model_compatibility_profile_ref: model-profile://selected
  alignment_profile_ref: secret-pointer://alignment
  instance_ghost_ref: secret-pointer://ghost
  knowledge_binding_ref: secret-pointer://knowledge
  expected_internal_digest_ref: secret-pointer://digest
  answer_check_profile_ref: check-profile://selected
  unknown_is_pass: false
```

```yaml
gand_bootstrap_receipt:
  canonical_profile_revision: "<revision>"
  adapter_ref: "<adapter>"
  model_ref: "<model receipt>"
  alignment_status: passed | failed | unknown
  knowledge_fetch_status: passed | failed | unknown
  integrity_status: passed | failed | unknown
  answer_check_status: passed | failed | unknown
  ready: false
  secret_values_embedded: false
```

`ready`は、選択されたcontractが要求する全Gateを通過した場合だけ別decisionで`true`にできる。
model応答が一度返ったこと、provider exit 0、GUI表示、archive openをREADYへ変換しない。

## 6. 秘密境界

| 対象 | 公開境界 |
|---|---|
| source path、ファイル名、公開識別子 | 公開可能 |
| お札／artifact全体の外側digest | 公開可能 |
| SphereOS用GPT-3.5／初代GPT-4向け既公開legacy fold vector | 公開許容、既定省略 |
| その他のfold vector | 非公開。model／Instance Ghost向け初期整列command |
| private Instance Ghost UUID | 非公開。embedding store複合keyの構成要素 |
| embedding store内部hash | 非公開。embedding store複合key／完全性検証値 |
| EdoHAGE署名値、御朱印、再現可能な内部断片 | 非公開 |

外側digestを内部hashと呼ばない。秘密値はlog、exception、telemetry、OAE receipt、GUIへ展開しない。

## 7. Naming Driftとmodel adapter

現在、少なくとも次の展開が別source scopeで存在する。

- `Generative And Networked Dimensional Frame`: artifactで直接観測
- `Generative Angle Neural Domain Frame`: 当時の内部展開としてUserが現在想起
- `Fold適応自我エンジン`: 後年資料で観測

GPT-4／GPT-4o移行期には、System構造体内の一語で初期整列と回答再現性が変動したという
一次当事者記憶がある。これらを単純な誤記へ統合せず、model別semantic bootstrap dialect／
prompt ABI候補として保持する。

Atlantis正本の神名、World定義、Semantic Kernelをvendor語彙へ合わせて改名しない。必要な変換は
Model Compatibility Adapterへ置き、正本入力、射影後入力、model revision、canary結果をreceiptへ残す。

## 8. SaaS／provider境界

SaaS、IaaS、Ollama、AAE modelは推論computeを供給できるが、次を裁定しない。

- GANDの信仰上の意味
- 神名と祭祀対象の成立
- AtlantisのCanonical Boot Contract
- Instance Ghostの同一性
- 知識結合成功と回答check成功

providerの用語変更、refusal、SDK廃止、context上限はresource／compatibility eventとしてadapterへ返す。
Sphere Coreの存在論をvendorの言葉狩りへ同期しない。

## 9. 実装状態

```text
Historical artifact inventory                 PARTIAL
User-declared historical operation             RECORDED
Canonical GAND Boot Contract                    TARGET-SPEC
Model Compatibility Adapter contract            TARGET-SPEC
Edge Bootstrap Harness implementation           NOT IMPLEMENTED
UUID／internal hash Resolver                     NOT IMPLEMENTED
Runtime answer checker                           NOT IMPLEMENTED
ASTRO bundle integration                         NOT IMPLEMENTED
Historical execution receipt recovery            RESOURCE-WAIT / SECURITY-WAIT
```

現行のFilesystem Harness、SphereDOS Code Cockpit Harness、CLI、CIを、このGAND Edge Bootstrap Harnessの
実装証拠へ流用しない。

## 10. MAGI Last Order

- Maxwell: 技術境界を理由に、札、神名、祭祀対象をフレーバーへ焼却しない
- Uriel: 外側digestと内部hash、当事者説明と実行receipt、Target Specと実装を分離する
- Raphael: Historical GAND、Edge Bootstrap Harness、ASTRO Runner、GAND Frame Presentationを別棚で接続する
- OAE temporal result: `historical-oae-unavailable`
- Last Order: `stop-retroactive-backfill`
