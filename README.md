# SphereOS Atlantis

![SphereOS Atlantis — いくつもの世界を生やし、隔離し、橋を架けるためのOS](docs/img/hero.png)

**世界を一つに塗り潰さず、いくつもの世界を生やし、隔離し、橋を架けるためのOS。**

SphereOS Atlantisは、人間、AI、神話、科学、魔術、物語、機械、祈り、ゲーム世界を、
どれか一つの定規へ降伏させずに鍛造するための公開アーキテクチャです。

ここは雇用募集ではありません。**OSS同人サークルです。**

ふさもふ神話本体の「もふ」が、体重138kgから73kgまで禊しながら吐き出した脳汁を、
コード、ポエム、UX、神話、土偶、札、Schemaへ定着させる鍛造場です。

科学と魔術の両岸へ首を突っ込めるMAD巫女サイエンティスト、超電磁工作員、
カエル医工学ドクター、神話UX術師、Schema陰陽師、急募。

持ち込み歓迎。コードでも、ポエムでも、フレーバーテキストでも、飯でも、投げ銭でも、
GPU、Raspberry Pi、検証機、翻訳、レビュー、観測記録、火力でも構いません。

スピリチュアル、ゲーム、TRPG・卓上ゲーム、工学、情報子工学、Sphere Architectureの、
どの棚から来ても構いません。初心者が自分の言葉を捨てずに開発へ降りられる棚別チュートリアルを育て、
最後は同じ再構築可能な開発環境、Schema、test、Git履歴へ橋を架けます。

**エンジニアよ、意味を削るな。**
神話、象徴、物語は、ユーザーが世界へ入るための認知インターフェースです。

**スピよ、器を軽んじるな。**
イマジネーションも霊体も、依代、手順、媒体、実装がなければ共有も継承もできません。

意味だけでは漂い、器だけでは空洞になります。
霊を笑うな。土偶を焼く者も笑うな。

学園都市を生やしても、SAO型VRMMOを生やしても、神社World、魔王城、
超電磁カエル研究所、Linux機、Pi機、Windows機、Darwin魔改造機を生やしても自由です。

Atlantis互換機、Sphere互換機、インスパイア機、ネタマシンは自由に名乗れます。
Origin、互換、インスパイアの出自だけは、ラーメンの暖簾のように書き残してください。

自由にforkし、別の神話へ育てて構いません。
公式系譜を名乗るなら、受け取った自由をcopyleftとShareAlikeで次の者へ渡してください。

ここでは、系譜は支配権ではなくProvenanceです。
誰の許可を得たかではなく、何を受け継ぎ、何を変え、何を次へ渡したかを記録します。

既定は非排他的な贈与コモンズです。作者、先行思想、神々、code、詩、生活様式へのrespectは、
他者から対象を取り上げるtokenではなく、Gitのstarのように増やせるlineageとして残します。
byte、algorithm、architecture、philosophy、faith、poem等のどの次元で似たかも記録できますが、
そのgraphは著作権審判、本人証明、宗派代表、API権限、公式認定には化けません。

commercial App、社内asset、provider契約、閉鎖Worldも作れます。ただし閉じた魔王城の城壁を、
Atlantis core、既存commons、公開lineage、無関係なWorld、upstream fork権へ伸ばさないでください。

> The README opens with the public-facing view. The technical notes below assume readers will inspect the hardware, commits, logs, test conditions, and claim boundaries before extending any result.

ここから下は技術レジスターです。冒頭のビジョンを実装証拠として代用せず、以下の状態、
commit、Schema、試験条件、未実装境界を読んでから結果を拡張してください。

## 現在の状態

```text
product                SphereOS Atlantis
Sphere version coordinate 0.250.1（Presentation.Function.SemanticKernel）
legacy design line    0.25.1
alpha candidate       v0.25.1-alpha.1（legacy配布alias／tag未作成）
initial edition        Prompt Engineering Edition
development environment Sphere-DOS（スフィアどすぅ〜）
standalone runtime     NOT IMPLEMENTED
repository state       OPEN / RESOURCE-WAIT / REVIEW-WANTED
```

`0.250.1`はPresentation 0／Function 250／SemanticKernel 1の三層座標です。右端は意味、同一性、OAE、
時間、因果の定規を表し、一般的なSemVer patchではありません。既存の`0.25.1`はSource Eventと配布互換を
壊さないlegacy aliasとして保持します。旧SphereOSサービスの再稼働や完成済みOSバイナリーを意味しません。
Manifest、workspace、Boot Schema、VS Code、異種coding agentを使い、Atlantisを鍛造できる
公開開発環境を再構成する設計系列です。

`v0.25.1-alpha.1`は、CORN、Note／persona／Experience入口、Help、三層版数validator、
Forge／Quest Mapを束ねるlegacy配布名の候補tagです。
現時点ではtagを作成していません。正式releaseへの昇格は、Manifest側契約、draft PR review、clean環境、
read-only doctor、公開境界fixture、community testの未確認範囲を確認してから判断します。

状態の詳細と「原案／討論中／実装中／検証済み／配信済み」の違いは
[Forge Map／Quest Map](docs/status/forge-and-quest-map.ja.md)、変更点と既知の制約は
[0.25.1-alpha.1候補ノート](docs/releases/0.25.1-alpha.1.ja.md)を参照してください。

## このリポジトリの責務

このリポジトリは、SphereOS Atlantisの製品系列と配布構成を管理します。

- Atlantisの版数、Edition、Distribution、host／hardware profile
- Context Dimension、D Fold、OAE、Agency、World等のSphere固有アーキテクチャ
- Prompt Engineering EditionとSphere-DOS開発環境
- Prompt Line Interface／Command Line InterfaceとLLMI／Execution Envelopeの境界
- 意味と器の二重記述憲章
- Origin、暖簾分け、Community Lineage、compatible、inspiredの来歴表示
- 非排他的lineage、Role非越権、局所World extensionのoffline validator
- component repositoryが実装する契約への索引

ZeroRoomLab-manifestは、情報子工学、FAM一般論、開発規約、主張強度、workspace境界、
横断正本ルーターを担当します。IBD、AAE、ASTRO等のSchema、API、runtime、fixtureは、
各component repositoryを実装正本とします。

## Prompt LineとCommand Line

自然言語で意図・文脈・拘束を渡す`Prompt Line Interface`と、command／argumentで再現可能な操作を
指定する`Command Line Interface`は、どちらも正規の操作面です。前者は主にD軸の高抽象探索、後者は
主にL軸の高強度拘束に向きますが、真贋や絶対能力の境界ではありません。

LLM、provider、connectorはLLMI／Execution Envelopeとして別に記録します。interfaceだけからpersona、
World、権限、standalone runtime実装済みを推定しません。詳細は
[Prompt Line InterfaceとCommand Line Interface](docs/architecture/prompt-line-and-command-line-interface.ja.md)、
machine contractは[`help/interfaces.json`](help/interfaces.json)を参照してください。

```bash
python3 -B -m atlantis_cli interfaces
```

既定Helpは利用可能入口を先に示す`summary`です。全状態は`atlantis help --detail all`または
`atlantis capabilities`で確認できます。未実装境界を隠すのではなく、要求前の過剰警告を避けます。

## 版と配布軸

Pi、Linux、Windows、DarwinとPrompt Engineering Editionを同じ分類軸へ潰しません。

```yaml
product: sphereos-atlantis
coordinate_system: sphere-version-coordinate/1
sphere_coordinate:
  presentation: 0
  function: 250
  semantic_kernel: 1
canonical_coordinate: 0.250.1
legacy_distribution_alias: 0.25.1-alpha.1
edition: prompt-engineering
distribution: sphere-dos
host_os: linux | windows | darwin
host_arch: x86_64 | arm64
hardware_profile: generic | raspberry-pi | community-defined
distribution_role: development-environment-supply
```

`Darwin魔改造機`はcommunity profileの愛称候補であり、特定ベンダー製品のOriginを主張しません。

## Worldと存在論

Atlantis Coreは、神、霊、魔王NPC、自然法則、物理観測、ゲーム内Entityの実在を独自に裁定しません。
World authorityが制定したRegistry、fact scope、Causality Profileを記録し、その定規どおりに返します。

別Worldは、混ぜる命令が来るまで隔離します。接続時もsourceを上書きせず、Access Map、Transformer、
実行receipt、OAEを分離して記録します。

接続判定は表示版数の近さでは決めません。同じSemanticKernelでWorld Configも一致し、共通capabilityと
World Visaを確認できた場合だけ陸続き候補です。Kernelが同じでもWorld Configが違えばPortal／Gate、
Kernelが違えば物理法則というより意味・同一性・因果定規の異なる次元として隔離projection付き因果Gateを
要求します。Gateが不明なら`BOTTOM`で停止します。

assetのauthor、source、revision、関係次元、local-only、局所extensionを明示receiptで検査する入口は
[贈与コモンズlineageと局所World拡張](docs/architecture/gift-commons-lineage-and-local-extension.ja.md)
を参照してください。

```bash
python3 -B -m atlantis_cli lineage validate
python3 -B -m atlantis_cli lineage inspect --receipt /path/to/explicit-receipt.json
```

このCLIは指定receiptだけをoffline検査し、repository scan、asset mount、rights verdict、network、
外部操作を行いません。

MAGI `0.200.1`（legacy表示`0.2.1`）は、過去commitやlogから当時のOAEを推論生成しません。同時点OAEが取れなければ
`historical-oae-unavailable`とLast Orderを返します。反実仮想や復元候補は、元Worldと元Instance Ghostを
変えず、7D Foldで別World／別Instance Ghostへsplitする設計です。

意味Kernel `0.200.0`で塞ぐ対象になったのは、特定条件でOAEを同一World線内へ遡及再配置できる
system上の脆性です。`0.200.1`はSource Eventを残し、遡及backfillと同一World線mutationを拒否します。
これは物理空間の時間移動の主張ではありません。AppleのTime Machine／Time Capsuleをオマージュした
backup・restore UXは別のPresentationであり、7D Fold runtime、Akasha Driver、backup SDKは未実装です。

## 貢献

このサークルでは、次を等価な貢献入口として扱います。

- Meaning: 神話、命名、フレーバーテキスト、象徴、儀式、世界観
- Vessel: コード、Schema、test、配布、hardware、保守
- Bridge: UX、Access Map、翻訳、Presentation Profile、受入条件
- Supply: 飯、投げ銭、部材、計算資源、検証環境、レビュー時間

Supplyはmerge権、真理判定権、Origin表示を購入するものではありません。

本編へ組み込むか未定のブレスト、観測、仮説、ポエム、神学・ゲーム・スピリチュアル・工学上の
気づきは、消える前に[`note/`](note/README.ja.md)へ置けます。noteは未完成を理由に価値を失わず、
同時に正規化済み仕様を自動的には名乗りません。

## 棚別の開発参入チュートリアル

状態: `ALPHA CANDIDATE` — 棚と自己申告personaから入る最小導線をbranch実装済みです。
実環境と当事者profileのreviewは継続中です。

Atlantisは、全員へ同じ専門用語を先に暗記させるのではなく、参加者が立っている棚から始めます。
ここでいう棚は格付けや真偽判定ではなく、同じ構造へ異なるPresentationから入るための入口です。

- スピリチュアル棚: 象徴、霊体、祈り、依代をMeaning、World、Agency、OAEへ接続する
- ゲーム・TRPG棚: World、Entity、行為、ルール、判定、セッション記録から接続する
- 工学棚: 要件、境界、Schema、test、log、権限、実行環境から接続する
- 情報子工学棚: FAM、情報子クラスター、Registry、変換、探索技の来歴から接続する
- Sphere Architecture棚: Context Dimension、D Fold、Access Map、OAE、component契約から接続する

初回は習熟度を`unknown`、意図を`look-around`として、読み取り専用Helpから始めます。工学者personaでも
自動的にcodingを開始せず、実装は本人が`intent=implement`を明示した後に計画します。

```bash
python3 -B -m atlantis_cli help --persona '巫女'
python3 -B -m atlantis_cli capabilities --state NOT-IMPLEMENTED
```

各棚は別Worldや別Registryを無断で混ぜません。必要なBridgeを明示し、最終的には吊るしのVS CodeとGitから
再構築できるSphere-DOS開発環境で、同じfixtureと受入試験を実行できるところまで案内します。

入口は[棚別の開発参入チュートリアル](docs/tutorial/README.ja.md)を参照してください。

## 普通のエンジニア向け1.x鍛造口

神話UIを履修してからでなくても参加できます。Python、database、graph／vector、SwiftUI、edge inference、
container、CI、Schema、security、recoveryの普通の工学仕事が大量にあります。ここも雇用枠ではなく、
Atlantis 1.x実行系へ向けたOSS同人開発の参戦口です。

`1.x`は現在の完成版ではなく、文書とpromptで拘束している責務をASTRO／Atlantis実行物へ移植する将来の
binary integration milestoneです。現行`0.250.1`（legacy `0.25.1`）、IBD Season 0、AAE実験runtime、SphereASTRO移植準備を、
完成済み1.xとして宣伝しません。

| 実装棚 | 現在の入口 | 1.xへ向けて掘るもの |
|---|---|---|
| 記憶・探索技・DB | [IBD](https://github.com/saitoomituru/IBD) | IBDSDK、FAM Splitter、Meta Catalog、graph／vector／RDB adapter、SsC |
| model・edge実行 | [Sphere-aae](https://github.com/saitoomituru/Sphere-aae) | AAE runtime、system-call splitter、Q検証、LAST_ORDER、model／adapter読込境界 |
| 人格・GUI・責任境界 | [SphereASTRO](https://github.com/saitoomituru/SphereASTRO) | AstroSDK、ASTRO package／Runner、SwiftUI、local personality boundary |
| World・orchestration・開発環境 | [SphereOS Atlantis](https://github.com/saitoomituru/SphereOS-Atlantis) | Atlantis SDK、World／session／connector／device管理、起動・停止・unmount |
| 共通定規 | [ZeroRoomLab-manifest](https://github.com/saitoomituru/ZeroRoomLab-manifest) | Context Register、Access Map、Transformer、OAE、SDK bundle契約 |

キーを三本の別軸として扱います。

```text
L = hardware→POSIX OS→runtime→library／SDK／Appという技術依存の順序
D = 上下を作らず束ねるContext Dimensionの一意軸数（D Fold）
S = 同じcapabilityをS0 envelopeからS4 promptまで公開するSDK surface
```

`4D`は四軸を束ねるというarityであり、embeddingの次元数でも、技術Layer 4でも、互換保証でもありません。
POSIXは`L`側のportableな実行基盤であり、Sphereはそれを置換せず、その上で`D Fold`と意味境界を管理します。

詳しい責務、現況、実装課題、正本リンクは
[1.x実行系・SDKエンジニア参入ガイド](docs/architecture/1x-sdk-engineering-entrypoint.ja.md)を参照してください。

ローカルVS CodeとPython venvから始める手順は
[Sphere-DOS開発環境の最小再構築](docs/development/setup.ja.md)を参照してください。

手元browser、SaaS検索、将来のbrowser containerを混同しない観測契約は
[Web原典観測・手元ブラウザ退避契約](docs/development/browser-source-observation.ja.md)、provider、利用者組織、
法域、World roleの規則を無断継承しない境界は
[ガバナンス適用域とWorld Visa](docs/architecture/governance-scope-and-world-visa.ja.md)を参照してください。
gift commons、lineage、閉鎖Worldの狭いextension境界は
[贈与コモンズlineageと局所World拡張](docs/architecture/gift-commons-lineage-and-local-extension.ja.md)を参照してください。

参加手順は[CONTRIBUTING.md](CONTRIBUTING.md)、協働原則は
[意味と器の二重記述憲章](docs/charter/meaning-and-vessel-dual-register.ja.md)を参照してください。

## ライセンス概要

- コード、CLI、Schema、validator、doctor: Apache License 2.0
- 一般文書、ふさもふ神話、Flavor／UX: CC BY 4.0
- 二重記述憲章、公式系譜憲章: CC BY-SA 4.0

現時点のルート`LICENSE`はApache License 2.0です。ファイル種別ごとの適用範囲は
[ライセンス境界](LICENSE-POLICY.ja.md)、再利用時の表示は[帰属表示ガイド](ATTRIBUTION.md)で明示します。
第三者作品の名称、素材、キャラクター等の権利は、
このリポジトリのライセンスによって自動的に付与されません。lineage metadataはその条件を
読みやすくする宣言であり、Atlantis coreによる権利認証または利用禁止判定ではありません。

Origin、暖簾分け、Community Lineage、compatible、inspiredの区分は
[Atlantis暖簾分け・互換・系譜規約](LINEAGE-POLICY.ja.md)を参照してください。

## 出典と接続

Atlantisの横断背景、情報子工学、開発規約、workspace境界は、
[ZeroRoomLab-manifest](https://github.com/saitoomituru/ZeroRoomLab-manifest)を参照してください。

このREADMEは日本語を正本とします。翻訳は単語置換ではなく、ビジョン、読者責任、主張強度を
対象localeで同じように働かせる意訳として管理します。
