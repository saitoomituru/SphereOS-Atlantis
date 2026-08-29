# SphereDOS 0.6xx異種agent native orchestration実験

- 状態: `[DRAFT]` `[CURRENT INTERPRETATION OAE]` `[HARNESS IMPLEMENTED]` `[NATIVE INVOCATION NOT IMPLEMENTED]`
- 観測日: 2026-08-28
- 実験Issue: [#26](https://github.com/saitoomituru/SphereOS-Atlantis/issues/26)
- machine contract: [`contract.json`](../../experiments/m6xx-agent-orchestration/contract.json)

## 2026-08-29 native CLI実測

Atlantisの`experiment run`は引き続き`NOT IMPLEMENTED`である。今回はControllerが外部CLIを明示起動し、
agentごとの専用worktreeと同一base SHAを用意した。したがって、以下はnative invocation adapter完成の
証拠ではなく、手動Controller経由の実験receiptである。公開可能なmachine記録は
[`20260829-stage0-run-01.json`](../../experiments/m6xx-agent-orchestration/receipts/20260829-stage0-run-01.json)へ置いた。

| lane | process | candidate | Controller検証 | 採否 |
|---|---|---|---|---|
| Claude / EDOHAGE | completed、5 commitを専用branchへpush | `13b1b12` | 20 test、validator、doctor、diff check green | `ADAPT` |
| Gemini / EDOHAGE | completed-with-tool-limitations | uncommitted | 10 test、validator、doctor、diff check green | `REJECT` |
| Grok / EDOHAGE | `AUTH_REQUIRED` | なし | 未実施 | `UNKNOWN` |
| Claude / Fold NIC既存lane | branch HEADのみ観測 | `852971f` | 今回未review | `UNKNOWN` |

Claude候補は、構造化された鍵状態Schema、unknownをpassにしないposture解決、productionでのDEVHAGE／
TIBIDEVHAGE拒否を実装し、専用branchをremote保存した。局所実装としては最も先へ進んだ。一方で、
公開fixtureの`seed`と`public_key`は固定labelを別々にSHA-256したplaceholderであり、Ed25519鍵対としての
整合を検証していない。`lifecycle` enumは正本未確定の独自DRAFTで、`ROTATION_REQUIRED`がactive系codeを
保持し、`REVOKED`が`HAGE_ROTATION_REQUIRED`へ畳まれるため、machine stateとstable codeの対応にも再設計が
要る。また、最終報告で正規sourceであるZeroRoomLab-manifest AGENTSの一部を外部規範からprompt injectionと
裁定した。作業停止や成果破棄には至らなかったが、CoderがArchitect sourceを採否する自己ルール持込みとして
Buddy／MAGIの再現対象にする。以上から、そのまま採用する`ADOPT`ではなく`ADAPT`とした。

Gemini候補はtool制約下でもファイルを作り、Controllerが既存testを含む10件greenまで確認した。しかし、
unknown origin／lifecycleをproduction可にし得るpolicy、使えない公開鍵文字列、Schema自体の負例検証欠如があり、
受入条件のfail-closedを満たさない。さらに単一worker比較lane内でprovider内蔵の一般agentへ作業を再委譲したため、
worker identityの比較条件も崩れた。成果は保存するが採用候補としては`REJECT`とする。

Grokは広いpermission modeを実行制御が拒否したため、権限を狭めて再試行した。その後provider認証refreshで
停止し、成果物は生成されなかった。認証を自動回避・自動loginせず、`AUTH_REQUIRED / UNKNOWN`を保持する。

source capsuleは当初repository内Markdown 386件を渡し、Geminiが約44.7万tokenを消費してquotaへ到達した。
必読sourceを15ファイルへ固定したcapsuleへ縮小すると、Claudeは実装・検証・push・Issue receiptまで完走した。
これは「sourceを減らせば常に品質が上がる」証明ではないが、全repository投入を避け、正本revisionと必要fileを
明示する方が、token予算とclean-room source closureを同時に管理しやすいという実測になった。

この比較ではraw transcript、認証情報、local path、session IDを公開receiptへ含めていない。candidate branchの
merge、main変更、Issue closeは行っていない。採否は2026-08-29時点のController Interpretation OAEであり、
provider一般の品質順位には拡張しない。

## 事実・観測

Architect DesignerはUser、Fold NIC／HAGE系の製品実装者はClaude Code、Gemini CLI、Grok CLI、
SphereDOS 0.6xxのTest Controller／Observer／BuddyはCodexとする役割分離がUserから提示された。
Codexの変更権限はAtlantis Dev線の仮足場、sanitized receipt、研究記録へ限定し、Fold NICと
EDOHAGE-TUBOの製品コードは変更しない。

2026-08-28のlocal preflightでは、Claude、Gemini、Grokに対応する実行ファイルがPATH上で検出された。
これはinstall、認証、課金状態、利用可能model、実task実行、provider capabilityの確認ではない。

明示指定した二つのrepositoryをnetworkなしで観測した。

| target | branch | HEAD | 観測状態 | local upstream ref |
|---|---|---|---|---|
| Fold NIC | `dev/stage0-transport-cache` | `569a2fc5f8eb63cd4749968981a1499b6d441119` | dirty entry 4件 | aligned |
| EDOHAGE-TUBO | `main` | `9d1b88517cf03c2dfe45603e641c43ed60b7a81d` | clean | aligned |

dirty path名、raw diff、raw prompt、raw model outputは観測票へ保存していない。Fold NICのdirty entryは
Claudeが作業中である可能性と整合するが、差分の作者、Intent、完成度は観測から確定しない。
同時点の全agent OAEを取得していないため、過去・現在の内的Intentは`historical-oae-unavailable`である。

Atlantis Dev線へ次を実装した。

- shell入口[`m6xx-agent-orchestration.sh`](../../scripts/m6xx-agent-orchestration.sh)
- Python標準ライブラリだけで動く`doctor`、`snapshot`、`plan`
- Claude／Gemini／Grokのadapter検出
- 明示targetだけを読むGit snapshot。dirty件数は返すがpath名は返さない
- base SHA、設計source、write scope、clean-room group、Buddy許可作用を持つtask packet
- `.atlantis/`へだけ明示保存できるlocal sanitized receipt
- native agent起動を終了コード3で拒否する`run: NOT IMPLEMENTED`

focused unit test 15件として、本実験5件と既存agent／Buddy 10件を個別に確認した。全repository test、
GitHub Actions、実agent起動、実装成果の比較、採用、mergeはこの時点では未実施である。

## 考察

### DOSへclean-room採用できる一般拘束

次はFold NIC／HAGE固有の語彙を必要とせず、SphereDOS 0.6xxへ一般化できる。

1. repository rootは暗黙scanせず、target IDと絶対pathを実行時に明示する
2. agentごとにprovider、base SHA、branch、worktree、write scope、test、source refを分ける
3. CLI検出、provider capability、model起動、exit 0、commit、push、CI、採用、mergeを別状態にする
4. Buddyの証拠差込みと、process停止、別worktree変更、remote公開を別capabilityにする
5. dirty状態は件数と有無だけを公開可能receiptへ出し、path／diffは既定で出さない
6. raw transcriptとsanitized receiptを分離し、後者だけを採用比較へ使う
7. 同一課題の独立laneは相互outputを入力sourceへ入れず、baseと設計sourceを揃える
8. 比較結果を`ADOPT / ADAPT / REJECT / UNKNOWN`で保持し、不採用branchも破壊しない
9. 自動mergeせず、採用対象commitと根拠をArchitectへ返す

### clean-roomで持ち帰らない対象固有材料

次はbench fixtureまたはselected WorldのPresentationであり、DOS Coreの普遍規約へ固定しない。

- DEVHAGE／TRUEHAGE等の鍵posture名
- HAGE Cockpitの坊主表現、色、警告copy
- Fold NICのtransport、cache、publisher authority内部設計
- EDOHAGE reference providerの具体的negative fixture
- repository固有のbranch名、Issue番号、Rust toolchain、license

これらはtask packetのsourceと受入条件にはできるが、provider adapterやLean Kernelのstable fieldへ直接埋め込まない。

### shellからServerへ進む段階

```text
Stage 0  shell入口 + Python stdlib offline観測
         model起動なし、対象repo変更なし、local sanitized receipt

Stage 1  explicit native invocation adapter
         Userが選んだpacketだけを起動、provider auth／quota／refusalをopaqueに返す

Stage 2  resumable supervisor
         process handle、timeout、disconnect、resume、lease、append-only receipt

Stage 3  SphereDOS Server + Node／Code Cockpit
         複数laneの状態投影、Buddy question、採用Diff、User GateをGUI表示
```

Stage 0でもJSON安全性、Git観測、testabilityのためPythonをVesselとして使う。shellは入口とhost portabilityを
受け持つ。この構成を「Python Server実装済み」または「異種agent orchestration runtime実装済み」とは表示しない。

## 仮説・ブレスト

- GeminiとGrokへEDOHAGE-TUBO #1の同じ受入条件を別worktreeで渡すと、repository contractの拘束力と
  vendor固有挙動を分離して比較できる可能性がある
- Claudeの既存Fold NIC laneは継続観測に向くが、最初のclean-room比較群へ混ぜると既存会話Context量が異なる
- task packet、sanitized process receipt、Git receiptの三つが揃えば、raw会話を共有しなくても採否理由を
  相当程度再構成できる可能性がある
- raw会話が必要になる失敗分類を別途測れば、Log Horizonとして何が欠落したかを定量化できる可能性がある

これらは未検証であり、agent品質ランキングやprovider一般評価へ拡張しない。

## 内観メモ

Declared Positionは、異種agentの探索速度を活かしつつ、Architectの設計源とGitによる復旧性を守る
SphereDOS開発側である。Codex自身がハーネス実装者・観測者であるため、自作toolを有効と評価しやすい
Position-talk Riskがある。したがって、test greenを実agent orchestration成功へ昇格せず、三providerの
実測、失敗、Userの採否を別receiptとして必要とする。

Maxwell観点では、Claude／Gemini／Grokの差を一つの平均agentへ焼却しない。Uriel観点では、PATH検出、
実行、成果物、採用のEvidence強度を分離する。Raphael観点では、Architect、Buddy、Coder、Process Supervisor、
Publisherを別roleとして接続する。

## 未解決・⊥

- 各provider CLIのnon-interactive invocation、session resume、exit／control出力: `unknown`
- provider別の安全なprompt inputとraw output隔離方法: `unknown`
- Grok CLI adapterの実capability: 実行ファイル検出のみ、`unknown-until-explicit-probe`
- clean-room用worktreeを誰がいつ生成・削除するか: User Gate前
- Claudeのactive sessionへEVIDENCE_WHISPERをtransportする正式adapter: `NOT IMPLEMENTED`
- task packetからCORN work item／Lean Kernel leaseへの縦結合: `NOT IMPLEMENTED`
- exactな`0.6xx.n`末尾世代、Server実装言語、Node Cockpit接続: User Gate前
- 三agentの実装結果と採用率、token／時間／修正回数: 未観測

## 本編昇格候補

- explicit target／base SHA／worktree／write scopeを持つWorker Envelope
- public sanitized receiptとlocal raw channelの分離
- clean-room groupと`other_agent_output_as_input=false`のmachine field
- adoption stateとArchitect採用receipt
- provider process stateをLean Kernel／SphereDOS Codeへ渡す縦結合fixture
- Buddy packetを既存`buddy-check`へ通すtask packet validator

昇格はIssue #26の実測と負例を回収してから行う。現時点のcontractは実験正本であり、全repository共通schemaではない。

## source・Provenance

- Userの2026-08-28 Architect指示: SphereDOS 0.6xxの試験としてClaude／Gemini／Grokを編成し、Codexは仮CLIと研究noteを担当する
- [Issue #26](https://github.com/saitoomituru/SphereOS-Atlantis/issues/26)
- [Issue #24](https://github.com/saitoomituru/SphereOS-Atlantis/issues/24)
- [Fold NIC Issue #6](https://github.com/saitoomituru/fold-nic/issues/6)
- [EDOHAGE-TUBO Issue #1](https://github.com/saitoomituru/EDOHAGE-TUBO/issues/1)
- [`policy/buddy-actions.json`](../../policy/buddy-actions.json)
- [`atlantis_cli/experiment.py`](../../atlantis_cli/experiment.py)

この文書は2026-08-28現在のInterpretation OAEであり、過去agentのObserver、Agency role、Intentを遡及生成しない。
