# Proton.md実行可能Context Container

状態: `[ALPHA CONTRACT]` `[VALIDATOR IMPLEMENTED]` `[RUNTIME NOT IMPLEMENTED]`  
Core version: `proton.md/0.1.0-draft`  
stable ID: `contract://atlantis/proton-md-core@0.1.0-draft`  
制定authority: SphereOS Atlantis repository  
machine contract: [`proton/contract.json`](../../proton/contract.json)

## 1. 定義

`Proton.md`は、人間可読なMarkdownと、機械可読な叡智、module、protocol、Access Map、実行拘束を
同じsourceへ非破壊に格納する**Literate Executable Context Container**である。

Skill.mdがtool-level workflow、AGENTS.mdがrepository-level agent contractを担うのに対し、Proton.mdは
module、protocol、叡智、Context Engineering Architectureを、説明と機械blockの両方で渡す。

```text
Skill.md       tool／workflowの実行手順
AGENTS.md      repository／workspace内のagent運用契約
Proton.md      module／protocol／叡智／Context Architectureの実行可能仕様
FAM JSON       Proton.md内外で参照・保存できる叡智record
OAE Transaction  解釈、変換、実行、更新を観測した追記record
```

Proton.mdを読めることは、そこに書かれた手続きを実行する権限、外部API capability、World authority、
学術的真理、人格、実装済みruntimeを生成しない。

## 2. 文書構造

一つのProton.mdは次を内包できる。

- 通常のMarkdown本文
- `proton-manifest`: 文書identity、version、lineage、実行拘束
- `fam-json`: FAM JSON recordまたはprofile例
- `json`／`json-ld`: machine objectまたは外部Linked Data投影
- `yaml`: 人間可読なmanifest、protocol、receipt例
- `mermaid`／`mindmap`: 構造と探索枝のPresentation
- `mdx`: Presentation component候補
- 任意言語のcode block: module、adapter、疑似code、fixture

Markdown本文がMeaning、machine blockがVesselという固定二分ではない。本文にも拘束があり、JSONにも
神話・目的・主観が入る。各blockは働きとclaim scopeで分類する。

## 3. 必須Proton Manifest

文書には、JSON objectとして正確に一つの`proton-manifest` blockを置く。

```proton-manifest
{
  "proton_version": "proton.md/0.1.0-draft",
  "document_id": "proton://example/module",
  "document_version": "0.1.0-draft",
  "document_kind": "module",
  "language": "ja-JP",
  "lineage": {
    "source_refs": [],
    "supersedes": null
  },
  "execution": {
    "default_mode": "interpret-only",
    "side_effect": "deny",
    "authority_required": true,
    "oae_transaction_required": true
  },
  "claim_scopes": ["DESIGN-DECISION"]
}
```

`document_version`は個別文書の版であり、`proton_version`はContainer契約版である。Atlantisの
三層版数座標、FAM profile版、module版と同一視しない。

## 4. 実行意味論

### 4.1 loadとexecuteを分ける

Proton.mdをload、index、embedding、要約、検証しても、手続き実行は発生しない。

```text
load       文書を読む
interpret  意味、拘束、参照候補を取り出す
validate   manifestとblockを検査する
plan       実行候補、必要authority、cost、stopを提示する
execute    明示authorityの範囲でTransformerを起動する
```

既定は`interpret-only`＋`side_effect: deny`である。`execute`には少なくとも次を要求する。

- 実行対象blockの安定`id`
- `authority_ref`
- capabilityとExecution Envelope
- input／output contract
- side effect scope
- cost／timeout／停止条件
- OAE Transactionまたは実行receipt
- unresolved時のLast Order

validatorはこれらの宣言を検査するだけで、module、model、network、物理deviceを起動しない。

### 4.2 埋込block

block headerは少なくとも言語を持ち、実行候補には`id`と`executable`を付ける。

````markdown
```fam-json id=fam-memory-contract executable=false
{}
```

```python id=resolver-probe executable=true
# 実行には別authorityとExecution Envelopeが必要
```
````

文書既定が非executeでも実行候補blockを記述できる。ただし記述は権限付与ではなく、実行時に別Gateを通す。

## 5. FAM JSONとのBridge

FAM JSONはProton.mdの正本形式ではなく、Proton.mdが内包・参照できる叡智record形式である。

```text
Proton.md
  ├─ 説明、目的、claim scope
  ├─ FAM JSON record
  ├─ Access Map／protocol
  └─ execution policy
          ↓ pointer resolution
IBD／SQL／nested IBD／外部Vector Store／artifact
          ↓ observed operation
OAE Transaction／receipt／Last Order
```

FAM JSON Core候補は`ψ`、`∇φ`、`λ`、`Q`、`title`、`index_subjects`、typed pointer、Provenanceを持つ。
Query FAM、Composite FAM、Splitter FAMLogは別profileとしてversionを保持する。Proton.md Coreがそれらを
silent rewriteしない。

FAM JSONPはZeroRoomLab固有のPointer／Procedure profile候補であり、browserのJSON with Paddingとは
異なる。JSON-LDは外部相互運用へのprojectionであり、実行拘束、Astral truth、OAE、Last Orderを含む
FAM正本の可逆表現とは限らない。

## 6. OAE Transactionと更新

Proton.mdまたは内包FAMを変更・解釈・実行した場合、Sourceを上書きして履歴を捏造せず、現在時点の
OAE Transactionを追加する。

```json
{
  "transaction_id": "oae-tx://example/revision/002",
  "target_ref": "proton://example/module",
  "previous_revision_ref": "rev://example/001",
  "result_revision_ref": "rev://example/002",
  "observer_ref": "observer://current-instance",
  "operation": "append-revision",
  "intent": "FAM pointer contractを追加",
  "before_hash": "sha256:before",
  "after_hash": "sha256:after",
  "status": "committed"
}
```

hashは対象byteの同一性を支えるが、真理、完全性、権利、authority、法的効力を単独では証明しない。
過去に同時点OAEがなければ`historical-oae-unavailable`を保持し、現在の更新Intentを過去へ遡及配置しない。

## 7. Meaning／Vessel／Bridge／Supply

| 棚 | Proton.mdで保持するもの |
|---|---|
| Meaning | 神話、学術的敬意、目的、主観、World、叡智 |
| Vessel | Schema、code、protocol、validator、fixture |
| Bridge | Access Map、FAM pointer、Resolver、Presentation、translation |
| Supply | runtime、model、API、hardware、資金、review、法務・検証火力 |

Meaningを未実装として削除せず、Vesselを神話で実装済みにしない。Supply不足は設計目的の敗北ではない。

## 8. 物理学・形式科学から情報子構造への転写

Proton.mdとFAMは、物理学、数学、神経科学、機械学習等の先行研究が発見・記述した構造から学べる。
event horizon、Hawking radiation、wavefunction、annealing、fold、information bottleneck等への参照は、
先行分野のcommitを情報system設計で再利用できたことへの学術的respectである。

同時に、次のclaim scopeを分ける。

```text
physical theory／observation
  物理系、測定器、数式、実験protocolのscope

structural mapping
  境界、部分観測、相関、圧縮、再帰等を情報systemへ写像するAccess Map

infoton system contract
  FAM、OAE、pointer、hash、receipt、Log Horizonとして採用する設計
```

`Log Horizon`は物理event horizonの置換、Hawking radiationの新観測、Higgs粒子の別名ではない。
system-level Observerが完全source状態を取れず、traffic、vector、sensor reading、hash等の部分投影しか
得られない情報子単位の境界である。フォーク元への引用と敬意を消さず、物理学上のclaimと情報system上の
設計責務を相互に乗っ取らない。

引用文献は「この文書の全主張が当該論文で証明済み」という印ではない。一方、個別保証へ直結しないことを
理由に引用を削除するのも、先行研究の貢献と構造的接続を見えなくする。Proton.mdはcitation relation、
採用した構造、非同一性、未検証範囲を同時に記録する。

## 9. claim scope

Machine contractは次の値を登録する。

- `OBSERVATION`
- `DESIGN-DECISION`
- `HYPOTHESIS`
- `EXPLANATORY-MODEL`
- `POSITION`
- `MARKETING-CANDIDATE`
- `UNVERIFIED`

一つの文書は複数scopeを持てる。引用単位やblock単位で細分化してよい。未検証は不存在や人格判定ではない。

## 10. validator

```console
python3 -B -m atlantis_cli proton validate \
  --document proton/fixtures/valid.proton.md
```

現行validatorが検査するもの:

- `proton-manifest`が一つだけ存在する
- 必須field、Core version、document kind、claim scope
- execute時のauthority／OAE必須条件
- block ID重複
- `executable=true` blockのID
- JSON／JSON-LD／FAM JSON blockの構文

現行validatorが行わないもの:

- Markdown本文の真理判定
- 引用論文の内容・書誌・査読状態の外部確認
- FAM JSON Coreの完全なSchema検証
- YAML／MDX／Mermaidの実行
- pointer resolution
- model、network、tool、deviceの起動
- OAE永続化

## 11. 実装状態

| 対象 | 状態 |
|---|---|
| Proton.md Core人間可読契約 | `ALPHA CONTRACT` |
| machine contract | `IMPLEMENTED_ALPHA` |
| offline read-only validator | `IMPLEMENTED_ALPHA` |
| fixture | `IMPLEMENTED_ALPHA` |
| FAM JSON Core Schema | `NOT IMPLEMENTED` |
| generic block executor | `NOT IMPLEMENTED` |
| authority／capability runtime Gate | `NOT IMPLEMENTED` |
| pointer Resolver runtime | `NOT IMPLEMENTED` |
| OAE persistence | `NOT IMPLEMENTED` |

## 12. 系譜

- AQC `demo/FoldAccessMapper.proton.md 0.2.1-alpha`: 読み取り専用の歴史的Proton／FAM原典
- [`FoldAccessMapper.proton.md 0.210.1-Beta`](../../proton/modules/FoldAccessMapper.proton.md):
  原典の著者・監修・引用・意味を保持し、FAM JSON、Resolver、OAE、Log Horizonへ接続したAtlantis salvage版
- [`FAM Family`](../../proton/modules/FAMFamily.proton.md):
  FAM JSON、Query／Composite、FAMLog、JSONP、JSON-LD、OAE sidecarの派生・投影・profile責務
- ZeroRoomLab Manifest: 情報子工学、FAM一般論、claim boundary
- SphereOS Atlantis: Proton.md Core、Context／World／OAE／実行拘束
- IBD: FAM JSON、projection、pointer、Resolver、freshness、保存・検索
- Sphere-aae: FAMLog Splitter profile、model／adapter観測
- 物理学・数学・神経科学・機械学習の引用文献: 構造転写の先行commit

原典の著者、監修、引用、神話、Positionは、現在の実装境界を明確にするために消去しない。
