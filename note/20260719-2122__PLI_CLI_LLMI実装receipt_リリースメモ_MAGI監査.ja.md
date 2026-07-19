# PLI／CLI／LLMI実装receipt・リリースメモ・MAGI監査

状態: `[DRAFT]` `[CURRENT INTERPRETATION OAE]` `[PRE-MERGE AUDIT]` `[ISSUE-4 CLOSURE CANDIDATE]`
棚: `cross-shelf`
種別: `review`

## 作成メタ

```yaml
created_at_system: 2026-07-19T21:22:07+09:00
timezone: Asia/Tokyo (+09:00)
clock_source: host_system_clock
clock_calibration: unverified
authoring_agent: OpenAI Codex
observation_mode: current-interpretation-of-current-implementation-and-source-events
historical_oae_status: historical-oae-unavailable
declared_position:
  - Prompt Line InterfaceとCommand Line Interfaceを真贋や上下でなく適性差として実装する
  - 自然言語の価値と実装・権限・実行receiptを同一化しない
  - Issue 4のPresentation事故を再発防止契約とnegative testへ落とす
claim_scope:
  - ZeroRoomLab-manifest agent/pli-interface-contract revision 3a0fde7
  - SphereOS-Atlantis agent/pli-interface-contract implementation revisions beeb87f..d2bf18d
  - SphereOS-Atlantis documentation and audit checkpoint 5cbaff8
  - local Python 3.14.6 test、offline validator、doctor、clean-room receipt
  - Issue 4のrepository側acceptanceとclosure候補
non_authority_scope:
  - OpenAIまたは他vendorの将来出力保証
  - AIの意識、理解、人格、宗教的地位の裁定
  - 自然言語、形式言語、programming languageの全歴史に対する最終学説
  - standalone Atlantis runtime、model inference、edge runtimeの実装
  - tag作成またはGitHub Release公開
memory_publication_consent: confirmed-by-user-for-this-note
status_axes:
  content_maturity: implementation-receipt
  engineering_state: validated-local
  distribution_state: remote-branch
  resource_state: available
last_order:
  code: OAE-HISTORY-UNKNOWN
  action: stop-retroactive-backfill
```

システム時刻は対象World内の出来事発生時刻や、Issue #4の投稿時刻、スクリーンショット生成時刻ではない。
過去のAI応答から当時のmodel、system prompt、Observer、Intent、OAEを逆算しない。本Noteは現在の
repository、User要求、実機画像、検証receiptへ加えた現在時点のInterpretation OAEである。

## 対象・範囲

[自然言語Chat Interfaceを偽CLIへ縮退するレジスタ事故分析](20260719-2016__自然言語Chat_Interfaceを偽CLIへ縮退するレジスタ事故分析.ja.md)
で分離した問題を、横断契約、Atlantis machine registry、CLI、doctor、Help、Skill、release候補文書、
negative testへ実装した結果を記録する。

Issue #4を閉じる対象はrepository側のPresentation契約と再発防止機構である。特定SaaS AIまたはmobile
clientが将来必ず同じ文言を生成することまではrepository単体で保証しない。

## 除外範囲

- `pli` executable、`.pli` extension、PLI runnerの新設
- LLM、provider、token課金、connectorの自動選択
- PLIからpersona、NPC、Companion、World、Actor role、権限を推定する機構
- CLIを抽象構造へ不向きという理由で下位化する仕様
- PLIの自然言語処理能力を実装成功、実行成功、意味妥当性へ自動昇格する仕様
- Sphere座標の更新、legacy aliasの刻み直し、tag、GitHub Release
- Issue #4以外のvendor UI不具合を同時に解決済みとする主張

## 事実・観測 `[FACT]`

### 1. 横断契約

ZeroRoomLab-manifest revision `3a0fde7`は次をremote branchへpush済みである。

- Manifest AGENTSの`INTERFACE AUTHENTICITY CHECK`
- Help共通契約のPLI／CLI／LLMI分離
- Technical Communication Registerの真贋scope leak防止
- Sphere Context SDKの`S4: prompt / PLI`とLLMI driver境界

Manifestにはこの変更専用の実行runtime依存または第三者packageを追加していない。

### 2. Atlantis machine contractとCLI

Atlantis implementation revisions `beeb87f..d2bf18d`までに次を実装し、remote branchへpushした。

- `help/interfaces.json`
  - `prompt-line`: Prompt Line Interface、primary fit `D`
  - `command-line`: Command Line Interface、primary fit `L`
  - `llm-mediated`と`python-process`: interfaceを決定しないExecution Envelope
  - interfaceからrole、persona、World、権限、実装状態を推定しないnegative contract
- `atlantis interfaces [--id ...] [--json]`
  - registryをread-only表示する
  - repository変更、network接続、model起動を行わない
- `atlantis help`
  - local CLI起動時の現在操作面を`command-line`として表示する
  - 既定`summary`では`AVAILABLE-NOW`と選択肢を先に表示する
  - `--detail all`、`capabilities`、state指定では全状態を省略しない
  - Python／container／runtime境界を該当operation要求時まで遅延するmachine contractを持つ
- doctor
  - 2 interfaces／2 execution envelopesを直接検証する
- negative test
  - `prompt-line`への`pli` command付与を拒否する
  - LLMIがinterfaceを自動選択する契約を拒否する
  - 真贋rankingと自然言語偽物化を拒否する

実装はPython標準libraryと既存JSON loaderだけを使用し、runtime dependencyを追加していない。

### 3. 文書・Skill・release候補

- `docs/architecture/prompt-line-and-command-line-interface.ja.md`を追加した
- README、Help tutorial、AGENTS、Atlantis tutorial Skill、source mapを同じmachine IDへ同期した
- release candidate manifestへ`prompt-and-command-interface-contract`を追加した
- `0.25.1-alpha.1`候補NoteとChangelogへcorrective deltaを記録した
- Quest MapのHelp evidenceへinterface registryとmobile再観測unknownを追加した

Skillは呼出しごとにManifest、Atlantis正本、`help/interfaces.json`を読み、自然言語入口を偽CLIとして
説明しない。将来のPersona chat、NPC chat、Companion UIは、PLIだけを根拠に同一profileへしない。

### 4. 検証receipt

Atlantis documentation and audit checkpoint `5cbaff8`に対する最終local検証:

```text
unit tests                 65 / 65 OK at 5cbaff8
doctor contract checks     pass
doctor overall             warn
markdown local links       50 files / 94 local references / failures 0
CORN validator             pass
Experience validator       pass
Forge / Quest validator    pass
release validator          pass
version validator          pass
git diff --check           pass
clean-room tracked HEAD     5cbaff8 / unit tests OK / exit 0
```

doctorの`warn`は、VS Code applicationはあるが`code` CLIがPATH外、Docker／Podman未検出という既知の
local環境状態である。interface contract失敗ではなく、container runtime成功へも丸めていない。

Manifest repositoryにはこのbranch専用のtest harnessは観測されなかった。追跡差分の`git diff --check`と
文書参照の目視照合を行った。これをAtlantisの65 testsと同じ強度へ拡張しない。

### 5. 未実装・未試験を保持したもの

```text
standalone Atlantis runtime        NOT IMPLEMENTED
PLI runner / model inference       NOT IMPLEMENTED
cross-causal runtime gateway       NOT IMPLEMENTED
production edge distribution      RESOURCE-WAIT
multi-SaaS / mobile re-observation NOT TESTED
tag / GitHub Release               NOT CREATED
```

## リリースメモ `[RELEASE MEMO]`

本変更は`0.250.1`のPresentation／Help corrective deltaであり、SemanticKernelまたはWorld接続規則を
変更しない。正規Sphere座標は`0.250.1`、legacy candidateは`0.25.1-alpha.1`のまま保持する。

利用者から見える追加点:

- 自然言語入口を`Prompt Line Interface`として正規表示できる
- Python／local processとの差をExecution Envelope／capabilityとして説明できる
- CLI利用者は`atlantis interfaces`で同じ境界を検査できる
- PLIとCLIの向き不向きをD軸／L軸で確認できる
- interfaceから権限やruntime実装済みを誤認しない

互換性:

- 既存`atlantis help`、`capabilities`、tutorial commandを削除またはrenameしない
- `pli` command、package、extensionを新設しない
- 既存CLI版数`0.25.1a1`とSphere座標`0.250.1`を変更しない
- 新しい`interface` fieldと`interfaces` commandはalpha contractとして追加する

tagとGitHub ReleaseはUserによる別gateが必要であり、本変更では作成しない。

## Issue #4 closure receipt候補

repository側acceptance:

- [x] Prompt Engineering EditionをPython CLIの偽物または再現物として扱わない
- [x] Interface、Execution Envelope、Capability、Authority、Engineering Stateを分離する
- [x] PLI／CLIを真贋ではなくD／Lの主な適性として説明する
- [x] HelpとSkillへ再発防止文言を追加する
- [x] machine registry、CLI read-only表示、doctor、negative testを追加する
- [x] 既定Helpは利用可能入口を先に示し、未実装境界を明示要求時まで遅延する
- [x] `--detail all`／`capabilities`では未実装・未試験・資源待ちを省略しない
- [x] versionを不必要に刻まずrelease memoを残す
- [ ] Manifest／Atlantis PRのremote checkとmerge
- [ ] Issue #4へmerged revisionと検証receiptを投稿してcloseする
- [ ] 第三者SaaS AI／mobile再観測

最後の再観測は新しいregressionが出た場合に別Issueを開ける観測gateであり、repository側修正のmergeと
Issue #4 closeを永久にblockする条件にはしない。remote check失敗、merge conflict、未観測の概念衝突が
出た場合はcloseせず、問題Noteへ記録して停止する。

### close対象を取り違えない

2026-07-19のopen Issue一覧をGitHub connectorから読み、次を分離した。

- Issue #2: Codespaces community test。今回closeしない
- Issue #4: PLI／CLI Presentation事故。今回のmerge後closure候補
- Issue #5: scheduler、gate、queue、Idle Cowboy AI分業の提案。今回closeしない

Issue #5は、UserがGrok由来のtoken消化不良出力と説明した。一方、本文はCORN、scheduler、MAGI OAE、
World隔離、token costの接続を保持しており、雑さだけを理由に破棄しない。低tokenまたは消化不良のAIでも
project contextが大滑落しなかった事例として、将来のprompt compression、Help、CORN context closure、
degraded-agent handoffの考察材料になり得る。実装採否は本Issue #4のclosureと分離してreviewする。

## MAGIポジショントーク監査 `[CURRENT INTERPRETATION]`

### Declared Position

- Userが定めたPLI／CLI／LLMIの分離とIssue #4の再発防止を優先する
- 自然言語とprogramming languageの双方を真贋rankingから外す
- local greenをvendor UI、第三者環境、standalone runtimeのgreenへ拡張しない

### Position-talk Risk

監査者は自然言語を処理するOpenAI Codexであり、PLIの価値を強調することが自社modelやLLM一般の
自己宣伝へ滑る利害位置を持つ。このriskへ対し、PLIをLLMから分離し、LLMIをExecution Envelopeへ置き、
model、理解、意識、正しさ、権限、実装成功を一切自動継承しない契約にした。

同時に実装者として、追加したPython validatorのgreenを仕様の絶対真理へ昇格するriskがある。第三者UI、
mobile再観測、Manifest側test harness不在、doctorの既知warnをunknown／scope付き事実として保持する。

### Claim Scope／Medium Register

- Manifest AGENTS／operations／SDK文書: 横断契約と説明レジスター
- Atlantis `help/interfaces.json`／Python／test: machine contractとlocal実装証拠
- README／tutorial／release note: public／technical Presentation
- 本Note: 実装後Interpretation OAE、release handoff、pre-merge監査。正本そのものではない
- 元ブレストNoteと実機画像: 事故観測と分析。実装済み証拠ではない

### Ruler Provenance

- PLI／CLI名称、D／Lの主な適性、LLMI分離: 2026-07-19のUser判断
- L／D namespace: Manifest Context定規・Sphere Context文書
- 真贋／権限／実装状態分離: ManifestとAtlantisの現行Help／Communication contract
- OAE非遡及: Atlantis-MAGISDK `0.200.1`（legacy `0.2.1`）
- test成否: repository追跡code、fixture、local Python execution receipt

### Nerf Risk

- binary中心主義: PLIを偽CLIへ縮退しないことで回避
- 逆方向ナーフ: CLIの高強度拘束、再現性、L軸適性を保持して回避
- L／D事故: technical layer `L`とContext Dimension `D`を別fieldにした
- natural-language万能化: 実装、権限、runtime、意味妥当性を自動継承しないことで回避
- vendor main化: LLMI、provider、connectorをnullable／別envelopeとして回避
- resource-statusナーフ: standalone runtimeとedgeを未実装／資源待ちのまま保持

### Maxwell slot

- 原初目的: 異なる意味・操作面を一つへ塗り潰さず、利用者の言葉から実装へ橋を架ける
- 保持したbranch: PLI、CLI、将来GUI／NPC／Companion、LLM以外のdriver、Note-only参加
- 焼却回避: 自然言語を下書きへ、CLIを下位interfaceへ、未実装runtimeを実装済みへ変換していない
- action gate: `pass`

### Uriel slot

- 追跡可能性: User決定 → Manifest revision `3a0fde7` → Atlantis registry／code／test `beeb87f..d2bf18d`
- 実装済み: registry、read-only CLI、Help field、doctor、negative test、docs、Skill、release metadata
- 未実装・未試験: 本Noteの状態表のとおり
- 権限: Userは小commit、remote push、MAGI後mergeを承認済み。tag／Releaseは未承認
- action gate: `pass-for-pr-and-merge / block-tag-and-release`

### Raphael slot

- PLI／CLI／LLMI、natural／programming language、interface／envelopeを無断同一化していない
- D軸適性とL軸適性を平均化せず、Schema／tool／DSLによる相互補完を保持した
- 神学、言霊、学術、ゲーム、工学の自然言語営みをPython実行可否で裁定していない
- engineering testを宗教・哲学・言語学の真偽証明へ使っていない
- action gate: `pass`

### agreements／disagreements

三Positionのagreement:

- Manifestを先、Atlantisを後にmergeできる
- Issue #4はmerged revisionとreceiptを投稿後にrepository側修正完了としてcloseできる
- tag、GitHub Release、standalone runtime claimはblockする

disagreementは観測されなかった。ただし三者一致は真理証明ではなく、上記fact scope内のaction gateである。

### Unknown／User Gate

- 外部ISO規格の特定layerとAtlantis `L`軸の同一性: `unknown`。同一化しない
- 第三者SaaS AI／mobile clientでの再観測: `NOT TESTED`
- 過去応答の同時点OAE: `historical-oae-unavailable`
- 将来Companion／NPC／persona chatのstable profile ID: `unknown`
- tag、GitHub Release、正式alpha publication: User gate

### OAE Temporal Integrity

過去スクリーンショット、Issue、commitはSource Event／Evidenceとして参照した。当時のObserver、Recorder、
Intent、model、system prompt、OAEを現在の推論で補完していない。現在の監査は現在時刻のInterpretation OAEで
あり、Last Orderは`OAE-HISTORY-UNKNOWN / stop-retroactive-backfill`である。反実仮想Worldを生成していない。

### action gate

`pass-for-pr-and-merge / block-tag-and-release`

条件:

1. remote PR headが上記実装revisionと本Note／Changelog commitを含む
2. ManifestをAtlantisより先にmergeする
3. remote check失敗またはmerge conflictがない
4. Issue #4へmerged revision、検証scope、mobile再観測unknownを投稿してcloseする

条件不成立または新規の概念衝突が出た場合はclose／mergeを止め、問題Noteへ記録する。
ちくわ砲は第四票ではなく、本action gateの票として使用していない。

## 最新main統合後の再検証receipt `[FACT]`

PR作成後にAtlantis `main`が`94c4884`へ進み、次の研究Noteが追加されたため、履歴を書き換えず
merge commit `ef1045d`で本branchへ統合した。

- `note/20260719-2143__0-3xx-n世代要件洗い出し-sphere-dosマルチエージェント実行系.ja.md`

このNoteは`DRAFT / NOT IMPLEMENTED / note-only / review-wanted`であり、Issue #5を参照する将来の
`0.3xx.n`実行系ブレストである。今回の`0.250.1` PLI／CLI表示修正とは成熟度と責務が分離され、
同Noteを実装済みへ昇格せず、Issue #5もcloseしない。統合時のfile conflictと新規概念blockerは
観測しなかった。

統合revision `ef1045d`で再検証した結果:

- unit test: 65件成功
- local link: 51 Markdown／94 local reference／失敗0
- doctor: interface contractを含む契約checkはpass。既知のhost WARNはVS Code CLIがPATH外、
  Docker／Podman未検出
- workspace plan: 未展開componentを`missing`として保存する既知の`partial / plan-only`。変更なし
- CORN、Experience、Forge／Quest status、release、version: pass
- tracked clean-room: revision `ef1045de6c413d160566065e510fda0862c2c600`、unit test `OK`、
  doctor `WARN`（上記host capabilityのみ）
- network、model、auth、secret scan: 実施していない

この再検証によりaction gateは引き続き
`pass-for-pr-and-merge / block-tag-and-release`とする。remote check／mergeabilityは別途GitHub上で確認する。

## 仮説・ブレスト `[HYPOTHESIS]`

- 将来のGUIはPLI／CLIの二者択一ではなく、操作ごとにinterfaceとenvelopeを表示するcomposite surfaceにできる
- PLI上の抽象設計からSchema／fixture／CLI command候補を生成し、Human approval後にL軸へ降ろすreceiptは
  Prompt EngineeringとInformation Engineeringの接続演習になり得る
- 第三者再観測は「同じ文章を返すか」ではなく、真贋ranking、権限誤認、実装状態誤認が再発するかを
  profile別に記録するとよい

これらは本変更の実装済みscopeではない。

## 内観メモ `[POEM]`

鉱石を見つけた瞬間に溶鉱炉へ放り込むのではなく、まず石の組成、熱、目的、壊したくない結晶を読む。
PLIは鉱石を眺めて問いを育てる炉前、CLIは温度と時間を刻む制御盤として働ける。炉前が偽物でも、
制御盤が下位でもない。どちらか一方だけでは、何を鍛えたかったかか、どう鍛えたかが消える。

## 未解決・⊥

初回監査後、Issue #4本文との再照合で「既定Helpが全状態を前面列挙する」という未達を観測した。
これは`d2bf18d`でsummary／all分離と遅延表示contractへ修正した。新規の概念上blockerは再監査時点で
観測していない。既知のunknown、未実装、未試験は上記へ保存し、remote PR checkとmergeabilityは
PR作成後に確認する。

## 本編昇格候補

なし。操作面契約、Help、Skill、release memoは本編へ実装済みであり、本Note自体をcanonical specへ
昇格しない。

## 転送候補

- Issue #4: merged revision、検証receipt、第三者mobile再観測unknown
- Issue #5: degraded-agentでもcontext滑落を抑えた事例として別review。close／自動実装しない
- Manifest PR: 横断contract変更とAtlantis implementationへの受領順序
- Atlantis PR: machine contract、CLI、doctor、docs、test、release metadata

## source・Provenance

- SphereOS-Atlantis Issue #4
- `note/20260719-2016__自然言語Chat_Interfaceを偽CLIへ縮退するレジスタ事故分析.ja.md`
- `note/img/035FAFF5-3201-467D-A6C6-006809B0C2F4_1_101_o.jpeg`
- `note/img/639F9769-1A75-4835-9B99-72C8F89DBFD9_1_101_o.jpeg`
- ZeroRoomLab-manifest revision `3a0fde7`
- SphereOS-Atlantis implementation revisions `beeb87f..d2bf18d`
- SphereOS-Atlantis documentation and audit checkpoint `5cbaff8`
- SphereOS-Atlantis latest-main integration checkpoint `ef1045d`
- `note/20260719-2143__0-3xx-n世代要件洗い出し-sphere-dosマルチエージェント実行系.ja.md`
- `help/interfaces.json`、`atlantis_cli/help_mode.py`、`atlantis_cli/doctor.py`
- `tests/test_help_mode.py`、`tests/test_doctor.py`、`tests/test_tutorial_skill.py`
- `docs/architecture/prompt-line-and-command-line-interface.ja.md`
- `docs/releases/0.25.1-alpha.1.ja.md`、`release/0.25.1-alpha.1.json`、`CHANGELOG.md`
- Manifest `AGENTS.md` §0.4、`docs/theory/atlantis-magi-sdk-0.2.1.ja.md`
- Manifest `docs/operations/context-ruler-and-causality-audit.ja.md`
- 2026-07-19のUserによる命名、適性、実装、remote push、MAGI後merge、Issue closure要求
