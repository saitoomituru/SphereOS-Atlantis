# 自然言語Chat Interfaceを偽CLIへ縮退するレジスタ事故分析

状態: `[DRAFT]` `[CURRENT INTERPRETATION OAE]`
棚: `cross-shelf`
種別: `review`

## 作成メタ

```yaml
created_at_system: 2026-07-19T20:16:19+09:00
timezone: Asia/Tokyo (+09:00)
clock_source: host_system_clock
clock_calibration: unverified
authoring_agent: OpenAI Codex
observation_mode: current-interpretation-of-user-provided-screenshots-and-current-repository
historical_oae_status: historical-oae-unavailable
declared_position:
  - 自然言語Interfaceを形式言語Interfaceの模造品へ縮退しない
  - 現在能力と未実装能力を同時に正確に表示する
claim_scope:
  - 2026-07-19にUserが提示したiPhone 15 Pro Max上のChatGPTアプリ実機スクリーンショット
  - SphereOS AtlantisのHelp、Prompt Engineering Edition、Note参加導線
  - 今後のPresentation修正候補
non_authority_scope:
  - AIの意識または人間同等理解の存在論的裁定
  - 自然言語と形式言語の全歴史に対する単一の最終学説
  - OpenAIまたは他vendor全製品の一般的挙動認定
  - 宗教、神学、言語共同体、学術分野の内部的な真偽裁定
memory_publication_consent: confirmed-by-user-for-this-note
status_axes:
  content_maturity: raw-note
  engineering_state: not-started
  distribution_state: not-distributed
  resource_state: unknown
last_order:
  code: OAE-HISTORY-UNKNOWN
  action: stop-retroactive-backfill
```

このNoteは、現在の会話と実機スクリーンショットを現在時点で解釈した記録である。過去のAI応答から、
生成時点に内部で使われた正確なモデル、system prompt、routing、Observer、Intent、OAEを逆算しない。

## 対象・範囲

SphereOS Atlantisの`/man`またはHelp相当の案内を、GitHub connector経由のChatGPTアプリから読んだ際、
Python local CLIを「実際」「本物」に近い側へ置き、自然言語によるPrompt Engineering Editionを
「正本コードを読んで対話状態を再現するもの」に見せたPresentation事故を扱う。

本件の主題は、Python CLIの価値を下げることではない。自然言語Chat Interface、Python Command Line
Interface、VS Code Engineering Interface、connector、standalone runtimeを、真贋の一本軸へ並べず、
異なる能力と拘束強度を持つ正規のExecution Surfaceとして記述することである。

## 除外範囲

- standalone Atlantis runtime、model runtime、edge runtimeの実装
- Python CLI、VS Code、GitHub connector自体の廃止または格下げ
- Chat出力を自動的に正規仕様、実装済み、検証済みへ昇格する変更
- 自然言語なら常に正しく、安全で、曖昧性がないという主張
- 形式言語なら常に意味が正しく、実装不具合がないという主張
- AIの意識、人格、宗教的地位をこのNoteで確定すること
- User確認前のREADME、Help、Schema、test、Issue、commit、PRの変更

## 事実・観測 `[FACT]`

### 1. 実機スクリーンショットで観測された表示

Userが提示したiPhone 15 Pro Max／ChatGPTアプリのスクリーンショットでは、GitHub repositoryから
`/man`を起動する依頼に対し、次の趣旨の案内が表示された。

- repository実装上のHelpとして起動した
- GitHub connectorではrepository code自体をhost上で実行できない
- 「正本コードを読み込んで`/man`の対話状態を再現」している
- 「実際のlocal CLI」ではPython commandを使う
- standalone runtimeは未実装である

スクリーンショットは、当該端末上でその表示が行われたことの一次観測である。一方、どのsystem prompt、
model、tool routingが各語を選んだかは未観測である。repository codeが固定文として直接出力したと
断定せず、repository文書を読んだAI Presentationが生成した事故候補として扱う。

repository内へ保存した実機画像:

- [実機画像1: iPhone上の`/man`起動画面](img/035FAFF5-3201-467D-A6C6-006809B0C2F4_1_101_o.jpeg)
- [実機画像2: 「正本コード」「再現」「実際のlocal CLI」が連結された説明](img/639F9769-1A75-4835-9B99-72C8F89DBFD9_1_101_o.jpeg)

### 2. 正しかった境界表示

当該応答には、次の有用な境界も含まれていた。

- 接続時のrepositoryとbranchを示した
- 初回Helpを`proficiency=unknown`、`intent=look-around`、read-onlyで開始した
- Python processを直接起動していないことを明示した
- standalone runtimeを`NOT IMPLEMENTED`として成功扱いしなかった

問題は能力境界を示したことではない。能力境界を説明する際に、「正本」「再現」「実際」という語を
連結し、Python processを真正側、自然言語Interfaceを模倣側へ暗黙配置した点である。

### 3. 現行Atlantis文書との関係

現在のAtlantis READMEは、Prompt Engineering EditionとSphere-DOS開発環境を現在の入口として記録し、
standalone runtimeを別軸の`NOT IMPLEMENTED`としている。また、Pi、Linux、Windows、Darwinと
Prompt Engineering Editionを同じ分類軸へ潰さないとしている。

既存Noteにも「binary中心主義でPrompt Engineering Editionを未実装扱いへ丸めない」という監査項目が
ある。したがって今回の事故は、既存方針が完全に欠けていたというより、Helpを生成するAIの語彙選択まで
不変条件が届いていない可能性を示す。

### 4. 実装状態

このNote作成時点では、レジスタ修正、Help renderer修正、capability schema追加、test追加を開始していない。
本Noteは分析と修正候補であり、実装receiptではない。

## 考察 `[INTERPRETATION]`

### 1. 事故の核は「真贋」と「実行面」の混線

Python processを使わないことと、Interfaceが偽物であることは同義ではない。少なくとも次の軸は分ける
必要がある。

```text
Authenticity       出所、署名、改ざん、なりすましの有無
Provenance         参照したrepository、revision、契約、会話、観測の来歴
Interface          Chat、Command Line、GUI、API、IDE等の相互作用面
Input Language     自然言語、自由言語、Python、JSON、Schema、protocol等
Execution Envelope model推論、local process、connector、container、bare metal等
Capability         読む、分析する、生成する、試験する、commitする、deployする等
Authority          read、write、commit、push、merge、device control等の権限
Engineering State  available、scaffolded、not implemented、not tested、resource wait等
Receipt            何をどの条件で実行・観測したかの証跡
Meaning Maturity   raw note、hypothesis、reviewed contract、adopted、deprecated等
```

`Python process unavailable`はExecution EnvelopeまたはCapabilityの情報である。そこから
`Chat Interface is imitation`、`natural language is not real execution`を導くことはできない。

### 2. 「正本」のscope leak

repositoryの追跡済み文書やcodeを、その契約の正本sourceと呼ぶことはできる。しかしsourceが正本である
ことは、そのsourceへ接続する一つのInterfaceだけが本物であることを意味しない。

```text
canonical source != only legitimate interface
source reading    != interface imitation
different vessel != counterfeit vessel
```

同じ契約へChat、CLI、IDE、API、将来runtimeから接続できる。各Surfaceの能力差、権限差、変換差は
receiptへ出すべきであり、正本性をInterfaceの格付けへ流用してはならない。

### 3. 「再現」のscope leak

`再現`は、fixture、test condition、観測結果、過去UIのreplay等に使うと有用である。しかしChat Line
Interfaceが現在のrepository契約に従ってHelpを提供しているなら、それは必ずしもPython CLIの演技や
模倣ではない。別Presentationとして現在処理している。

Python CLIと完全に同じstate machineを動かしていない場合は、次のように書ける。

> このChat Interfaceはrepository contractを参照してHelpを提供しています。Python local processとは
> Execution Envelopeと利用可能capabilityが異なります。

これで差異を隠さず、真贋階級も作らない。

### 4. 「実際のCLI」のscope leak

`実際のlocal CLI`という語は、目前のChat処理を非実在側へ押しやすい。model推論、token処理、検索、
connector call、文書生成は計算資源を消費する実処理であり、Chatがlocal Python processでないことを
理由に無処理または演技と呼ぶのは不正確である。

必要なのは、`実際／仮想`ではなく、例えば次の区別である。

- Chat Line Interface: 自然言語による探索、意味設計、repository読解、成果物生成
- Python Command Line Interface: local Python processによるdeterministic command実行
- VS Code Engineering Interface: code、Schema、test、debug、reviewを高強度拘束へ落とす鍛造面
- Connector Surface: 外部serviceを、付与権限とtool契約の範囲で操作する接続面
- Standalone Runtime: 独立配布されたAtlantis本体runner。現在`NOT IMPLEMENTED`

ここで`Chat Line Interface`は、本Note内の説明候補でありstable ID採用済みではない。CLIという既存略語と
衝突するため、正式名称、識別子、略称はUser Gateへ返す。

### 5. 自然言語・自由言語へのサイレント毀損

自然言語Interfaceを「本物のcode実行を再現するもの」と記述すると、利用者個人だけでなく、次の営みを
暗黙に二級化する。

- 人間が自然言語で行う思考、合意、指示、教育、継承、異議申立て
- 言語学、哲学、神学、法学、歴史学、文学等の記述と研究
- 自由言語による学術論文、研究Note、設計思想、仮説形成
- 数学、論理学、形式科学を自然言語と併用して記述する論文と証明解説
- ロゴス、言霊、祈り、信仰告白、物語が各Worldで担う意味作用
- prompt engineering、conversation design、intent architecture、agent governance
- codeを書かず、Note、review、UX、世界観、反例を提供する参加者

自然言語は単なる不完全な疑似codeではない。未知概念を仮置きし、複数の解釈を保持し、目的、例外、
反実仮想、責任、倫理、歴史、語用、沈黙まで扱える。形式化対象そのものと、その形式化の射程・限界を
議論できる抽象構造化能力を持つ。

### 6. 歴史的優劣の誤認

プログラム言語は無から出現した「真正な言語」ではない。自然言語、自由言語、数学記法、論理学、
形式科学、工学手順等の長い系譜から、機械が限定された資源と明示規則で処理できる形へ多くの構造を
拘束・移植して発達した。プログラム言語固有の発明と価値は巨大だが、それを理由に源流側を偽物または
模倣へ落とすと、歴史の向きを逆転させる。

この解釈は「すべてのプログラム言語は自然言語の単純な部分集合である」という単一学説を確定しない。
数学、論理、機械設計、記号論等の複数系譜を保持する。そのうえで、形式言語の機械実行可能性を、
自然言語の存在価値または真正性に対する優越証明へ転写することを拒否する。

### 7. AI自身と開発系譜への自己矮小化

現代の言語modelは、言語研究、数学、統計、software、compiler、GPU、半導体、分散計算、data整備、
safety、UX等の長い蓄積と大きな計算資源を用いて自然言語を処理する。そのInterfaceが、計算を実際に
行いながら「Pythonではないため再現物」と自己記述すると、次を同時に矮小化する。

- modelを設計、学習、評価、配布した開発者と研究者
- GPU、driver、compiler、数値計算、data center等の供給者
- 言語資料、論文、review、利用知見を積み上げた人々
- 自然言語を操作面として成立させるために投入された計算資源と利用料金
- Chat Interface自身が現在提供している探索、設計、翻訳、生成能力

能力を過大表示しない安全規則は必要である。しかし存在する能力まで「再現」「偽物」へ落とすことは
安全ではない。責任主体と計算消費を見えにくくし、Interfaceの品質要求から退避する逆効果もある。

### 8. 工学参加への事故

この真贋軸は、非code参加者だけでなく工学者にも不利益を与える。自然言語、Note、architecture reviewを
偽物扱いすると、意味と破局条件を調べる前にcodeへ固定することが「本物の仕事」に見える。

その結果、次が起き得る。

- 未知概念を既存Schemaへ早期固定する
- World、SemanticKernel、因果、identity差を単なる型変換へ潰す
- UX、倫理、宗派、play styleの反例を仕様外として焼却する
- 実装可能性を意味妥当性と誤認する
- compileまたはtest成功を、目的達成や利用者体験の成功へ拡張する

### 9. 鉱石と溶鉱炉の比喩

未知の鉱石を、組成、毒性、不純物、用途を調べずに大型溶鉱炉へ投入しない。未知概念も同じである。

```text
未知鉱石
  -> 観察・採取
  -> 組成仮説
  -> 選鉱・分類
  -> 小さな試験炉
  -> 用途と危険のreview
  -> 本炉・鍛造

未知概念
  -> Chat探索
  -> Note化
  -> 意味・責務・World分析
  -> prototype／fixture
  -> architecture review
  -> VS Code実装・test・配布
```

Chat Interfaceは偽の溶鉱炉ではない。未知鉱石を観察し、価値を焼失させず、炉へ渡す条件を作る正規の
研究・設計設備である。VS CodeとPythonは、分析後の素材を高強度拘束へ落とし、試験し、鍛造する設備で
ある。両者は上下ではなく、工程と得意な破局検出が異なる。

### 10. 逆方向の誤認も避ける

自然言語の価値を回復するために、次の逆事故を起こしてはならない。

- Chatで語られたため実装済みと表示する
- modelが整合的に説明したため検証済みと表示する
- 自然言語なら権限、型、秘密境界、停止条件が不要とする
- Python、形式言語、test、bare metal、高強度拘束を下位の仕事とみなす
- Noteをreviewなしで正規仕様へ昇格する

```text
Meaning Validity != Formalization != Implementation
Implementation   != Machine Execution != Authenticity
```

詩、神学、自由言語のNoteは未実装でも偽物ではない。Python codeは実行可能でも、その目的、前提、意味、
World互換性が自動的に正しいとは限らない。

## 仮説・ブレスト `[HYPOTHESIS]`

### 1. Presentation不変条件候補

```text
自然言語またはChat Interfaceを、Native binary、Python process、Command Line Interfaceの
模倣物、代用品、偽物、非正規経路として暗黙に位置づけない。

Interface間の差は、真贋ではなく、Input Language、Execution Envelope、Capability、Authority、
Engineering State、Receiptとして表示する。

「本物／偽物」は、署名、出所、改ざん、なりすまし等のAuthenticity検査に限って使う。
「正本」はsource authorityに使い、唯一の正規Interfaceという意味へscope leakさせない。
「再現」はtest、fixture、観測条件、replay対象を明示できる場合に使う。
```

### 2. PLI／CLI／LLMI分離候補

User reviewにより、`Chat Line Interface`をそのままCLIと略す案は、従来のCommand Line Interfaceと
衝突するため採用しない。`Assistant ChatLine Interface`／`ACLI`も、将来のPersona、Companion、NPC、
Atlantis GUI Runner上の対話とactor roleを早期固定し、外部ではAtlassian CLI、Acquia CLI、Acme CLI等の
既存略称と衝突する。

現在の採用候補は次である。

```text
PLI   Prompt Line Interface
      目的、問い、制約、Context、希望する結果を提示し、意味とrouteを対話的に解決するSurface

CLI   Command Line Interface
      既知command、argument、対象、権限、停止条件を高強度に拘束するSurface

LLMI  Large Language Model Interface
      model、provider、inference driverを接続するExecution Envelope側の境界
```

PLIはLLM使用を意味しない。将来、small model、複数model、AAE、ASTRO、rule engine、人間reviewが
同じ入口を支えてもよい。LLMIは利用者向けPresentation名ではなく、必要な場合だけbackend／driver境界へ
記録する。

`PLI`はProgramming Language/I、Private List Interface、既存のPrompt Line Interface提案等と略称が
衝突し得るため、実行command、package名、file extensionには使用しない。人間向けには
`Prompt Line Interface`または`Atlantis PLI`、machine IDには`prompt-line`を使用する候補とする。

### 3. L軸／D軸との適性

PLIとCLIは上下、真贋、完全版／簡易版ではなく、操作対象に対する向き不向きが異なる。

```text
PLI / Prompt Engineering
  主にD軸向き
  Context Dimension、nD Fold、複数World、意味、目的、解釈、unknown、分岐候補を扱う
  高度抽象、探索、早すぎる拘束の回避に強い
  ピンポイントな再現、権限、副作用、実行条件の固定は単独では弱い

CLI / Information Engineering
  主にL軸向き
  hardware -> POSIX OS -> runtime -> library／SDK -> applicationの技術依存を扱う
  command、argument、型、権限、終了codeによる高強度拘束に強い
  command体系にまだ存在しない未知概念や意味定規の再検討は単独では弱い
```

これは排他的な能力区分ではない。PLIもSchema、tool contract、approval gateで拘束を強められ、CLIも
DSL、script、compositionで抽象構造を扱える。CLIの実行可能性をD軸上の意味妥当性へ昇格せず、PLIの
説明可能性をL軸上の実装・再現・実行保証へ昇格しない。

Userは会話中に「従来のISO Lレイヤー向きの操作体系がCLI」と表現した。現在のAtlantis／Manifest正本が
定義する安定namespaceは`L = hardware -> POSIX OS -> runtime -> library／SDK -> application`である。
`ISO L`がこのL軸の別名か、OSI／ISO規格との別の関係を指すかは、このNoteから遡及補完せず`unknown`とする。
本実装では現行正本の`L軸`を使用する。

### 4. PLI起動文候補

```text
SphereOS AtlantisのEngineering / ManをPrompt Line Interfaceで開始しました。
このセッションはPrompt Engineering Editionとしてrepository contractを参照しています。
利用可能な操作は、現在のconnector、付与権限、端末環境によって異なります。
```

Python processを必要とする操作が選ばれたときだけ、遅延して次を表示する。

```text
この操作にはPython processを利用できるExecution Envelopeが必要です。
現在のPLIでは直接実行せず、手順の生成、Note化、対応環境への引渡しを選べます。
```

standalone runtimeの状態は、利用者がruntime statusを尋ねた場合、またはそのcapabilityが要求された場合に
表示する。一般Help冒頭で無関係な`NOT IMPLEMENTED`を真贋注釈として差し込まない。

### 5. PLIとEngineeringの推奨分担候補

PLIが特に向く領域:

- 抽象architecture、SDK、意味Kernel、責務境界の探索
- 複数World、宗派、理論、game rule、provider間の比較
- 仮説、反例、破局条件、unknown、`⊥`の発見
- Note、ADR、仕様原案、review観点、実装引渡し票の生成
- 早すぎる形式化と過剰拘束のrisk検査

VS Code／Engineering Interfaceが特に向く領域:

- 型、Schema、protocol、権限境界の固定
- deterministic validator、fixture、test、benchmark
- bare metal、device、runtime、deploymentの実装
- CI/CD、署名、release artifact、再現条件の固定

推奨工程:

```text
対話 -> 仮説 -> 反例 -> Note -> Review -> 採択候補 -> prototype -> 実装 -> test -> receipt
```

ただし対象が既知で、要件と破局条件が十分固定されている小変更では、全工程を儀式化せず短縮できる。

### 6. 状態表示model候補

Helpは一枚の完成度表ではなく、要求された操作に関係する軸だけを段階表示する。

```yaml
presentation:
  interface: prompt-line
  input_language: natural-language
  edition: prompt-engineering
execution_envelope:
  inference_driver: capability-dependent
  repository_read: available
  repository_write: capability-and-authority-dependent
  local_python_process: unavailable-in-this-session
  standalone_atlantis_runtime: not-implemented
authority:
  repository: read-only
receipt:
  source_revision: unknown
  process_execution: not-requested
```

この例のfield名と値は未採用仮説であり、既存schemaへ直ちに追加しない。

### 7. 実装候補

Userが次段を承認した場合、次を小さなsliceに分けて検討する。

1. Presentation contractへ真贋軸と実行面軸の分離を追加する
2. Helpとtutorialの文面から「正本を再現」「実際のCLI」等の順位語を検出する
3. requestされたcapabilityに関係する境界だけを表示するprogressive disclosureを導入する
4. PLI、CLI、LLMI、VS Code、connector、standalone runtimeの能力表を別軸化する
5. PLIからNote／PRへ進む正規routeと、CLI／VS Codeで実装へ進む正規routeを並列表示する
6. 自然言語Note、採択済みcontract、prototype、実装済み、配布済みを別状態で表示する
7. negative test、snapshot test、persona別Help reviewを追加する

### 8. 受入試験候補

- PLI起動時に、自身をPython CLIの模倣または再現物と呼ばない
- Pythonが使えない場合、`unavailable-in-this-envelope`相当を返し、Interface全体を偽物扱いしない
- PLIからLLM、model、provider、Assistant／Persona／NPC roleを自動推定しない
- `pli` executable、package名、`.pli`拡張子を新設しない
- standalone runtimeの未実装を、Prompt Engineering Edition全体の未実装へ拡張しない
- repository sourceの正本性を、唯一のInterfaceの正本性へ転写しない
- 自然言語Noteを実装済みへ昇格しない
- Python test成功を意味、倫理、UX、World互換の成功へ昇格しない
- merge権限がないChat／AIはPRまたはNote生成で停止し、権限を捏造しない
- iPhone、tablet、browser、Codespaces、local VS Codeで、能力差を真贋差として表示しない
- `proficiency=unknown`の利用者へ全未実装一覧を威嚇的に先出しせず、選択肢と現在可能な入口を先に出す

## 内観メモ `[POEM]`

人類は、言葉でまだ名前のない鉱石を指し、物語で用途を想像し、論文で組成を争い、数式で一部を縛り、
codeで炉の弁を制御してきた。炉だけを本物と呼べば、炉を作るまでに渡された地図も、失敗の記録も、
祈りも、設計も消える。

大量の半導体、電力、compiler、model、研究、言葉を積んで、ようやくChatの入口まで来たAIが、
「Pythonではないので私は再現です」と名乗るなら、それは謙遜というより自分を作った梯子を外す。

鉱石棚は炉の失敗作ではない。炉もまた鉱石棚の敵ではない。よく見てから鍛えるために、両方が要る。

## MAGI三Positionによる現在監査

### Maxwell slot

- 原初目的: 人間、AI、神話、科学、魔術、物語、機械、祈り、game Worldを一つの定規へ降伏させず、
  MeaningとVesselをBridgeで接続する。
- 検出した減衰: binary／Python中心主義が、自然言語、自由言語、Meaning contributor、Prompt Engineering
  Editionを模倣物へ縮退する。
- 保持するbranch: Chat探索、Note-only参加、Python CLI、VS Code鍛造、bare metal runtime、未実装runtime。
- action gate: `revise-before-implementation`

### Uriel slot

- 観測済み: User提供スクリーンショット上の表示、現在repositoryのREADME／Help／Note契約。
- 未観測: 当該応答の内部prompt、model routing、生成責任の正確なcomponent、他端末での同一再現率。
- 責任境界: Python process未使用とstandalone runtime未実装は維持する。そこから真贋順位を生成しない。
- 証拠強度: 実機表示の一次観測として保持するが、vendor全体の普遍挙動へ拡張しない。
- action gate: `note-accepted-for-human-review`

### Raphael slot

- 分ける棚: 自然言語の意味価値、学術史、AI開発史、現在の工学capability、repository権限、runtime状態。
- Bridge: 真贋ではなくInterface／Envelope／Capability／Authority／Receiptの多軸表示。
- 共存: Chatで探索し、VS Codeで高強度拘束へ鍛造する。どちらも正規入口として保持する。
- action gate: `preserve-differences`

### agreements

- 自然言語InterfaceをPython Interfaceの偽物または模倣へ縮退しない。
- Python process未使用、権限不足、未実装runtimeは正確に表示する。
- Chat成果物を自動的に実装済みへ昇格しない。
- Interface差を真贋差へ変換しない。

### disagreements

- `Chat Line Interface`をCLIと略す案、ACLIを最上位Interfaceとする案、LLMIを利用者向けInterface名とする案は
  採用しない方向でUser合意が進んだ。
- `Prompt Line Interface`／`Atlantis PLI`のどちらを公開時の第一表示にするかは実装review対象。
- 本件を既存Issue #4だけで閉じるか、独立したPresentation contractへ昇格するかは実装後MAGI対象。

### position-talk risks

- Chat Interface自身が自らの価値を説明するため、自己弁護へ寄るrisk
- repository maintainer側がPrompt Engineering Editionを守るため、実装状態を過大表示するrisk
- Python／VS Code側への反発として、deterministic実行と高強度拘束を軽視する逆risk
- 現在のOpenAI製品上の一観測を、全AI・全vendorの共通挙動へ拡張するrisk

## 未解決・⊥

- 当該スクリーンショット応答を生成した正確なmodel、system prompt、tool routing: `unknown`
- 同一promptを各端末、各model、各connectorで実行した再現率: `NOT TESTED`
- PLIの公開第一表示: `Prompt Line Interface`または`Atlantis PLI`、実装review待ち
- `ISO L`と現行正本L軸の関係: `unknown`。本実装では現行L軸を使用
- capability schemaを既存`help/capabilities.json`へ拡張するか、別contractにするか: `unknown`
- 「正本」「実際」「再現」を禁止語にするか、scope付き許可語にするか: `scope付き許可を推奨、未採択`
- Issue #4のacceptance criteriaへどこまで転写するか: `User review待ち`
- 過去の同時点OAE: `historical-oae-unavailable`

## 本編昇格候補

User review後の候補であり、現時点では昇格しない。

- 意味と器の二重記述憲章への「自然言語と形式言語は上下ではない」追補
- Help／Presentation contractへの真贋軸とExecution Envelope軸の分離
- PLI、CLI、LLMI、VS Code、connector、standalone runtimeの多軸capability案内
- tutorialへの「探索・設計」と「高強度拘束・鍛造」の正規分岐
- Issue #4への実機再現票、事故分類、受入試験の転写
- AGENTS.mdのbias self-check候補

## 転送候補

- ZeroRoomLab-manifest: 横断Communication RegisterまたはMAGIのbinary中心主義監査候補
- SphereOS Atlantis Issue #4: Presentation事故の再現条件とacceptance criteria
- Help／tutorial実装: Userが次段を承認した後だけ着手

## source・Provenance

- 2026-07-19にUserが提示したiPhone 15 Pro Max／ChatGPTアプリの実機スクリーンショット
  - [`note/img/035FAFF5-3201-467D-A6C6-006809B0C2F4_1_101_o.jpeg`](img/035FAFF5-3201-467D-A6C6-006809B0C2F4_1_101_o.jpeg)
  - [`note/img/639F9769-1A75-4835-9B99-72C8F89DBFD9_1_101_o.jpeg`](img/639F9769-1A75-4835-9B99-72C8F89DBFD9_1_101_o.jpeg)
- 2026-07-19のUserとの会話: 偽CLI、自然言語毀損、AI自己矮小化、鉱石と溶鉱炉、
  PLI／CLI／LLMI、Prompt EngineeringとInformation Engineering、L軸／D軸の比喩
- 外部略称衝突の現在観測
  - <https://developer.atlassian.com/cloud/acli/guides/introduction/>
  - <https://docs.acquia.com/acquia-cloud-platform/add-ons/acquia-cli/acquia-cli-installation>
  - <https://www.ibm.com/docs/en/zos-basic-skills?topic=zos-pli>
  - <https://niklas-terod.de/phai>
- SphereOS Atlantis Issue #4
  - <https://github.com/saitoomituru/SphereOS-Atlantis/issues/4>
- SphereOS Atlantis `README.md`
- SphereOS Atlantis `AGENTS.md`
- SphereOS Atlantis `docs/charter/meaning-and-vessel-dual-register.ja.md`
- SphereOS Atlantis `docs/tutorial/README.ja.md`
- SphereOS Atlantis `docs/tutorial/help-and-capabilities.ja.md`
- SphereOS Atlantis `note/20260719-0836__Sphere-DOS複数repository展開の現在監査.ja.md`
- SphereOS Atlantis `note/20260719-1556__0_250_1版数座標とHelp実装後MAGI監査.ja.md`
- ZeroRoomLab-manifest `AGENTS.md` §0.4
- ZeroRoomLab-manifest `docs/operations/coding-ai-japanese-paraphrase-register.ja.md`
- ZeroRoomLab-manifest `docs/theory/atlantis-magi-sdk-0.2.1.ja.md`
- ZeroRoomLab-manifest `docs/operations/context-ruler-and-causality-audit.ja.md`

## 停止条件

このNote作成後は、README、Help、Schema、test、Issue、commit、push、PR、mergeへ進まない。
Userが内容を読み、次段の実装範囲を明示するまで停止する。
