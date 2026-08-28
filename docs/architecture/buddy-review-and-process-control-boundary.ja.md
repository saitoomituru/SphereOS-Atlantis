# Buddy Reviewとprocess制御の境界

状態: `[CANONICAL-CANDIDATE]` `[0.2xx MAGI FIX IMPLEMENTED-ALPHA]`  
事故票: [#24](https://github.com/saitoomituru/SphereOS-Atlantis/issues/24)  
Manifest契約候補: [Manifest #31](https://github.com/saitoomituru/ZeroRoomLab-manifest/issues/31)

## 1. 目的

Architect Designerの設計原文をBuddy Reviewerがコーダーへ運び、設計Diffを強く批評する役割と、
別agentへsignal、cancel、killを行うProcess Supervisor権限を分離する。

2026-08-28の事故では、CodexがBuddy依頼からprocess停止権限を推論し、MAGI自己監査より先にClaudeへ
SIGINTを送った。差分は残り秘密漏えいも観測されなかったため、必要な作用は停止ではなく、設計原文と
Diffを並べたreview challengeだった。

## 2. 現行0.2xx.n修繕

Atlantis-MAGIは別agentへの制御作用より前に、自分自身へ次を問う。

- Last Orderは情報注入、review、process controlのどれか
- Observer、Interpreter、Buddy、Architect、Coder、Process Supervisorを統合していないか
- 観測Diffと現在解釈を分離したか
- 設計逸脱の可能性を、停止が必要な破局へ昇格していないか
- transport capabilityをauthorityとして扱っていないか
- 通常のGit rollbackで回復できるか

exactな0.2xx.nの末尾番号はUser Gateであり、この修繕だけで新しいrelease番号を確定しない。

## 3. m.6xx.n機械拘束

m.6xx Dev線の`policy/buddy-actions.json`は次のactionを別capabilityとして宣言する。

```text
EVIDENCE_WHISPER
REVIEW_CHALLENGE
DECISION_SUBSTITUTION
PROCESS_INTERRUPT
WORKTREE_MUTATION
REMOTE_PUBLICATION
```

m.6xx Dev線の`atlantis_cli.buddy`は、Buddy requestをofflineで判定する。

- 設計source付き`EVIDENCE_WHISPER`を許可する
- 設計sourceと確認質問付き`REVIEW_CHALLENGE`を許可する
- POSIX pipe、TTY、session resumeから`PROCESS_INTERRUPT`を導出しない
- User authorizationがあるprocess停止を区別する
- 秘密漏えいまたは不可逆な外部破壊が実行中で、証拠参照がある場合だけEmergency Brake候補を返す

このvalidatorはsignalを送らない。Provider Adapter、Code Cockpit、Archangel Runnerが実際の制御作用前に
呼び出す統合は`NOT IMPLEMENTED`である。unit testのgreenをOS全体への強制済み表示へ昇格しない。

## 4. Buddy packet

次世代Envelope候補は、最低限次を保持する。

```json
{
  "actor_role": "buddy-reviewer",
  "action": "REVIEW_CHALLENGE",
  "architect_source_refs": ["issue://architect/source"],
  "supporting_context_refs": ["manifest://operations/samurai-coding"],
  "observed_diff_refs": ["git-diff://worktree"],
  "conflict_hypothesis": "設計責務が実装から消えた可能性",
  "question_for_coder": "どの条件を保持し、どれを別Vesselへ移しましたか？"
}
```

Buddyはコードと論理を強く批評できるが、Architectの採用判断を捏造しない。コーダーには説明、修正、
反証の余地を残す。

## 5. 公開checkpoint

公開可能な変更は小さな意味単位で日本語commitし、検証済みcheckpointをremoteへpushする。
停電、端末故障、agent context loss、誤編集が起きてもGit Diffから回復できるため、rollback可能な失敗を
理由に探索を止めない。

秘密鍵、credential、private payload、非公開個人情報はcheckpointへ含めない。secret非公開と
公開checkpoint推奨は別境界である。

## 6. 状態

| surface | 状態 |
|---|---|
| 自然言語Buddy契約 | `CANONICAL-CANDIDATE` |
| 0.2xx MAGI不変条件 | `IMPLEMENTED-ALPHA` |
| action policy JSON | `m.6xx Dev線 IMPLEMENTED-ALPHA`／main未提供 |
| offline validator | `m.6xx Dev線 IMPLEMENTED-ALPHA`／main未提供 |
| negative unit test | `m.6xx Dev線 IMPLEMENTED-ALPHA`／main未提供 |
| Provider Adapterへの強制配線 | `NOT IMPLEMENTED` |
| Code Cockpit表示 | `NOT IMPLEMENTED` |
| 常駐Runnerでの制御 | `NOT IMPLEMENTED` |
| exactな0.2xx.n／m.6xx.n | `USER GATE` |
