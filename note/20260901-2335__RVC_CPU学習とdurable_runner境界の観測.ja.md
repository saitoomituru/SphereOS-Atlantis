# RVC CPU学習とdurable Runner境界の観測

実施日: 2026-09-01
clock_calibration: unverified
source: `saitoomituru/Retrieval-based-Voice-Conversion-WebUI@9b9e1e5`
related: Atlantis #6, #9, #20, #29 / Manifest #4, #13, #19, #25
state: `[DRAFT NOTE]` `[OBSERVED EXTERNAL EXPERIMENT]`

## 目的

外部RVC repositoryで行ったデルタもん歌唱modelのCPU学習を、AtlantisのRunner／Provider／
receipt設計へ接続できる観測材料として残す。Atlantis standalone runtime、AI model、voice
asset、DAW統合が実装済みになったという意味ではない。

## [FACT] 実験の経路

1. AirDrive上の公式学習音声65 filesをsymlinkで参照。
2. RVC 40k/F0/v2の前処理233 clips、RMVPE F0 233/233、HuBERT 768-dim 233/233を段階実行。
3. Terminal本体のAppKit `EXC_BAD_ACCESS/SIGSEGV`を検出。Python学習器のcrashとは分離。
4. script直接起動のimport collision、CPU DDP TCPStore bind、CPU DataLoader shm manager失敗を個別に記録。
5. module entrypoint、CPU single-process、DataLoader worker 0へ切り替え、epoch 1・2へ到達。
6. 各段階のstdout、train.log、experiment note、Git commitを保存。voice modelと音声は保存対象外。

## [INTERPRETATION] #9 Archangel Runnerへの接続

今回、Terminalが落ちても「task全体が終了した」とは限らず、逆にPythonがexit 0でも全入力が
有効とは限らなかった。Runner Coreで最低限次を別stateとして保持する必要がある。

```text
host_crashed != child_failed != stage_failed != task_failed
stage_success != model_quality != publication_ready
```

taskには`task_id`、`stage`、`host_ref`、`pid`、`started_at`、`exit_code`、`artifact_refs`、
`resume_from`、`unknown`を付け、foreground／background／managed hostの差を隠さない。
これは#9のdurable orchestration仮説への観測feedbackであり、Runner実装済みの証明ではない。

## [INTERPRETATION] #6 Provider / firepower state

「火力が下がった」はprovider failureへ直結させず、`detected`、`registered`、`approved`、
`dispatchable`、`resource-wait`を分離する材料になる。CPU single-processは高性能ではないが、
目的に対する継続可能なhostとしては機能した。高火力の統合testへ切り替える時点は、
別のUser Gateとhardware receiptを要求する。

安全境界として、local-only sourceをcloud providerへ送らない、model downloadを自動化しない、
secretやtokenをreceiptへ書かない、という既存#6の条件を維持する。

## [INTERPRETATION] #20 Edge Bootstrap / Gate

bootstrapは「base modelがある」だけでは完了しない。今回も、依存、source、slice、F0、feature、
filelist、train、index、変換、品質評価を別Gateにした。`unknown != pass`、`checkpointなし != 学習完了`、
`epoch到達 != 歌唱品質合格`を明示できる。

## [INTERPRETATION] #29 Fold Cluster

同一の「落ちた」報告に複数candidate causeが共存した。Terminal/AppKit、Python import、無音clip、
TCPStore、shared memoryを単一原因へ潰さず、source、時刻、host、stage、observed／hypothesis、
recovery、unknownを関係付きで保持するのがFold Clusterの小さな追試例になる。これは量子論や
物理superpositionの主張ではなく、障害解析上の未収束候補を保持する工学的用法である。

## [UNKNOWN / NOT IMPLEMENTED]

- Atlantis RunnerがこのRVC processをdispatch・resumeしたわけではない。
- `task_id`／PID lease／heartbeat／checkpoint resumeのAtlantis実装は未確認。
- 高火力provider、DAW/AU、model index、歌唱品質、公開・再配布条件は未確認。
- ここでのCPU時間とsandbox errorは、全provider・全OSの一般則ではない。

## [NEXT]

- #9へ、host crashとchild/task stateを分離するreceipt fixture候補を返す。
- #6へ、resource eventとcapability stateを混同しないCPU fallback観測を返す。
- #20/#29へ、bootstrap Gateと未収束原因clusterのfixture候補を返す。
- Manifestのcanonical schema採用後に、必要なfieldだけを差分反映する。
