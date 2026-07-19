# Atlantis 1.x実行系・SDKエンジニア参入ガイド

状態: `[DRAFT]` `[0.25.1 DESIGN LINE]` `[1.x TARGET]`

この文書は、SphereOS Atlantis 1.xの実行系を鍛造するエンジニア向けに、component repository、
技術Layer `L`、Context Dimension `D Fold`、SDK surface `S`を混線させず案内する。

ここでいう募集は雇用ではなくOSS同人開発への参加募集である。報酬、業務委託、賞金がある場合は、
対象issueまたは別契約で明示される。

## 1. 1.xは現在状態ではなく統合milestone

Atlantisの版数正本では、次を区別する。

```text
SphereOS 3.x / 4.x        終了済みlegacy service
SphereOS Atlantis 0.x.0   文書化architectureとprompt-bound bootstrap
SphereOS Atlantis 1.x.0   executable binary integration milestone
SphereOS Atlantis x.x.n   security／corrective patch
```

1.xは全機能完成ではない。現在文書とpromptで拘束している責務が、少なくとも次の実行境界として
接続された最初の安定系列を指す。

- ASTRO package／Runnerによる個体実行境界
- IBDによる記憶、Context、Provenance、relation、model recordの保存と参照
- Atlantisによる複数ASTRO、World、session、connector、deviceのlocal orchestration
- AAE由来model、adapter、weightの読込境界
- MCP等の外部tool境界
- 起動、停止、権限縮小、復旧、unmount
- machine-readableなRegistryとclaim boundary

## 2. Component別の現在地と工学入口

| component | 現在の公開状態 | 実装入口 | まだ主張しないもの |
|---|---|---|---|
| [SphereOS Atlantis](https://github.com/saitoomituru/SphereOS-Atlantis) | 0.25.1-alpha.1候補／Prompt Engineering Edition | 開発環境、World orchestration契約、CORN、Note／persona／Experience入口、doctor、MAGI OAE時間gate | standalone Atlantis runtime |
| [IBD](https://github.com/saitoomituru/IBD) | Season 0／Draft Specification | IBDSDK、FAM Splitter SPI、Meta Catalog、Composite FAM、SsC、adapter | production DB、実Neo4j性能、対応DB保証 |
| [Sphere-aae](https://github.com/saitoomituru/Sphere-aae) | experimental edge AI runtime／preflightを含む | system-call splitter、FAM routing、Q、LAST_ORDER、model境界 | 完成済み人格container、完成済みFAM全系 |
| [SphereASTRO](https://github.com/saitoomituru/SphereASTRO) | Swift／SwiftUI GUI・責任境界、AI未接続 | ASTRO package、Runner、人格・継続性Registry、GUI | 統合済みAI runtime、永続人格実行 |
| [ZeroRoomLab-manifest](https://github.com/saitoomituru/ZeroRoomLab-manifest) | 横断正本・Reviewを含む | Registry、Context OS、SDK共通契約、主張境界 | 各componentのruntime実装正本 |

隣接repositoryを同じworkspaceで開けることは、変更権限や暗黙依存を意味しない。各repositoryを編集する前に
その`AGENTS.md`と最寄りの仕様を読む。

## 3. `L`、`D`、`S`を別キーで持つ

### 3.1 技術Layer `L`

`L`は何の上で何が実行されるかという順序軸である。

```text
hardware
  → firmware／kernel
  → POSIX-compatible OS
  → process／container runtime
  → Sphere runtime
  → library／SDK／App／prompt surface
```

順序を変えると依存構造が変わる。POSIX、process、container、database kernel、device driverはここに属する。
SphereOSはPOSIX OSを置換せず、その上で動く。

### 3.2 Context Dimension `D Fold`

`D`は一つのFoldへ束ねた重複のない意味軸数である。

```text
D = |unique(context_dimension_refs)|
```

Fold内の軸はpeerであり、列挙順から上下関係を作らない。同じ`4D Fold`でもFold ID、Dimension ID、
Registry revision、World、fact scope、Access Mapが違えば互換とは限らない。

```text
Astro 4D Fold = Cloud Chakra / Spiritual / Elemental / Astral
Actor 4D Fold = User / Assistant / System / Vendor
```

両方とも4Dだが、同じ四軸ではない。`D`をembedding dimension、配列長、技術Layer番号へ流用しない。

### 3.3 SDK surface `S`

`S`は同じcapabilityへ入る抽象度である。

| key | 利用者 | 入口 |
|---|---|---|
| `S0` | runtime／adapter実装者 | envelope、Ref、Schema、receipt、OAE、unknown |
| `S1` | driver／library実装者 | Registry Provider、Splitter、Transformer、Sink、adapter |
| `S2` | App開発者 | IBDSDK、AstroSDK、Atlantis SDK等のdomain bundle |
| `S3` | automation／low-code開発者 | typed workflow、FAM Query builder、policy選択 |
| `S4` | User／Assistant／Agent | promptから型付きQuery／FAMへcompileする入口 |

上位surfaceは下位surfaceを隠せるが、Registry、Fold、Provenance、Transformer、OAE、unknownを捨てない。

## 4. SDK bundleの最低キー

```yaml
sdk_bundle:
  bundle_id: sdk://example/domain@1
  sdk_surface: S2
  capabilities: []
  technical_dependencies:
    - layer_ref: runtime/application
      requires: component-sdk@0.x
  context_fold:
    fold_ref: fold://example/domain@1
    dimension_refs: []
    context_dimension_count: 0
  registry_refs: []
```

接続時はstable ID、revision、Dimension集合、Schema、Access Map方向、Transformer capability、permission、
fact scope、World、loss、unknown、`⊥`、OAE receiptを検査する。同じD数だけで自動接続しない。

## 5. 普通のエンジニアが今掘れるissue棚

- Python: CLI、Schema validator、read-only doctor、fixture、clean-room test
- Database: Neo4j、MariaDB／PostgreSQL、RDB connector、Evidence freshness、migration
- Search／math: embedding adapter、Vector profile、SsCの数理検証、異種store scoreの校正
- Swift／SwiftUI: SphereASTRO GUI、境界表示、unknown／unmount／復旧UX
- Edge／ML: model lineage、adapter／weight loader、system-call splitter、LAST_ORDER
- Runtime: native service、embedded library、container profile、IPC／HTTP／RPC境界
- OS／device: Pi、Linux、Windows、Darwin、sensor、GPIO、時計校正、offline復旧
- Security: capability、secret境界、権限縮小、停止、監査receipt
- DevEx: VS Code、Dev Containers、GitHub Codespaces、CI、複数coding agentの隔離初期化
- Documentation: API reference、ADR、図、翻訳、神話Presentationと工学仕様の二重記述

神話やスピリチュアル表現を採用しなくても、工学契約へ直接貢献できる。ただし、それらの棚を不要な装飾として
削らない。同様に、神話Presentationだけでtest、権限、失敗、復旧を成功扱いにしない。

## 6. 正本リンク

- [Atlantis版数・1.x到達条件](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/main/docs/theory/sphereos-atlantis-versioning-and-bootstrap.ja.md)
- [Sphere Context Dimension OS](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/main/docs/theory/sphere-context-dimension-os.ja.md)
- [霊的言霊の次元とD Fold](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/main/docs/philosophy/spiritual-context-dimension-and-fold.ja.md)
- [Sphere Context SDK共通契約](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/main/docs/theory/sphere-context-sdk-contract.ja.md)
- [IBDのContext Dimension OS／IBDSDK](https://github.com/saitoomituru/IBD/blob/main/docs/architecture/context-dimension-os-and-ibdsdk.ja.md)
- [IBDSDK module契約](https://github.com/saitoomituru/IBD/blob/main/docs/specification/ibd-sdk-module-contracts.ja.md)
- [Sphere-aae（公開main。Context Dimension／OAE profileは別branchでReview中）](https://github.com/saitoomituru/Sphere-aae)
- [SphereASTRO](https://github.com/saitoomituru/SphereASTRO)
