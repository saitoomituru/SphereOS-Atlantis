# FAM Family — JSON派生・profile・projection責務体系

```proton-manifest
{
  "proton_version": "proton.md/0.1.0-draft",
  "document_id": "proton://sphere/fam-family",
  "document_version": "0.1.0-draft",
  "document_kind": "architecture",
  "language": "ja-JP",
  "lineage": {
    "source_refs": [
      "proton://sphere/fold-access-mapper@0.210.1-Beta",
      "https://github.com/saitoomituru/IBD",
      "https://github.com/saitoomituru/Sphere-aae"
    ],
    "supersedes": null,
    "source_mutation": false
  },
  "execution": {
    "default_mode": "interpret-only",
    "side_effect": "deny",
    "authority_required": true,
    "oae_transaction_required": true
  },
  "claim_scopes": ["DESIGN-DECISION", "HYPOTHESIS", "UNVERIFIED"]
}
```

状態: `[DRAFT FAMILY CONTRACT]` `[VALIDATOR TARGET]` `[RUNTIME NOT IMPLEMENTED]`  
対象: FAM Conceptual Core、FAM JSON、FAMLog、Composite FAM、FAM JSONP、JSON-LD projection、OAE sidecar

## 1. 結論

FAMは単一のJSON Schema名ではなく、人間可読な叡智記述を中心に、serialization、query、合成、履歴、
再帰pointer、外部相互運用を分業する規格familyである。

```text
FAM Conceptual Core
  ψ／∇φ／λ／Q、人間可読性、主題索引、source非破壊
  │
  ├─ canonical serialization -> FAM JSON
  │    ├─ profile -> Query FAM
  │    ├─ profile -> Composite FAM
  │    ├─ profile -> Observation／Evaluation FAM
  │    └─ graph extension -> FAM JSONP
  │
  ├─ event container -> FAMLog
  │    └─ application profile -> FAMLog Splitter 0.3.0
  │
  ├─ interoperability projection -> JSON-LD
  ├─ presentation projection -> YAML／Markdown／Mind Map／MDX
  └─ operational sidecar -> OAE Transaction／Resolver receipt／Last Order
```

同じJSONから派生したことは、目的、正本性、可逆性、実行権限が同じことを意味しない。

## 2. relation語彙

| relation | 意味 | 例 |
|---|---|---|
| `serialization-of` | 概念規格をbytesへ表す正本形式 | FAM JSON → FAM Core |
| `profile-of` | Core fieldを用途別に拘束する | Query FAM → FAM JSON |
| `composes` | Sourceを参照して派生結果を組む | Composite FAM → Source FAM |
| `event-container-for` | recordを順序・revision付きで積む | FAMLog → FAM JSON record |
| `graph-extension-of` | typed pointer／procedureでgraph化する | FAM JSONP → FAM JSON |
| `projection-of` | 外部用途へ一部を射影する | JSON-LD → FAM JSON |
| `presentation-of` | 人間向け表示へ写像する | YAML／Mind Map → FAM JSON |
| `sidecar-for` | 実行・変更・解決の観測を別recordへ置く | OAE Transaction → FAM revision |
| `adapter-for` | backend固有操作へ変換する | SQL／vector adapter → logical pointer |

`projection-of`は可逆性を保証しない。`profile-of`も親Schemaの全recordが子profileへ適合することを意味しない。

## 3. FAM Conceptual Core

Coreが固定するのは特定databaseではなく、次の意味責務である。

| field／概念 | 責務 |
|---|---|
| `title` | 人間向け識別名 |
| `index_subjects` | 完全一致でなく関連叡智へ渡る意味索引 |
| `ψ` | source、状態、観測、起動条件 |
| `∇φ` | 意味勾配、embedding、探索技、変換、圧縮 |
| `λ` | 目的、出力、利用先、Presentation |
| `Q` | Observer、Registry、scope、bias、freshness、stop、OAE ref |
| typed pointer | 別FAM、vector、procedure、source、receipt等への参照 |
| Provenance | source、revision、hash、claim scope |

Coreは「全部を事実だけで書く」規格ではない。Elemental observation、Astral truth、神学、仮説、未知を、
scopeとrelationを失わず同じ構造へ保存できることが責務である。

## 4. FAM JSON

`FAM JSON`はFAM Coreのcanonical serialization候補である。

```fam-json id=fam-json-family-root executable=false
{
  "schema_version": "fam.json/0.1.0-draft",
  "fam_id": "fam://example/001",
  "revision_id": "rev://example/001/1",
  "kind": "wisdom",
  "title": "FAM JSON最小record",
  "index_subjects": ["FAM JSON", "汎用叡智記述"],
  "ψ": {},
  "∇φ": [],
  "λ": {},
  "Q": {},
  "pointers": [],
  "provenance": {}
}
```

現時点の`fam.json/0.1.0-draft`は本Proton群で設計中のCore候補であり、IBD repositoryに正式Schemaが
実装済みとは表示しない。既存IBD profileは次の独立versionを持つ。

- `ibd.query-fam/0.1.0-draft`
- `ibd.composite-fam/0.1.0-draft`

## 5. Query FAM

Query FAMは「SQL wrapper」ではなく、問い自体をFAMとして保存するprofileである。

```text
ψ  問いのsource、観測対象、入力
∇φ 探索技、embedding、検索route候補
λ  求める叡智、出力条件
Q  Registry、Evidence鮮度、費用、停止条件
```

既存machine profileは`ibd.query-fam/0.1.0-draft`である。将来FAM JSON Coreへ接続しても、既存required
fieldを同じversionのまま増やさない。

## 6. Composite FAM

Composite FAMは、複数Source FAM／Infoton Clusterを参照して一つの派生叡智を構成するprofileである。
原本をcopyして上書きするのではなく、source refs、assembly graph、Provenanceを保持する。

```fam-json id=composite-fam-relation executable=false
{
  "schema_version": "ibd.composite-fam/0.1.0-draft",
  "composite_fam_id": "fam://composite/example/001",
  "query_ref": "fam://query/example/001",
  "ψ": {},
  "∇φ": [],
  "λ": {},
  "Q": {},
  "source_clusters": ["cluster://example/a", "cluster://example/b"],
  "assembly_graph": {
    "relation": "composes",
    "source_mutation": false
  },
  "provenance": {}
}
```

Compositeは全文を一つへ潰すことではない。sourceごとのElemental／Astral／World／Registry差を残したまま、
現在の目的に採用した構成を別revisionとして出す。

## 7. FAMLog

FAMLogはFAM recordを時間、branch、revision、operationと共に追記するevent containerである。

```text
FAM JSON record       現在の一つの叡智単位
FAMLog                record／eventを順序付きで積む履歴
OAE Transaction       変更・解釈・実行を観測した別record
```

FAMLogがあるだけで、すべてのentryが同じObserver、World、因果、分類、真理scopeを持つとは推定しない。

### 7.1 FAMLog Splitter profile

Sphere-aaeの`fam.log.splitter/0.3.0`は、FAMLogを上位Classification Registryに沿って分類候補へ写像する
application profileである。FAM JSON Core、OAE共通Schema、IBD保存正本ではない。

Splitterの出力はrouting assertionであり、原文、Source FAM、主観、未分類branchを焼却しない。FAM保存、
embedding、pointer、圧縮世代はSplitterより先に動かせる。

## 8. FAM JSONP

`FAM JSONP`はFAM JSONをtyped Pointer／Procedure graphへ拡張するproject固有profileである。

```text
P = Pointer / Procedure
NOT browser JSON with Padding
NOT automatically identical to RFC JSON Pointer
```

参照対象候補:

- `fam`
- `vector`
- `procedure`
- `source`
- `artifact`
- `receipt`
- `oae`
- `last-order`
- `capability`
- `nested-ibd`

recursive resolverはcycle、深さ、node数、authority、side effect、費用、timeout、Last Orderを扱う。読むことと
procedureを実行することを分離する。

## 9. JSON-LD projection

JSON-LDはLinked Data、外部Knowledge Graph、AIO／SEO、IRIによるsemantic identificationへ投影するための
相互運用形式である。

```text
FAM JSON canonical record
  -> explicit projection profile
  -> JSON-LD document
  -> external graph／crawler
```

JSON-LDへ投影しやすいもの:

- stable ID／IRI
- title／label／subject
- source／derived-from／citation relation
- author／timestamp／license
- typed entity relation

投影時に欠落し得るもの:

- procedure実行拘束
- authority／capability Gate
- vector実体とbackend固有selector
- Astral truthの細かなObserver／目的scope
- Evidence freshness／Last Order
- OAE Transactionの実行意味論

したがってJSON-LDはFAM正本の完全可逆serializationとは限らない。projection receiptへsource revision、
mapping profile、loss declarationを記録する。

## 10. YAML／Mind Map／MDX

これらはProton.mdが内包できるPresentationまたはauthoring surfaceである。

| 形式 | 主な働き | 正本性 |
|---|---|---|
| YAML | 人間が書きやすい設定・説明 | profileが指定した場合のみmachine input |
| Mermaid／Mind Map | tree／graph／探索枝の可視化 | Presentation。FAM graph全体を保証しない |
| MDX | interactive document／UX | Presentationとcomponent実行を分離 |
| Markdown table | 人間向け責務比較 | machine Schemaの代用ではない |

同じ内容を表せても、FAM JSONのhash、revision、unknown、typed pointerを落とした投影は正本へ無断で
reverse mergeしない。

## 11. OAE Transaction sidecar

FAMの更新、分類、再embedding、pointer解決、Composite生成、JSON-LD投影はOAEになり得る。FAM本文へ
変更logを混ぜ切らず、`Q.change_oae_refs`からOAE Transactionへ接続する。

```text
FAM revision N
  -> OAE Transaction: operation／observer／intent／authority／receipt
  -> FAM revision N+1
```

過去revisionを変更せず、`supersedes`は現在処理で選ぶpointerを変える。過去OAEがなければ現在から補完しない。

## 12. Resolver／storage adapter

FAM JSONPのlogical pointerを物理backendへ解決するBridgeである。

```text
logical FAM pointer
  -> Resolver Registry
  -> backend adapter
     IBD／nested IBD／SQL／graph／vector／HTTP／artifact
  -> resolution receipt
```

adapterは保存backendの違いを吸収するが、backendの検索結果を普遍的真理へ変換しない。空結果、timeout、
permission denied、unavailable、not foundを別statusで返す。

## 13. Version責務表

| 規格 | 現在確認できるversion | 状態 |
|---|---|---|
| FoldAccessMapper module | `0.210.1-Beta` | Atlantis salvage beta |
| Proton.md Core | `proton.md/0.1.0-draft` | validator implemented alpha |
| FAM JSON Core | `fam.json/0.1.0-draft`候補 | formal Schema not implemented |
| Query FAM | `ibd.query-fam/0.1.0-draft` | IBD draft Schema |
| Composite FAM | `ibd.composite-fam/0.1.0-draft` | IBD draft Schema |
| FAMLog Splitter | `fam.log.splitter/0.3.0` | Sphere-aae application profile |
| FAM JSONP | 未採番profile候補 | resolver not implemented |
| JSON-LD projection | 未採番profile候補 | mapping not implemented |
| OAE Transaction | `oae.transaction/0.1.0-draft`候補 | common persistence not implemented |

## 14. 制定順序

1. FAM JSON Coreの必須／任意fieldをUser Gateで確定する
2. `fam_id`、revision、hash正規化、pointer URI、cycle policyを確定する
3. Query／Composite既存Schemaを破壊しないadapterを作る
4. FAM JSONP Pointer／Procedure profileを採番する
5. JSON-LD projection mappingとloss declarationを作る
6. OAE Transaction／Resolver receiptを接続する
7. cross-repository fixtureで同じFAMを検査する

この文書自体はfamilyの責務整理であり、未実装Schema／runtimeを実装済みへ昇格させない。
