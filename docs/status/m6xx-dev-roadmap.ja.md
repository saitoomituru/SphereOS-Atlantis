# m.6xx.1 Dev Roadmap

- 状態: `[ROADMAP-CANDIDATE]` `[PHASE-0]` `[RUNTIME NOT IMPLEMENTED]`
- branch: `dev/m6xx.1-reincarnation-sdk`
- 公開正本: [Issue #16](https://github.com/saitoomituru/SphereOS-Atlantis/issues/16)
- Milestone: [m.6xx.1 — Sphere Reincarnation SDK Next Generation](https://github.com/saitoomituru/SphereOS-Atlantis/milestone/1)
- 運用盤: [Project #2](https://github.com/users/saitoomituru/projects/2)（private）

## 1. このbranchの目的

現行`0.250.1` Prompt Engineering Editionを壊さず、意味管理情報子clusterを別Vesselへ搬送しても
source、scope、unknown、provenance、authority、因果を失わないSphere Reincarnation Frameworkを鍛造する。
その最小の意味伝達保証核を`Sphere Reincarnation Lean Kernel`候補とする。

`m.6xx.1`は正式release座標ではない。Presentation番号、Function値、runtime言語、package分割、release日、
Stable／LTS条件はUser Gateまで固定しない。

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

## 5. Phase

| Phase | 内容 | 状態 |
|---|---|---|
| 0 | branch、README、package／product棚、旧Source対応表 | `IN PROGRESS` |
| 1 | package manifest、coordinate handshake、Context Envelope | `NOT STARTED` |
| 2 | Lean Kernel task／lease／OAE state machine | `NOT STARTED` |
| 3 | Provider Adapter probe／opaque output fixture | `NOT STARTED` |
| 4 | Fold Access Mapper FAM JSON／Proton resolver | `NOT STARTED` |
| 5 | SphereDOS Server headless Host | `NOT STARTED` |
| 6 | SphereDOS Code Cockpit最小Presentation | `NOT STARTED` |
| 7 | Server／Code統合、crash／resume／conflict負例 | `NOT STARTED` |
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

## 7. MAGI receipt

- Maxwell: SphereDOSの都合で一般業務、Open Inspector、PostPet、third-party Presentationを焼却しない
- Uriel: 現行0.250.1の実装済み範囲と6xx候補を分離し、scaffoldをruntimeへ昇格しない
- Raphael: main、Dev branch、Kernel、Mapper、Server、Code、Project、Issueを別棚として接続する
- preserved unknown: exact coordinate、runtime言語、物理repo分割時期、Stable／LTS資源
- action gate: `pass with user gates`

この文書は現在時点のInterpretation OAEであり、過去commitへ当時のIntentを遡及生成しない。
