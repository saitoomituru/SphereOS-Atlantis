# Vespa CloudとAtlantis Server 0.300.1を鍛造するタイミング

状態: `[DRAFT]`
棚: `sphere-architecture`
種別: `brainstorm`

## 作成メタ

```yaml
created_at_system: 2026-07-20T10:25:22+09:00
timezone: Asia/Tokyo
clock_source: host_system_clock
clock_calibration: unverified
authoring_agent: GPT-5.6 Thinking via GitHub connector
declared_personas: []
declared_position:
  - 本会話でユーザーが提示したSphereOS Atlantisの設計ブレストを、現在時刻のNoteとして整理する
claim_scope:
  - Vespa Cloud仮設層とAtlantis Server 0.300.1の最小構成
  - 共有ホスティング上の軽量control planeと外部compute workerの責務境界
non_authority_scope:
  - Fold8GおよびAkasha DBの正規仕様
  - さくらのレンタルサーバの契約上限・最新仕様の確定
  - IBD、Sphere-aae、SphereASTRO各repositoryの実装変更
  - production安全性・性能・可用性の保証
memory_publication_consent: confirmed
status_axes:
  content_maturity: raw-note
  engineering_state: not-started
  distribution_state: not-distributed
  resource_state: constrained
```

システム作成時刻は、対象World内の時刻、出来事の発生時刻、原資料の作成時刻を意味しない。

## 対象・範囲

SphereOS Atlantisの現行Prompt Engineering Edition、CLI、CORN stack、既存のscheduler／worker構想を踏まえ、
共有ホスティング程度の小さな火力でも成立する分散実行control planeを、`Atlantis Server 0.300.1`候補として
鍛造し始める時期かを整理する。

本Noteでいう`Vespa Cloud`は、Fold8Gによる意味次元圧縮やAkasha DBをまだ持たない仮設の分散搬送層である。
仕事札、capability、lease、receipt、artifact参照を保持し、実計算はPrompt Lineのprovider火力、CLI利用者の
手元火力、GitHub Actions、VPS、community worker等へ委譲する。

## 除外範囲

- 意味次元圧縮、意味空間routing、Akasha DB、7D／8D Fold runtimeの実装済み主張
- Mattermost等の常駐chat server、LLM inference、vector DB、重いEmbedding生成の共有host内実行
- Kubernetes、Redis、RabbitMQ、NATS等を初版の必須依存へ置くこと
- 外部workerへsecret、個人情報、local-only inputを配布すること
- `Server`を単なる`Server Advanced`の低性能版として定義すること

## 事実・観測 `[FACT]`

1. 現行AtlantisはSphere座標`0.250.1`、Prompt Engineering Editionであり、standalone runtimeは
   `NOT IMPLEMENTED`として公開されている。
2. Atlantisの責務にはEdition、Distribution、host／hardware profile、World orchestration契約、
   component契約への索引が含まれる。IBD、Sphere-aae、SphereASTROのruntime実装は各repositoryが正本である。
3. CORNはrepository-nativeなwork item、append-only event、Forge projection、scheduler入口を持つ。
   現在はoffline validation、context receipt、one-shot `tick`、Forge dry-runまでを実装し、scheduler常駐、
   network write、model inference、provider authenticationは実装しない。
4. Issue #5ではqueue／scheduler、Idle Cowboy dispatch、World別隔離が提案されている。
5. Issue #6では0.3xx.n候補として、環境内AI火力の検出・登録、queue polling、retry、承認済みworkerへの
   分散実行、receiptが検討されている。queue backendの最小依存とCORN／Issue／queue正本の関係は未解決である。
6. 現行Atlantisのvenv bootstrapはPython 3.11以上の標準機能を基本とし、公開されている開発追加依存は
   `PyYAML==6.0.3`である。production server runtime用の外部Python依存は、この調査範囲では定義を確認していない。
7. workspaceではZeroRoomLab-manifestのみがrequiredで、IBD、Sphere-aae、SphereASTROはoptional componentとして
   revision固定されている。workspace所属は暗黙の実装依存や変更権限を意味しない。
8. ユーザーは初期配置先候補として、WordPressを支えられる程度のPHPとMySQL互換RDBを持つ共有hostを提示した。
   hostの正確なversion、process制限、cron制限、同時接続上限は本Noteでは未確認である。

## 考察 `[INTERPRETATION]`

現在は、巨大な分散cloudを先に作る段階ではなく、**分散cloudが後から生えるための契約を固定する段階**に見える。

蜂の巣にとって、何の木へ付いているかは交換可能なhost profileであり、何の蜜を運ぶかはpayload profileである。
Vespa仮設層が保持すべき不変部は、hostやpayloadの銘柄ではなく、次の境界である。

```text
job contract
  -> capability match
  -> authority gate
  -> lease
  -> external execution
  -> immutable receipt
  -> review / acceptance
```

共有host上の`Atlantis Server 0.300.1`は、推論器ではなくcontrol planeとして扱う。PHPとMySQL互換RDBで、
WordPressの親戚に見える程度の短いrequest、SQL transaction、cron tickへ負荷を抑える。重いMAGI workflowは
Prompt Lineのprovider管理火力、またはCLI workerの利用者管理火力へ直結させる。

この分離により、小規模時は「便所の隅の小さな巣」で終わっても契約を満たし、火力とworkerが増えれば、
queue backend、artifact store、scheduler、regionを差し替えて大きな巣へ成長できる。

## 仮説・ブレスト `[HYPOTHESIS]`

### 1. Distribution候補

```yaml
product: sphereos-atlantis
coordinate_system: sphere-version-coordinate/1
candidate_coordinate:
  presentation: 0
  function: 300
  semantic_kernel: 1
canonical_candidate: 0.300.1
edition: prompt-engineering
distribution: atlantis-server
profile: matchbox
role: provisional-distributed-execution-control-plane
```

`0.300.1`は現時点では候補であり、version registryへ未採用である。

### 2. Matchbox profileの最小責務

```yaml
matchbox_profile:
  local_compute: metadata-and-validation-only
  heavy_compute_local: forbidden
  database: mysql-compatible
  application_runtime: php
  scheduler: cron-or-external-pull
  realtime_websocket: not-required
  artifact_body_storage: optional-external
  secret_distribution_to_workers: forbidden
```

### 3. 最小module

```text
Ingress
  job作成、Schema検証、rate limit

Work Registry
  job state、priority、required capability、scope、stop condition

Worker Registry
  worker ID、capability、approval、trust scope、capacity heartbeat

Lease Manager
  claim、期限、heartbeat、timeout、requeue

Receipt Store
  success／partial／failed／refused／timeout、実行envelope、hash、unknown

Artifact Reference
  payloadと成果物のcontent-addressed参照。初版では大容量本体を抱えない

Projection Bridge
  CORN work item、GitHub Issue、Forum、Wallet Pain Boardとの参照関係
```

### 4. 最小SQL概念

```text
jobs
workers
leases
receipts
artifact_refs
capability_refs
append_events
```

初版はRDBのtransactionと一意制約で二重claimを防ぎ、message brokerを必須化しない。
SQL schema、migration規約、index、retentionは別のcontract候補として設計する。

### 5. 実行envelopeの分離

```yaml
prompt-line:
  compute_owner: provider-managed
  result_default: proposed-output
  commit_authority: false

command-line:
  compute_owner: worker-managed
  result_default: working-tree-change-or-receipt
  commit_authority: explicitly-scoped
```

Prompt LineとCLIは真贋や上下ではない。provider管理火力とworker管理火力を同じqueueへ接続しても、
権限、privacy、cost、成果物の硬さを別レジスターで保持する。

### 6. component依存候補

```text
ZeroRoomLab-manifest
  共通定規、CORN横断契約、Context監査。required。

SphereOS-Atlantis
  Distribution、Server profile、job／worker／lease／receipt契約、CORN projection。

IBD
  0.300.1 Matchbox MVPではrequiredにしない。将来のmemory／search／Akasha系Bridge候補。

Sphere-aae
  worker execution adapter候補。Server本体のrequired dependencyにしない。

SphereASTRO
  worker／job可視化や個体責任境界の将来Bridge候補。MVP外。
```

### 7. 非目標

- Matchbox host自体でMAGI、AAE、IBDを常駐実行する
- capability一致だけでauthority、privacy、安全性、成果物採用を推定する
- receiptをaccepted resultと同一視する
- worker failureを人格、World、project全体の破局として扱う
- hostの火力不足を設計思想の敗北へ一般化する

## 内観メモ `[POEM]`

蜂は杉か桜かをほとんど気にしない。蜜がLLM推論かtestか画像生成かも、運搬路の思想ではない。
巣があり、札が読め、帰還票を返せればよい。

火力が来れば巣房は勝手に増える。火力が来なければ、さくら運営のおかんに重いthreadを見つからない、
便所の隅の小さな巣で終わる。それでも、仕事札とreceiptが壊れなければVespaとしては生きている。

## 未解決・⊥

- `0.300.1`を正式なSphere座標候補として採用するauthorityと変更手順
- `Atlantis Server`、`Vespa Scaffold`、`Matchbox profile`のstable IDと正式名称
- CORN work item、Server SQL job、GitHub Issueのうち何をcanonical sourceとするか
- append-only eventとSQL row更新をどう両立するか
- worker registrationの認証方式、鍵rotation、失効、replay対策
- external workerへのpull方式、cron方式、webhook方式の優先順位
- artifact本体の保存場所、容量上限、retention、content hash algorithm
- PHP／MySQL互換RDBの最低version、利用可能extension、transaction isolation
- 共有hostのCPU、memory、process、cron、outbound network、DB connection制限
- Forum／Wallet Pain BoardをServer 0.300.1へ含めるか、別App／Projectionとするか
- Server Advancedとの責務境界と命名
- Fold8G／Akasha DBが生えた後も残すtransport contractの範囲

## 本編昇格候補

- `docs/architecture/atlantis-server-0.300.1.ja.md`としてServer profileと非目標を正規化
- `versioning/contract.json`へ0.300.1候補を追加する前の変更票
- `server/contract.json`、`server/schema/*.json`、SQL migration方針の追加
- CORNとServer queueのprojection／canonical境界ADR
- Matchbox用GitHub Actions → 共有host deploy workflow

## 転送候補

- ZeroRoomLab-manifest: 分散worker／lease／receiptの横断contract候補
- Sphere-aae: CLI／local inference worker adapter候補
- IBD: 将来のartifact metadata、memory、search、Akasha Bridge候補
- SphereASTRO: worker identityと責任境界の表示候補

転送は本Note作成だけでは実行せず、各repositoryのAGENTS.mdと正本候補を読んだ別作業とする。

## source・Provenance

- 本会話におけるユーザーの設計ブレスト。2026-07-20、現在時刻のInterpretation OAEとして整理
- `AGENTS.md`
- `README.md`
- `docs/charter/meaning-and-vessel-dual-register.ja.md`
- `docs/architecture/1x-sdk-engineering-entrypoint.ja.md`
- `docs/operations/corn-stack.ja.md`
- `corn/registry.json`
- `workspace/components.json`
- `scripts/bootstrap_venv.py`
- `requirements-dev.txt`
- `note/AGENTS.md`
- `note/README.ja.md`
- `note/registry.json`
- `note/templates/brainstorm.ja.md`
- GitHub Issue #5「スケジューラー実装：ゲート・キュー管理とカウボーイAI分業によるトークンコスト最適化」
- GitHub Issue #6「0.3xx.n世代要件整理：環境内AI火力の検出・登録・分散実行」
- ZeroRoomLab-manifest pinned revision `af7ee209feaf6a96f87a8b42573e89fd849e109e`
  - `AGENTS.md` §0.4
  - `docs/theory/atlantis-magi-sdk-0.2.1.ja.md`
  - `docs/operations/context-ruler-and-causality-audit.ja.md`

### 現在の監査Position

```yaml
context_audit:
  medium_register: research-note
  declared_position: user-requested-design-preservation
  speaker_position:
    relation_to_target: authoring-agent-for-maintainer-request
    interest_disclosed: true
  ruler_provenance:
    - SphereOS-Atlantis/AGENTS.md
    - ZeroRoomLab-manifest@af7ee209feaf6a96f87a8b42573e89fd849e109e
  detected_nerf_risks:
    - resource-status-nerf
    - binary-only-completion-bias
    - cwd-as-mainline-bias
  preserved_unknowns:
    - server-coordinate-adoption
    - canonical-queue-source
    - exact-host-limits
    - security-contract
  human_review_required:
    - stable naming
    - 0.300.1 coordinate adoption
    - public deployment activation
```
