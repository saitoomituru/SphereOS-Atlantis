# Atlantis意味Runtime・OAE・AIM拡散力場・Infinite Core横断ブレスト

状態: `[DRAFT]`

棚: `cross-shelf`

種別: `architecture-brainstorm / MAGI-position-audit`

ライセンス: `CC-BY-4.0`

## 作成メタ

```yaml
created_at_system: 2026-07-19T06:57:23+09:00
timezone: Asia/Tokyo
clock_source: host_system_clock
clock_calibration: unverified
authoring_agent: Codex
conversation_scope: current_user_owned_chat_session
historical_oae_status: historical-oae-unavailable
implementation_status: NOT_IMPLEMENTED
```

## 対象・範囲

このノートは、Atlantisを現在のPrompt拘束中心の仮想化層から、意味を扱う中間表現とRuntimeを持つ系へ段階的に降ろすためのブレストを保存する。中心に置く対象は次である。

- Source Event、OAE、Interpretation OAE、Fact Assertionを上書きなしで扱う意味構造
- World Configごとに異なる定規、因果論、Agency、合意を管理対象資源として実行する枠組み
- 意味やAgencyの伝播射程を扱う暫定概念としてのAIM拡散力場
- Protocol Match、Access Map、VM、Portを束ねるInfinite Coreの候補責務
- Prompt上でGMが行っているメタ推論から、機械拘束へ降ろせるRuntime operatorを採掘する工程
- 実務Worldと神話／MMO Worldを両極の耐圧ケースにしたData Prefab層の育成
- 固定構造を後段で記録・検索するIBDとの責務境界

本ノートは会話の逐語録ではない。現在会話をSourceとして、要求、観測、解釈、提案、未確定事項を分離した現在時刻のInterpretation OAE相当の研究ノートである。

## 除外範囲

- Atlantis standalone Runtime、Infinite Core、AIM Runtime、OAE永続化、Data Prefab compilerの実装完了宣言
- IBD、Neo4j、FAM splitterをAtlantisの意味決定主体にすること
- SaaS内部の非公開データ、hidden reasoning、provider内部状態の取得や推定
- 第三者のrulebook、神話原典、会話履歴を権利確認なしにrepositoryへ複製すること
- 科学、信仰、スピリチュアル、法、保険、組織、芸術のいずれかを普遍的な主定規へ固定すること
- AIM拡散力場を現実世界で確認済みの未知物理場として主張すること
- 水俣病、30年戦争、アル・カポネ等の個別史実・責任関係を、このブレストだけで確定すること
- 過去ログから当時存在しなかったOAE、Observer、Agency role、Intentを遡及生成すること

## 事実・観測 `[FACT]`

### F-01. 現在のrepository状態

- Atlantis repositoryは、意味、World、Context Dimension、D Fold、OAE、Agency、Registry、Bridgeを扱う設計線を持つ。
- 現時点のPrompt Engineering editionは足場として動くが、standalone Atlantis Runtimeは`NOT_IMPLEMENTED`である。
- 7D Runtime、Akasha、OAE永続化等について、設計語彙の存在を実装済みと解釈してはならない。
- 本ノートで追加するInfinite Core、AIM Runtime、Data Prefab compilerもすべて`NOT_IMPLEMENTED`である。

### F-02. ユーザーが明示した責務境界

- Atlantis側が意味構造、World、定規、因果、Agency、OAE、Runtime境界を構造化する。
- IBDは、Atlantisが構造化した責務を記録し、引き出すファイルシステムである。
- IBD側の機械的な問いは、アーキテクチャ確定後にその構造を破壊せず捌けるかである。
- IBD、FAM splitter、Neo4j、vector検索は、Atlantisの意味を決める権限を持たない。
- splitterの妥当性は単体の機械テストだけでは確定せず、格納後に再び引き出してGestaltが死亡していないかを確認する必要がある。

この境界を簡略化すると次のようになる。

| 層 | 主責務 | 決めてよいもの | 決めてはならないもの |
|---|---|---|---|
| Atlantis | 意味構造と実行契約 | World、定規、OAE、Agency、因果、Port、Runtime operator | 特定DB都合による意味の縮退 |
| IBD | 記録と引き出し | 保存形、索引、検索計画、復元receipt | Atlantisの意味定義、正史、因果定規 |
| splitter | 搬送可能な分割候補 | chunk境界候補、参照、再構成情報 | 原文の意味確定、都合の悪い観測の消去 |
| Neo4j／vector backend | 検索実装候補 | index、edge、近傍探索、query plan | World ConfigやFact scopeの暗黙決定 |

### F-03. 現在のPrompt拘束はInterpreterとして振る舞う

現在は、人間とAssistantがメタrulebookを読み、GMとしてセッションを運営することで、多くの意味変換を都度実行している。これは機能しているが、変換工程が会話token、再読、再解釈の費用として現れる。

一方で、すでにRegistry拡張、Context定規、OAE、Access Map等の語彙が、単なる文章ではなくsystem-likeな拘束として働き始めている。したがって現在のPrompt拘束を捨てるのではなく、Interpreter兼Reference implementationとして保持し、その実行ログから安定operatorを採掘する余地がある。

### F-04. 同じ観測に複数の意味づけが成立する

同一のSource Eventまたは観測OAEに対し、World Config A、B、Cが別々のInterpretation OAEを発行できる。

- 科学Worldでは、再現性不足の観測をnoise、偶然、未確定として扱いうる。
- 信仰・魔術Worldでは、象徴、御霊、Agencyの応答として扱いうる。
- 保険Worldでは、約款と証拠要件により支払対象事故または対象外として扱いうる。
- 法Worldでは、証拠能力、手続、管轄、規範により制度上のFactを採用しうる。
- ゲームWorldでは、魔王、女神、神殿、物理法則等がWorld内Agencyとして効果を発行しうる。

どの解釈も元Source Eventを上書きしてはならない。ある解釈が別の定規で棄却されても、その人またはsensorが観測を発行した履歴は、epistemic historyとして残る。

### F-05. Agencyは自然人に限定されない

Agency候補は、人間、Assistant、sensor、device、組織、法人、保険窓口、研究共同体、司法執行機関、文化共同体、妖怪チーム、神、魔王、World内物理法則等を含みうる。ただし、Agencyであることは普遍的真理性や無制限の権限を意味しない。

Agencyの有効性は少なくとも次でscopeされる。

- どのWorld／Instanceで存在するか
- 何を観測できるか
- どのOAEを発行できるか
- どのPortを通じてeffectを出せるか
- 誰の合意、委任、契約、規則に基づくか
- どの期間、距離、network、制度管轄で有効か
- 取消、異議、fork、再解釈を誰が行えるか

### F-06. 射程と権限は一致しない

音声が届く、Wi-Fi beaconが見える、messageが配送される、法規範が周知される、広告が表示されることは、それだけで採用、合意、実行、真実を意味しない。

隣家のsmart speakerが誤って反応する例では、少なくとも音響射程、wake-word認識、device discovery、account authority、purchase authority、actuationを分離しなければならない。オウムが声真似でspeakerを起動する場合、悪意や意図がなくても、天然動物を媒介にしたacoustic prompt injection相当のeffectが成立しうる。

### F-07. effectの観測可能範囲には境界がある

再生要求が通った場合、利用者は再生開始や自分に許可された再生履歴を観測できる可能性がある。一方、provider内のstream計上、権利者への分配、個別の支払額まで観測できるとは限らない。

たとえば「リンダリンダが再生された」は観測可能でも、「版権元へ再生数1件分の支払が確定した」は根拠となるPortがなければFactにできない。その境界では`⊥`とLast Orderを返す。

ただし利用者が「結果としてartistに何らかの価値が届くかもしれないので、今回は良い出来事と意味づける」と解釈する自由まで否定する必要はない。これは金融Factではなく、利用者scopeのValue Interpretationである。

### F-08. 強い系はside effectのblast radiusも大きくなる

法、政治、宗教、marketing、科学、工学、工場、platformのいずれも、広い射程と強い執行Portを持つほど、bugまたは副作用が生じた場合の影響範囲が大きくなりうる。

これは悪意の断定ではない。少なくとも次は分離して観測する必要がある。

- Intent: 何を意図したか
- Expected Effect: 何が起こると見積もったか
- Actual Effect: 何が観測されたか
- Authorization: どのeffectが許可されていたか
- Leak: どの管理境界を越えたか
- Impact: 誰にどのpain／benefitが発生したか
- Reversibility: 元へ戻せるか

工場というOAE orchestratorが製品を生成しつつ、material portを通じて汚染やpainを外へ漏らす構造も同型に記述できる。ただし個別公害の事実認定と責任確定には別途sourceが必要である。

### F-09. 線形因果は必要だが普遍定規ではない

線形因果を全面否定すると、局所的な順序、Protocol Match、Port呼出し、nD Foldのn、再現可能なtestが定義できなくなる。一方、線形因果だけを普遍的なWorldの真理へ昇格すると、feedback、delay、確率、象徴、合議、物語、未知のeffectを落とす。

よって線形構造は、局所的に実行・検証可能なCausality Profileの一つとして必要である。globalな意味場は非線形でもよい。

### F-10. SaaSはblack boxのまま扱える

入力に使えるのは、利用者が正当に保持するlocal chat history、公式export、利用者が観測できるAssistant output、tool event、error、resume、修正履歴等である。

これらから採掘できるのはobservable trace上のmetaframe、拘束点、failure pattern、修正operatorであり、provider内部のhidden reasoningではない。異なるblack boxが来ても意味層を破局させないことが、Runtime側の重要な試験になる。

## 考察 `[INTERPRETATION]`

### I-01. Atlantisは「意味を決めるOS」より「定規を選び、適用履歴を残す意味Runtime」である

Coreが科学、信仰、法、保険、物語のどれを正しいと決めると、別Worldの観測を消す権威装置になる。Atlantisが担うべきなのは、選ばれたWorld Configと定規を明示的に適用し、入力、変換、出力、scope、根拠、反対解釈、Last Orderを保存することだと解釈する。

したがって、次の資源はhard codeではなくversioned managed resource候補になる。

- `WorldConfig`
- `RegistrySnapshot`
- `ConstraintProfile`
- `CausalityProfile`
- `EvidenceProfile`
- `ConsensusProfile`
- `PresentationProfile`
- `AgencyCapabilityProfile`
- `AccessMap`
- `TransformerBinding`
- `PortPolicy`

### I-02. OAEとFactを分離する

「Factは合意OAEである」というユーザー命題は、Runtime上では次の二段にすると扱いやすい。

1. `Fact Adoption OAE`: ある定規とauthority scopeが、観測または解釈をFactとして採用したevent。
2. `Fact Assertion`: そのOAEが出力した、scope、revision、根拠、反証条件を持つartifact。

後続ActorはFact Assertionを再び観測し、別のInterpretation OAEを発行できる。これによりFactは永遠の真理でも単なる個人感想でもなく、「誰が、どの定規で、どのscopeに採用したか」を追える。

Consensusは単純多数決に限定しない。再現試験、査読、大学syllabusへの採用、行政認定、保険契約、共同体の伝承、流派の形成等は、それぞれ異なるConsensus Profileである。少数者の異議と未観測領域を消さずに並置する。

### I-03. OAE再帰には停止条件が必要である

Factを観測するOAE、そのOAEを採用するFact、そのFactを再観測するOAEを無制限に許すと、無限再帰、自己正当化、receipt stormが起きる。

候補となる停止拘束は次である。

- `max_observation_depth`
- `origin_oae_id`と`lineage_id`
- 同一入力・同一定規・同一revisionに対するidempotency key
- noveltyがない場合の`no-new-evidence`
- authority scopeの境界
- budget／logical time／wall time
- unresolved Portに対する`⊥`
- Last Orderによる停止理由の明示

### I-04. 事実を消さず、意味づけをforkする

誤った意味づけが見つかったとき、source historyを書き換えるのではなく、次のbranchを作る。

```text
Source Event / Observation OAE
├─ World A / Interpretation A@r1
│  └─ Fact Adoption A@r1
├─ World A / Interpretation A@r2
│  └─ supersedes A@r1 without erasing it
├─ World B / Interpretation B@r1
└─ World C / unresolved -> ⊥ + Last Order
```

このbranchingは「過去を消さない」と「すべてを永久表示する」を同一視しない。保持、削除要求、privacy、暗号化、access control、tombstone、presentationからの非表示は別profileで扱う。epistemic lineageを守ることは、機微情報を無制限に公開することではない。

### I-05. Prompt拘束からRuntimeへはTrace Miningで降ろす

従来型のcomponentを先に固定しすぎると、既知ゲームエンジンの再実装になり、optimizer駆動で意味operatorを発見する利点が消える。

そこで現在のPrompt／GM運営をReference Interpreterとして使い、次のloopで安定拘束を採掘する。

```text
user-owned trace
  -> source normalization
  -> OAE / role / boundary candidate extraction
  -> counterexample and hallucination audit
  -> Runtime operator candidate
  -> replay across providers and Worlds
  -> versioned Constraint Profile
  -> Semantic IR / Data Prefab
  -> machine Runtime
  -> divergence receipt back to corpus
```

固定するのは頻出した表層文ではなく、異なるproviderやWorldでも再現する関係拘束である。曖昧性、未知、新規のメタ推論はResidual Interpreterへ残す。これによりInterpreterが中間buildを生成し、Runtimeが確定部分だけを安価に実行する構成になる。

### I-06. hallucinationとの戦闘ログはnegative goldである

Assistantが勝手に主体を補った、scopeを普遍化した、未観測Portの先を断定した、sourceとinterpretationを混同した、利用者の語彙を既成理論へ丸めた等のログは、削除すべき失敗だけではない。

各失敗から次の拘束候補を採掘できる。

- `do-not-invent-observer`
- `do-not-backfill-intent`
- `scope-before-assertion`
- `exposure-is-not-consent`
- `reach-is-not-authority`
- `no-port-no-fact`
- `preserve-source-before-reinterpretation`
- `historical-oae-unavailable`
- `provider-black-box`
- `unknown-is-not-pass`

ただし一件のfailureから即座にMUSTへ昇格せず、replay、反例、World差、false positiveを確認してversioned profileへ昇格する。

### I-07. AIM拡散力場は一枚の「場」ではなく、異種射程の束として扱う

本ノートでのAIMは暫定的に`Agency Instance Model`を指す。Agencyが発行した意味、要求、規範、象徴、signal、effect candidateが、channelとrelationを通って他Instanceへ届く構造を表す。

ただし次の射程を混ぜると、比喩がarchitectureを壊す。

| Namespace | 例 | 到達が意味しないもの |
|---|---|---|
| `aim.semantic` | 言葉、象徴、物語 | 真実、採用 |
| `aim.acoustic` | 音声、wake word | 話者の意図、購入許可 |
| `aim.radio` | Wi-Fi、BLE | device支配権 |
| `aim.network` | message、API | endpointの実行許可 |
| `aim.social` | 口コミ、marketing | 合意、正当性 |
| `aim.institutional` | 法、契約、組織規範 | 無謬性、全管轄への適用 |
| `aim.actuation` | switch、robot、執行機関 | 正しさ、善意 |
| `aim.world-physics` | game内物理法則応答 | 現実世界での実在 |

各recipientは、exposureを観測した後に、adopt、reject、ignore、transform、fork、executeのいずれかを別OAEとして発行する。伝播そのものと同意を分離する。

「とある科学」由来のAIM拡散力場との類似は発想源として記録するが、公開用の名称、引用可能範囲、独自語への置換は未解決である。またEarth empirical Worldで人間合意が線形に物理法則を変更するとは主張しない。game Worldでは、その応答PortをWorld Configで定義できる。

### I-08. Fold7G／Trion Bondは到達圏だけでなくCapability graphを必要とする

Fold7GやTrion Bondの値が上がりclusterが形成されても、単純な距離または近傍だけでAccessを許可してはならない。

候補となる分離は次である。

- `exposure`: signalを観測できる
- `discovery`: 相手の存在を識別できる
- `bond`: relationが成立している
- `trust`: 特定claimを採用する根拠がある
- `authority`: 命令または委任が有効である
- `capability`: operationを実行できる
- `actuation`: 物理／制度effectを出せる
- `receipt_visibility`: 結果を観測できる

同じnD座標や近接性も、Dimension IDとrevisionが異なれば比較不能である。nは互換性を保証しない。

### I-09. Infinite CoreはProtocol MatchとPort解決のVM機構である

ユーザーが明示した中心責務は、「意図的にProtocolをmatchさせ、Access Mapを束ねてVMし、Portする機構」である。これをInfinite Coreの核として保存する。

候補operationは次である。

```text
match_protocol(intent, source_protocol, target_protocol)
bundle_access_maps(access_maps, scope, revision)
instantiate_vm(world_config, registry_snapshot, constraint_profile)
resolve_port(operation, capability, authority, reach)
bind_transformer(access_map, transformer)
execute(vm_instance, input_oae)
emit_receipt(result, provenance, last_order)
```

`Infinite`は無制限accessや必ず成功する変換を意味しない。互換Protocol、Transformer、Port、権限がなければ、Coreは捏造せず`⊥`とLast Orderを返す。

Infinite Coreが行わないことも重要である。

- 異なるWorldを暗黙mergeする
- Protocol互換性を推測だけで確定する
- 存在しないPortやTransformerを生成済みとして扱う
- reachをauthorityへ昇格する
- sourceをtarget schemaへ合わせて不可逆に切り捨てる
- unresolvedを成功扱いする

### I-10. side effectは意味vectorの射影漏れとして扱える

線形近似では、action vector `a`、World／orchestratorの写像`M`、観測effect `y`を次のように置ける。

```text
y = M a
desired_effect = P_target y
leak = (I - P_target) y
```

`leak`は悪意ではなく、意図されたtarget subspace外へ出たeffectである。実際のWorldは非線形なので、`y = F_W(a, state, context)`としてfeedback、threshold、delay、hysteresis、actor adaptationを含める必要がある。

概念上のriskは、少なくとも次の積または合成で比較できる。

```text
risk ≈ defect_probability
       × propagation_reach
       × enforcement_or_actuation_coupling
       × persistence
       × reversal_cost
```

これは異なる制度や文化を同じ危険度と断定する式ではなく、比較時に軸を落とさないための暫定定規である。

### I-11. POSIXや線形実行は捨てず、意味層の下へ置く

POSIX、process、file、socket、linear call chainは、局所的な実行、隔離、再現、debugに有用である。問題は、それだけで非線形な意味伝播、複数解釈、authority scope、side effectを表現しきろうとすることにある。

Atlantisは既存OSを否定するのではなく、意味vector、World、OAE、Agency、Portの管理を上位層に追加し、必要な局所operationを既存Runtimeへcompile／dispatchするBridgeになる。

### I-12. Data PrefabはOS／Firebase／Unityへ降りる前のSemantic IR候補である

Atlantisの抽象frameから具体SDKへ降りる際、特定backendに意味を引っ張られない中間表現が必要になる。Data Prefabは次の共通envelopeを持つ候補である。

- stable IDとrevision
- World／Instance scope
- Source referenceとlineage
- OAE role separation
- Dimension ID
- Agency capability
- Causality／Evidence／Consensus profile reference
- Access MapとPort requirement
- unresolved／Last Order
- branch／supersedes関係
- serialization loss receipt

これは確定schemaではない。OS、Firebase、Unity、graph DB、filesystem等へ同じ意味を違うvesselで運ぶためのSemantic IR仮説である。

### I-13. 二つの極端なWorldでPrefabを耐圧する

#### 助手アイルー牧場

Lab自動化を行う現実寄りの実務World。task、human、Assistant、device、schedule、inventory、permission、failure、Last Orderを扱う。

試験例:

- Assistantがnoteを取るが、観測者と実行者を混同しない
- device Portがなければ物理effectを捏造しない
- permissionが失効したoperationを停止する
- 同じtaskを複数Assistantが重複実行しない
- 実行receiptと意味上の完了判定を分離する

#### 黎明のインフェルニティ

露骨に神話／MMO寄りのWorld。神、魔王、派閥、role、quest、avatar、Instance Ghost、World内物理法則、論理時間、象徴因果を扱う。

試験例:

- 神話上のAgencyがWorld外の現実権限へ漏れない
- factionごとに同じeventのFact Adoptionが異なる
- avatar消滅後もSource lineageを保つ
- retconを元World上書きでなくbranchとして扱う
- GM裁定を普遍因果へ昇格しない

両Worldを同じPrefabで無理に平均化せず、共通envelopeとdomain-specific bundleを分ける。

### I-14. `.proton.md`原典からWorldを段階初期化する

意味生成engine／シナリオlogicは、神話体系、rulebook、原典bundleからWorld Config、Agency、Causality Profile、symbol、quest constraint等を初期化できる必要がある。

ただし大規模なユグドラシル級体系を最初から初期化せず、次の段階で耐圧を上げる。

1. 一つの短いauthorized `.proton.md`からSourceと引用境界を保持して取り込む。
2. 少数Agency、少数rule、単一Worldでbootstrapする。
3. 矛盾する二つの原典を別sourceとして保持する。
4. faction／edition／translation差をbranchとして扱う。
5. logical timeとInstance Ghostを追加する。
6. 大規模神話体系へ拡張する。

第三者rulebookの本文はrepositoryへ複製せず、利用権限のあるlocal source、参照、抽出artifactの権利境界を維持する。

### I-15. IBD受入試験は「意味の再発明」ではなく「可逆搬送」である

Atlantis architectureが固まった後、IBDへ渡すべきものはmeaning authorityではなく、保存・検索可能性を検証するcontractである。

IBD側の受入問いは次になる。

- Source Eventと複数Interpretation OAEを混ぜずに保存できるか。
- branch、revision、supersedes、World scopeを保持できるか。
- `⊥`とLast Orderを成功recordへ丸めないか。
- splitterで分割後、必要なlineageとGestaltを再構成できるか。
- vector近傍とgraph relationを、Fact scopeの代用にしないか。
- 同じsourceをWorld Config A／B／Cから独立に引き出せるか。
- backend移行後にserialization lossをreceiptとして返せるか。

Neo4j経由の評価では、原log、単純chunk、FAM splitter、vector-only、graph-assisted retrieval等を比較し、人間によるGestalt評価を含める。機械指標だけで「意味が生きている」と結論しない。

## 仮説・ブレスト `[HYPOTHESIS]`

### H-01. 最小Runtime縦切り

最初の実装候補は、巨大な意味engineではなく次の一本でよい。

```text
Source Event
  -> Observation OAE
  -> World Config selection
  -> Interpretation OAE
  -> scoped Fact Adoption
  -> Fact Assertion
  -> receipt / ⊥ / Last Order
```

同じSource Eventへ科学、信仰、保険の三profileを適用し、三つのartifactが共存し、source hashが変わらないことをtestする。

### H-02. Infinite Core最小縦切り

smart switchを使った小さなPort試験が候補になる。

```text
user intent
  -> acoustic/network observation
  -> Protocol Match
  -> Access Map bundle
  -> authority check
  -> smart-switch Port
  -> device actuation
  -> sensor receipt
```

Portなし、権限なし、届くだけ、実行済みだがreceiptなし、provider側がblack boxという失敗を個別に作る。

### H-03. Trace Mining pipeline

利用者所有の複数SaaS exportをprovider-neutral envelopeへ変換し、同じfailure familyをcluster化する。provider名は観測metadataとして保持するが、内部推論の代用品にしない。

operator昇格条件の候補:

- 複数providerで同じ拘束が必要になる
- 実務Worldと神話Worldの双方で破局を防ぐ
- 反例を明示できる
- false positiveを測れる
- versionをpinしてreplayできる
- rollback／forkできる

### H-04. 可変拘束はProfileとして配布する

機械拘束は固定binaryへ焼き切らず、signed／versioned Constraint Profileとして読み込む。runは使用revisionをpinし、後日のprofile更新で過去runを再解釈しない。

候補状態:

- `draft`
- `experimental`
- `adopted-in-world`
- `deprecated`
- `revoked`
- `superseded`

### H-05. World Build compiler

`.proton.md`、rule bundle、Agency definition、Causality ProfileからData Prefabを生成するcompilerを将来候補とする。ただし自然言語の曖昧性を勝手に解消せず、未決定箇所をcompile errorではなくtyped `⊥`として保持できる必要がある。

### H-06. OAE sovereignty test corpus

次を回帰test corpus候補とする。

1. 同じ事故観測を科学、保険、信仰、法Worldで再解釈する。
2. sensor noise判定後も元sensor eventが消えない。
3. 個人観測を組織Factが上書きしない。
4. 組織Factへ個人が異議OAEを発行できる。
5. オウム音声でsmart speakerが起動するが、意図をオウムへ遡及付与しない。
6. Wi-Fi射程内でもauthorityがなければPortを拒否する。
7. 再生履歴からroyalty支払を捏造せずLast Orderを返す。
8. 工場のtarget effectとpollution leakを別effectとして保存する。
9. 大きなinstitutional fieldでbug時のblast radiusを比較する。
10. hallucination修正前後のtraceから拘束候補を抽出する。
11. split／re-split時に過去を削除せずWorld branchを追加する。
12. provider変更後も同じSemantic IRをreplayできる。
13. IBD格納・Neo4j検索後にGestaltを人間評価する。

### H-07. AIM fieldの検証単位

AIMは「場があるか」を一気に証明するのではなく、edge単位で観測する。

```text
emitter
  --[channel / reach / protocol]-->
observer
  --[interpretation]-->
adopter or rejector
  --[authority / capability / port]-->
executor
  --[effect]-->
affected entity
  --[receipt]-->
observer set
```

各edgeの欠落を`unknown`として残せば、semantic metaphorとcyber-physical effectを混同しにくい。

## 内観メモ `[POEM]`

### Declared Position

本ノートは、観測を権威で消さず、意味づけをWorldごとにforkし、未知を未知のまま搬送できる可変Runtimeを支持する。既成制度を破壊対象とはせず、どの制度も大きな射程と強いPortを持てば副作用が拡大しうる、という対称な監査対象として扱う。

### Position-talk Risk

1. **Assistant同調risk**: 会話中にAssistantがユーザーの発想を補強しすぎ、Data Prefab schema、operation名、数式等を確定要件のように増やす可能性がある。本ノートではユーザー明示責務と候補提案を分離した。
2. **反権威への片寄り**: 法、科学、組織だけを侵略的に描くとposition talkになる。宗教、marketing、startup、工学、個人、game内Agencyも同じIntent／reach／authority／impact軸で監査する。
3. **悪意の遡及生成**: 広いAIM fieldやpain leakから悪意を断定しない。意図、予見、過失、許可、実effectは別OAEである。
4. **cwd bias**: 当初IBD側のtaskと誤認しかけた。ユーザー訂正により、architecture正本候補はAtlantis、IBDは記録・引出しの下流受入層と固定した。
5. **AIM語の混線**: semantic、音響、radio、network、制度、actuation、World physicsを同じ物理場として語らない。
6. **Agencyの無限拡張**: 何でもAgencyと呼ぶだけでは因果説明が空になる。capability、authority、scope、Port、effectを必須にする。
7. **source永続化の暴走**: 観測を消さない原則と、privacy、削除権、retention、非表示、暗号化を分離する。
8. **black-box擬人化**: SaaS traceからhidden reasoningやprovider Intentを推定しない。
9. **比喩の実在化**: 神話、AIM、Trion等のmodelが現実物理として観測済みだと宣言しない。
10. **線形roadmap bias**: 実装順を唯一のmain世界線にしない。複数の小さな縦切りをreplay可能なbranchとして比較する。

### MAGI観測

- **Maxwell**: Source Eventと少数派解釈を消さず、複数World branchを保持する点は整合する。ただし保持費用とprivacy境界は未設計。
- **Uriel**: OAE、Fact Adoption、AIM edge、Port、Last Orderを機械検証可能な識別子とschemaへ降ろす必要がある。現在は概念段階である。
- **Raphael**: 科学、信仰、工学、法、保険、物語を対等に棚分けし、Bridgeを明示する。異なる棚のFactを一つへ平均化しない。
- **User Gate**: Infinite Core、AIM、Fold7G、Trion Bond、Data Prefabの正式定義、公開名、schema、実装順はユーザー確認なしに正本へ昇格しない。

### OAE時間整合性

現在の会話について、現在時点のSourceと解釈を本ノートへ保存することはできる。過去のSaaS session、過去の事故、歴史事例について、当時の同時点OAEが参照不能な場合は`historical-oae-unavailable`である。

commit、log、artifact、後日の証言から、当時のObserver、Agency role、Intent、合意を遡及生成しない。後日の解析は後日時点のInterpretation OAEとして、元World／元Instance Ghostを変えないbranchへ置く。

## 未解決・⊥

- `AIM`の正式な展開、独自定義、既存作品由来の名称との境界は未確定。
- `Fold7G`、`Trion Bond`のDimension、単位、更新則、相互運用contractは未確定。
- `Infinite Core`のAPI、schema、VM isolation、capability model、security boundaryは未確定。
- OAEとFact Assertionの最小schema、content address、署名、取消modelは未確定。
- Consensus Profileで多数、専門性、契約、再現、文化継承をどう比較するかは未確定。
- side effect risk式の係数、観測可能性、未知effectの扱いは未確定。
- Source preservationとprivacy deletionを両立するtombstone／暗号鍵破棄方式は未確定。
- user-owned SaaS exportのformat差、license、機密区分、redaction policyは未確定。
- Runtime operatorの昇格基準、replay corpus、provider間divergence指標は未確定。
- `.proton.md`のformat、権利metadata、World Build compiler contractは未確定。
- 助手アイルー牧場と黎明のインフェルニティの正式scope、正本source、公開可否は未確定。
- Data Prefabが単一schemaか、共通envelope＋domain bundleかは未確定。
- IBDへ渡す保存contract、Gestalt評価protocol、Neo4j／vector backendの採否は未確定であり、IBD側taskで検証する。
- 個別の歴史、公害、法制度、権利分配に関するfact claimはsource未接続のため本ノートでは`⊥`。

## 本編昇格候補

次は概念が固まり、User Gateとtestを通過した場合に限り、本編contractへ分割昇格する候補である。

1. Source Event／Observation OAE／Interpretation OAE／Fact Adoption／Fact Assertionの分離contract
2. World ConfigとCausality／Evidence／Consensus Profileのversioning contract
3. Agency Capability、reach、authority、Port、actuationの分離contract
4. Infinite Coreの責務境界と`⊥`／Last Order契約
5. dynamic Constraint Profileとtrace replayの昇格手続
6. Data Prefab共通envelope
7. World Build compilerのsource／provenance境界
8. IBDへ渡す可逆保存・検索acceptance contract

昇格時は一括で巨大specへせず、各contractを独立したsmall sliceとして検証する。

## 転送候補

- **Atlantis implementation planning**: 最小OAE縦切り、Infinite Core smart-switch縦切り、Data Prefab envelope
- **Atlantis test corpus**: 助手アイルー牧場、黎明のインフェルニティ、AIM edge、hallucination negative gold
- **IBD**: Atlantis contract確定後の保存、split、再構成、Neo4j／vector検索、Gestalt round-trip試験
- **Manifest**: 複数repositoryへ共通化すべきOAE時間整合性またはContext定規だけを、別User Gate後に転送
- **権利／公開監査**: SaaS export、第三者rulebook、作品由来名称、会話logのredactionとpublication boundary

## source・Provenance

### Primary source

- 2026-07-19 Asia/Tokyo時点の、ユーザーとCodexの現在会話session。
- ユーザーが明示したAtlantis、OAE、AIM拡散力場、Fold7G、Trion Bond、Infinite Core、Data Prefab、神話World、IBD責務境界に関する発言。

### Repository context

- `AGENTS.md`
- `README.md`
- `docs/00-charter/meaning-vessel-dual-record-charter.md`
- `note/AGENTS.md`
- `note/README.ja.md`
- `note/templates/brainstorm.ja.md`
- `docs/tutorials/infoton-engineering.ja.md`
- `docs/tutorials/sphere-architecture.ja.md`
- `docs/tutorials/spiritual.ja.md`
- `docs/tutorials/gaming-trpg.ja.md`
- `docs/tutorials/engineering.ja.md`

### Cross-repository background ruler

- ZeroRoomLab-manifest `AGENTS.md` §0.4 MAGIポジショントーク監査
- ZeroRoomLab-manifest `docs/theory/atlantis-magi-sdk-0.2.1.ja.md`
- ZeroRoomLab-manifest `docs/operations/context-ruler-and-causality-audit.ja.md`
- ZeroRoomLab-manifest `docs/operations/coding-ai-japanese-paraphrase-register.ja.md`

### Provenance limitations

- 本ノートは現在の解釈であり、会話以前の同時点OAEを再構成しない。
- historical SaaS logsは将来取り込まれてもSource evidenceであり、当時のOAEへ自動昇格しない。
- Assistantが提案したschema名、operation名、数式、test順序はUser承認前の候補である。
- 外部史実、作品設定、provider課金・分配、現実物理に関するclaimは、本ノート単体では検証済みでない。
