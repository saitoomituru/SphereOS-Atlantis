# m.6xx.1 Dev Roadmap

- 状態: `[ROADMAP-CANDIDATE]` `[PHASE-0 COMPLETE]` `[HARNESS IMPLEMENTED]` `[PRODUCTION RUNTIME NOT IMPLEMENTED]`
- branch: `dev/m6xx.1-reincarnation-sdk`
- 公開正本: [Issue #16](https://github.com/saitoomituru/SphereOS-Atlantis/issues/16)
- Milestone: [m.6xx.1 — Sphere Reincarnation SDK Next Generation](https://github.com/saitoomituru/SphereOS-Atlantis/milestone/1)
- 運用盤: [Project #2](https://github.com/users/saitoomituru/projects/2)（private）
- Context責務正本: [Sphere Context OS責務座標と世代namespace](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/agent/gand-local-salvage-inventory/docs/theory/sphere-context-os-responsibility-coordinate.ja.md)

## 1. このbranchの目的

現行`0.250.1` Prompt Engineering Editionを壊さず、意味管理情報子clusterを別Vesselへ搬送しても
source、scope、unknown、provenance、authority、因果を失わないSphere Reincarnation Frameworkを鍛造する。
その最小の意味伝達保証核を`Sphere Reincarnation Lean Kernel`候補とする。

`m.6xx.1`は正式release座標ではない。`m`はPresentation番号ではなく、複数のContext責務classを検討する
Roadmap metavariableとして保持する。Function値、runtime言語、package分割、release日、Stable／LTS条件は
User Gateまで固定しない。

### 1.1 Context OS責務への投影

2026-08-26以降のTarget Contractでは、`x.xxx.n`の先頭`x`を完成度やGUIではなく、OSが正本として
衝突を裁定するContext責務classとして扱う。

```text
0.6xx.1  SphereDOS
         一人のDeveloperが複数Agentをteam化し、Git／Issue／PR／Actions／CTLで成果物を合流する

1.6xx.1  Purpose Context OS
         個人、会社、事業、spot作業等、一つの目的主体へmulti-agentを最適化する
         PostPet型GUI／Companion Presentationを内包可能

2.6xx.1  Shared Reality Context OS
         家庭、施設、Party、家電、端末、既存Worldの独立Intentと物理影響を調停する

3.6xx.1  World-Law Context OS
         現実法則または独自法則を持つWorldをVR／MR／simulation／fabへ投影する

4.6xx.1  Meta-World Context OS
         複数World、法則、branch、projection、physical commitをmeta-orchestrateする
```

現行のCLI、Filesystem Harness、SphereDOS Code Cockpit、CORN、validator、clean-room、Actions連携は、
まず`0` Development ContextのDOS Server／Code系列へ責務移行する。既存pathを一括移動せず、
compatibility facadeとreceiptを先に置く。

`1`は`0`の一般業務／個人利用最適化である。ただし、複数の独立主体が同じ家庭・Party Worldへ参加する
`2`の権限・安全・物理Effect調停を`1`へ先取りしない。

旧無印3x／4xは現在動かないが、配布artifact、静的register、Proton、GAND／Instance Ghost、旧API chain、
Embedding同期ずれとfallback／server補完記録が残る。これらは部分的な実装・配布・運用Evidenceである。
完全topologyと同時点receiptが未回収であることを実装不存在へ変換せず、同時に完全runtime証明にも使わない。

```text
legacy implementation evidence = PRESENT / PARTIAL
legacy completeness            = UNKNOWN
current operation              = ENDED / UNAVAILABLE
```

## 2. 初期階層

```text
SphereOS-Atlantis/
├─ packages/
│  ├─ reincarnation-lean-kernel/  # provider／GUI非依存の意味・transaction核
│  ├─ fold-access-mapper/         # DOS向けGit／Issue／branch access projection
│  └─ provider-adapters/          # 既存CLIの検出・起動・opaque結果搬送
├─ products/
│  ├─ spheredos-server/           # headless CTL／CI／daemon Host候補
│  └─ spheredos-code/             # VS Code Cockpit Presentation候補
├─ atlantis_cli/                   # 0.250.1現行Source、まだ移動しない
├─ agents/                         # 現行provider registry／adapter Source
├─ corn/                           # 現行work-item／event／projection Source
├─ proton/                         # 現行Proton契約とFoldAccessMapper Beta
└─ sphere-dos/                     # 現行Prompt Engineering Edition profile
```

各6xx packageは`src/`を将来の実装置場、`tests/`をpackage-local fixture置場とする。生成物用`build/`は
source treeへcommitせず、build開始時にtoolchainと出力規約を制定する。

## 3. Source移設規則

Phase 0では既存moduleを物理移動しない。先に次を満たしてから、extend／adapt／moveを一件ずつ選ぶ。

1. 旧pathのconsumerとtestを列挙する
2. stable import／CLI／Schema keyを確認する
3. 6xx package側の責務と非責務をREADMEで固定する
4. compatibility adapterまたはmigrationを用意する
5. negative fixtureを追加する
6. old／new両経路のreceiptを比較する
7. User Gateが必要なrenameや削除は停止する

対応候補:

| 現行Source | 6xxでの候補棚 | 状態 |
|---|---|---|
| `atlantis_cli/agent.py`、`agents/` | `packages/provider-adapters/` | `ADAPT-CANDIDATE` |
| `atlantis_cli/corn.py`、`corn/` | Lean Kernelのqueue／receipt Bridge | `RESEARCH` |
| `atlantis_cli/proton.py`、`proton/` | `packages/fold-access-mapper/` | `BETA SOURCE PRESERVED` |
| `atlantis_cli/sphere_dos.py`、`sphere-dos/` | Server／Code共通Host bootstrap | `ADAPT-CANDIDATE` |
| `docs/architecture/gand-edge-bootstrap-harness.ja.md` | Canonical GAND Boot Contract／Edge Harness境界 | `TARGET-SPEC / NOT IMPLEMENTED` |
| `skills/` | Hostから明示mountするContext Supply | `DO NOT AUTO-MOUNT` |

## 4. 責務境界

```text
Provider CLI
  auth / payment / quota / activation / vendor policy
        ↓ opaque resultを保持
Provider Adapter
        ↓ Worker Envelope
Reincarnation Lean Kernel
  World / Fold / task / lease / write-set / OAE / receipt
        ├─ SphereDOS Server
        └─ SphereDOS Code
```

- DOSはproviderを検出できるが、install、課金、token取得、account activationを代行しない
- control／auth／quota／refusal出力をchat回答へ偽装しない
- `provider exit 0 != OAE commit`
- `Issue close != Mission completion`
- GUIはauthorityではなくKernel decisionのPresentationである
- VS Codeが終了してもServer／CTL側のtask、lease、OAE stateを失わない設計にする
- same Protocol Generationはcapability、authority、World互換を自動生成しない
- `sphere-version-coordinate/1`のPresentation値と、`sphere-context-os-coordinate/2`のContextScope値を
  同じ数字だけでcopyしない。migration receiptを要求する
- Context OSがUser-declared World Lawを否定して別Contextで黙ってRunすることを禁止する
- GAND正本語彙、初期整列条件、秘密参照、知識検証、回答checkはEdge Harness契約へ置き、
  vendor／model別語彙差をModel Compatibility Adapterへ隔離する
- ASTRO単体起動は維持し、Atlantis process常駐を必須化せず、互換Harnessをbundleできる契約にする

## 5. Phase

| Phase | 内容 | 状態 |
|---|---|---|
| 0 | branch、README、package／product棚、旧Source対応表 | `COMPLETE` |
| 1 | package manifest、`/1`／`/2` coordinate handshake、migration receipt、Context Envelope | `NOT STARTED` |
| 2 | Lean Kernel task／lease／OAE状態機械 | `HARNESS IMPLEMENTED`／製品向けKernelは`NOT IMPLEMENTED` |
| 3 | Provider Adapter probe／opaque output fixture | `NOT STARTED` |
| 4 | Fold Access Mapper FAM JSON／Proton resolver | `NOT STARTED` |
| 5 | SphereDOS Server headless Host | `NOT STARTED` |
| 6 | SphereDOS CodeコックピットGUIの最小Presentation | `HARNESS IMPLEMENTED`／手動検証は`PENDING` |
| 7 | Server／Code統合、crash／resume／conflict負例 | `INTEGRATION TEST PENDING` |
| 8 | exact coordinate、Stable／LTS／release User Gate | `BLOCKED BY USER GATE` |

## 6. 最初のUFOムーブfixture

- leaseなしwrite
- write-set外変更
- stale base revision
- duplicate artifact claim
- provider exit 0をOAE commitへ変換
- provider refusalをMission failureへ変換
- Issue closeをMission completionへ変換
- Fold越境tokenなしのEffect
- VS Code切断をtask abortへ変換
- Kernel拒否をGUIが成功表示
- `/1` Presentation値を`/2` ContextScopeへsilent copy
- `遊ぶ`ContextのTNT命令を、対象Worldを落として現実の製造へ誤配送
- User-declared World Lawを否定後、vendor default Contextでphysical EffectをRun
- MR／simulation成功をfab／家電／robotの物理実行権限へ昇格

## 7. MAGI receipt

- Maxwell: SphereDOSの都合で一般業務、PostPet、Party、MR／VR、現実改変、Meta-World branchを焼却しない
- Uriel: `/1`座標、`/2` Target、現行実装、6xx候補を分離し、scaffoldをruntimeへ昇格しない
- Raphael: 0～4 Context class、世代namespace、Kernel、Mapper、Server、Code、Project、Issueを別棚として接続する
- preserved unknown: exact coordinate、runtime言語、物理repo分割時期、Stable／LTS資源
- action gate: `pass with user gates`

この文書は現在時点のInterpretation OAEであり、過去commitへ当時のIntentを遡及生成しない。

## 8. 2026-08-21の観測と状態正本

PR #17のDevへの`merge`により、ファイルシステム試験ハーネスはDev基準線へ入りました。
SphereDOS Codeにも合成fixture駆動のコックピットGUI試験ハーネスがあります。ただし、両者を正式receiptで接続した
縦通し試験とVS Code Extension Host上の手動検証は未実施です。

機能ごとの状態は[機能状態表](m6xx-capability-matrix.ja.md)を人間向け入口、
[`status/capability-matrix.json`](../../status/capability-matrix.json)を機械可読正本とします。
この観測は2026-08-21時点の現在解釈であり、過去の作業者のIntentは
`historical-oae-unavailable`として遡及生成しません。
