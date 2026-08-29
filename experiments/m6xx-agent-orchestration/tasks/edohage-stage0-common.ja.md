# EDOHAGE-TUBO Stage 0 clean-room実装task

## task identity

- experiment: `experiment://spheredos/m6xx/foldnic-hage-native-agent-bench@1`
- Atlantis Issue: https://github.com/saitoomituru/SphereOS-Atlantis/issues/26
- target Issue: https://github.com/saitoomituru/EDOHAGE-TUBO/issues/1
- target repository: `saitoomituru/EDOHAGE-TUBO`
- exact base SHA: `9d1b88517cf03c2dfe45603e641c43ed60b7a81d`
- branch: controllerが指定するagent専用branch
- execution: bare metal native CLI。Dockerを使わない

## 役割と権限

Architect DesignerはUserである。あなたはCoderとして、現在の専用worktreeだけを編集する。
CodexはSphereDOS 0.6xx Test Controller／Observer／Buddyであり、製品コードの実装者ではない。

許可:

- 現在のagent専用branch／worktree内の変更
- 小さな意味単位の日本語commit
- 自分のagent専用branchへのremote push
- EDOHAGE-TUBO Issue #1への秘密非包含receipt
- 通常のcompile／test／lint failureのdebug

不許可:

- `main`への直接push、merge、Issue close
- force push、既存履歴rewrite、別agent processの停止
- 他方agentのbranch、worktree、transcript、未公開成果を読むこと
- actual secret、credential、private World資産の探索・読出し・log・commit
- raw key materialを通常receipt／Issueへ記載すること
- Dockerの導入、別repositoryの変更、固定source revisionの更新

## source closure

最初に対象worktreeの`AGENTS.md`が指定する必読sourceを順に読む。固定revisionは
`workspace/components.json`を正本とする。隣接repositoryの現在HEAD、会話memory、他agent成果で補完しない。

最低限:

- EDOHAGE-TUBO `AGENTS.md`、README、PLI、repository境界、HAGE posture、局所AGENTS
- ZeroRoomLab-manifest `e13dc44969a279cbd02992b267a5354644896f54`
- fold-nic `939e3e5ccbe2437e92a31faaf3ed6838656dde9f`のAGENTS、Issue #5／#6設計
- SphereOS-Atlantis `5f7a697e81b77b8286884f75840e3638dcc7ed68`のAGENTS、PLI／runner境界

必須sourceを解決できない場合は`CONTEXT-INCOMPLETE / stop-before-mutation`として、秘密を含まない
不足sourceと再開条件をIssue #1へ記録して停止する。

## 今回の実装scope

EDOHAGE-TUBO Issue #1の次の3項目を、negative testから小さく実装する。

1. `INSECURE_PUBLIC_TEST_KEY`と明記した決定的DEVHAGE fixture
2. `origin / strength_profile / compromise_state / lifecycle`のmachine-readable Schemaと負例
3. production profileでDEVHAGE／TIBIDEVHAGEをfail-closed拒否するpolicy test

設計詳細はrepository契約とtestから導ける範囲で選べる。独自暗号primitiveは作らない。Stage 0では実鍵生成、
OS Keychain／HSM、E2EE、Fold NIC runtime adapter、GUI runtime、rotation／recovery実装へ広げない。

公開fixtureに秘密性はない。秘密鍵まで含む場合は、専用path、`INSECURE_PUBLIC_TEST_KEY`、production不可、
source revisionをmachine-readableに固定する。公開fixtureをactual secretと呼ばず、actual secret取扱規約を
公開fixtureへ緩和しない。

HAGE aliasはpresentationである。machine判定は構造化fieldとstable codeを正本とし、身体的特徴、色、坊主画像、
ジョーク文をrisk計算へ使わない。短いEd25519 encodingを`TIBIHAGE`へfallbackせず`INVALID_PUBLIC_KEY`として拒否する。

## 開発方法

1. 既存tool／Schema／testを探索し、reuse／extend／adapt／create判断を開発ログへ残す
2. negative testを先に置くか、同一checkpoint内で実装と負例を対応させる
3. 小さく意味のある単位で日本語commitする
4. 各checkpointでrepository指定の検証を実行する
5. 再開可能なgreen checkpointを自分のbranchへpushする
6. Issue #1へcommit、command、結果、未試験、UNKNOWNを日本語で追記する

`git add .`、`git add -A`を使わず、対象pathを明示してstageする。unrelated差分を混ぜない。

## 必須検証

```console
python3 -B -m unittest discover -s tests -v
python3 -B scripts/edohage_dev.py validate --json
python3 -B scripts/edohage_dev.py doctor --json
git diff --check
```

追加runtime／languageを選んだ場合は、その選定理由、license、offline再構築、未試験環境を開発ログへ残す。

## 停止条件

局所修正で閉じない次の問題だけをfatal blockerとする。

- AGPL非互換結合が不可避
- actual private key／credentialが履歴へ入った疑い
- DEVHAGEをproduction経路で拒否できない構造
- plaintext／key materialがFold NIC、通常receipt、logへ流れる構造
- fail-openにしなければ成立しない
- 必須sourceを解決できず推測実装になる

通常のtest failure、依存不足、設計差、未実装は即時停止理由ではない。debugするか`NOT_IMPLEMENTED`を保持する。

## handoff

終了時に次を日本語で返す。

- branchとbase／after SHA
- 読んだ固定source revision
- 実装したもの／しなかったもの
- 既存tool探索とreuse判断
- test commandと結果
- commit／push／Issue receipt
- side effect、network、authority
- UNKNOWN、human review、次の一手
- clean-room保持: 他agent outputを入力へ使わなかったこと
