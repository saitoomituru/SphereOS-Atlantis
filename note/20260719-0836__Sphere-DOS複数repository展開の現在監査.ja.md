# Sphere-DOS複数repository展開の現在監査

状態: `[DRAFT]`
棚: `cross-shelf`
種別: `review`

## 作成メタ

```yaml
created_at_system: 2026-07-19T08:36:45+09:00
timezone: Asia/Tokyo (+09:00)
clock_source: host_system_clock
clock_calibration: unverified
authoring_agent: openai-gpt-5.6-thinking
observation_mode: current-interpretation-of-current-repository-state
historical_oae_status: historical-oae-unavailable
last_order:
  code: OAE-HISTORY-UNKNOWN
  action: stop-retroactive-backfill
```

この記録は現在時点の実装判断です。過去commitから当時のObserver、Intent、OAEを逆算しません。

## 対象・範囲

SphereOS Atlantis 0.2.1 Prompt Engineering Editionへ、固定revisionの複数repository workspaceと、
standalone runtimeではないSphere-DOS local development shellを追加する変更。

## 除外範囲

- IBD、Sphere-aae、SphereASTRO、ZeroRoomLab-manifest本体の変更
- component runtimeの起動と統合
- production deployment
- 7D Fold、Akasha Driver、backup SDKの実装
- model provider認証、秘密値、enterprise資産

## 事実・観測 `[FACT]`

- Atlantis本体にはPython venv、VS Code設定、Dev Container、doctor、unit test、clean-room CIが存在する。
- READMEはstandalone runtimeを`NOT IMPLEMENTED`、repository stateを`BOOTSTRAPPING`としている。
- component実装正本はZeroRoomLab-manifest、IBD、Sphere-aae、SphereASTROへ分離されている。
- 4 repositoryはいずれも公開GitHub repositoryで、2026-07-19現在のrevisionを参照できた。
- この変更のlocal unit testでは、manifest検証、offline plan、VS Code workspace生成、
  Sphere-DOS local receipt生成を標準Pythonだけで通した。
- この実行環境からGitHubへの直接cloneはDNS解決不能だったため、network clone経路は未試験である。

## 考察 `[INTERPRETATION]`

### Declared Position

直列的な「下位component完成後に上位OS」という企業roadmapを既定にせず、
現在存在する器を別Git履歴のまま一つの作業机へ並べ、欠損を明示した縮退運転を優先する。

### Position-talk Risk

編集者はAtlantis統合側から見ており、cwdのrepositoryを暗黙のmainへ置くriskがある。
対策として、各componentのroleを上下関係ではなく別責務としてmanifestへ記録し、
隣接repositoryの自動更新と自動編集を禁止する。

### Claim Scope / Medium Register

これはVesselとBridgeの開発環境変更であり、SphereOSの哲学的実在、神学的実在、
物理性能、完成済みstandalone runtimeを主張しない。

### Ruler Provenance

- workspace境界: SphereOS Atlantis AGENTS.md
- 横断定規とOAE時間整合性: ZeroRoomLab-manifest AGENTS.md §0.4、
  Atlantis-MAGISDK 0.2.1、Context定規・因果・OAE横断監査規約
- component revision: 各GitHub repositoryの現在参照可能なcommit
- branch選択: ユーザーの「作業環境構築して可能な範囲展開」の依頼

### Nerf Risk

- binary中心主義でPrompt Engineering Editionを未実装扱いへ丸めない
- clone成功をruntime稼働へ昇格しない
- resource不足やnetwork不能を設計思想の敗北へ一般化しない
- componentの別World、別Registry、別実装正本をAtlantisへ吸収しない

## 仮説・ブレスト `[HYPOTHESIS]`

固定revision workspaceとreceiptが安定すれば、次段でcomponentごとのdoctor adapterを追加し、
「clone済み」ではなく「契約を満たす範囲」をcomponent別に返せる。

## 内観メモ `[POEM]`

巨大な城を一晩で起動するのではなく、まず港に四本の桟橋を出す。
船は別の旗と航海日誌を保ったまま、必要なときだけAtlantisへ接岸する。

## 未解決・⊥

- network cloneがGitHub Actions、macOS、Windows、Linuxで同じように通るか
- component repository内の依存導入とruntime起動順
- optional componentが欠けたときの正式なcapability negotiation
- final 7D Dimension Registry
- production、hardware-specific distribution

## 本編昇格候補

- `workspace/components.json`
- `atlantis workspace plan|init|status`
- `atlantis sphere-dos boot|status`
- `docs/development/workspace-and-sphere-dos.ja.md`

## 転送候補

- component doctor adapterは各component repositoryへ別票
- revision更新票はZeroRoomLab-manifestの横断受領規約と接続

## source・Provenance

- SphereOS Atlantis README.md
- SphereOS Atlantis AGENTS.md
- docs/development/setup.ja.md
- ZeroRoomLab-manifest AGENTS.md §0.4
- docs/theory/atlantis-magi-sdk-0.2.1.ja.md
- docs/operations/context-ruler-and-causality-audit.ja.md
- GitHub repository metadata and current commit references observed on 2026-07-19
