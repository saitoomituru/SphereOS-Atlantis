# runner・機械拘束・証跡の分離契約

状態: `[CANONICAL-CANDIDATE]` `[IMPLEMENTED-ALPHA]`  
制定日: 2026-08-08  
適用scope: SphereOS Atlantis Prompt Engineering Edition、Sphere-DOS、PLI／CLI、GitHub Actions

## 1. 目的

Atlantis固有のstandalone runnerが未実装であることを、CLI、validator、test、CI、Git履歴まで
「実装されていない」「全部prompt依存」と誤変換する事故を防ぎます。同時に、GitHub Actionsが動くことを
standalone SphereOS runtime、model inference、常駐schedulerの実装証拠へ昇格する事故も防ぎます。

この契約では、操作面、実行主体、機械拘束、証跡を別axisとして扱います。

## 2. 用語

| axis | この契約での意味 | 現在の例 |
|---|---|---|
| Interface | 利用者が意図またはcommandを渡す面 | PLI、CLI |
| Execution Envelope | 実際に処理を行える環境・connector・host | SaaS AI、Git connector、local Python、GitHub-hosted runner |
| Atlantis runner | Atlantis固有のcomponent runtime、常駐scheduler／daemon、model inference等を起動・管理する実行系 | `NOT IMPLEMENTED` |
| Mechanical verification | deterministicなcommand、validator、test、workflowで受入条件を機械判定する面 | `atlantis_cli`、unit test、`verify.yml`、`note-pr.yml` |
| Receipt / Provenance | 何をどのrevisionで実行し、何が返ったかを追跡する証跡 | commit SHA、workflow run、test result、Git history |
| Authority | read、write、push、merge、外部操作等の権限 | Execution Envelopeごとに別管理 |

GitHub ActionsのjobはGitHub-hosted runner上で実行されます。この`runner`という一般名と、
SphereOS Atlantisの`standalone-runner` itemは同じ責務ではありません。

## 3. 現在の実装境界

2026-08-08時点で、少なくとも次を分離します。

```text
Prompt Line Interface                         AVAILABLE / contract present
Command Line Interface                        IMPLEMENTED-ALPHA
repository validators / unit tests             IMPLEMENTED-ALPHA
GitHub Actions mechanical verification         IMPLEMENTED-ALPHA
Git commit / workflow receipt                  AVAILABLE-NOW
Atlantis standalone runtime                    NOT IMPLEMENTED
Atlantis model inference runtime               NOT IMPLEMENTED
persistent scheduler / daemon                  NOT IMPLEMENTED
all-component production integration           UNKNOWN / NOT TESTED
```

`standalone runtime: NOT IMPLEMENTED`は、Atlantis固有runtimeの状態です。PLI、CLI、CI、repository contract、
Git receipt全体の状態ではありません。

## 4. 現行の機械拘束面

`.github/workflows/verify.yml`はpush、pull request、手動起動からGit追跡物を取得し、Python環境を再構築して
次を実行します。

- unit test
- read-only doctor
- component workspace planのoffline検証
- CORN正本のoffline検証
- Forge／Quest状態のoffline検証
- alpha release候補のoffline検証
- Sphere-DOS local scaffoldのboot／status
- Python 3.14側でGit追跡物だけを使うclean-room再構築

`.github/workflows/note-pr.yml`はNote-only PRについて、base／head SHAを渡して境界validatorを実行します。
これらは自然言語の自己申告ではなく、workflowに記述されたcommandのexit statusで合否を返す機械検査です。

2026-08-08にGitHub APIから観測した履歴では、`最小再構築検証`はrun 41まで到達し最新run 41が
`success`、`Note-only PR検証`はrun 9が`success`でした。

- `https://github.com/saitoomituru/SphereOS-Atlantis/actions/runs/31114556857`
- `https://github.com/saitoomituru/SphereOS-Atlantis/actions/runs/29687900790`

この観測は各runが対象revisionで成功したことを示します。将来run、第三者fork、未列挙OS、全component、
production loadまで自動的に保証しません。

## 5. PLIと機械拘束の接続

PLIは自然言語で目的、Context、制約、unknownを扱う操作面です。PLI自身がすべての拘束を自由文で
完結させる必要はありません。

```text
natural-language intent
  -> repository contract / AGENTS / Manifest
  -> selected action
  -> CLI / validator / test when deterministic projection exists
  -> GitHub Actions or local execution envelope
  -> receipt
```

したがって、Prompt Engineering Editionを「機械拘束ゼロのprompt芸」と説明しません。一方、自然言語から
まだCLI／Schema／testへ射影されていない判断は、機械保証済みへ昇格しません。

## 6. 証跡の主張強度

証跡は次の強度で閉じます。

```text
workflow definition exists
  != workflow executed

workflow executed successfully at revision X
  != all revisions are green

specified checks are green
  != whole system is green

GitHub-hosted runner executed Sphere-DOS scaffold checks
  != Atlantis standalone runner exists
```

`local green != system green`、`unknown_is_pass = false`を維持します。

## 7. 第三者追試

第三者は、作者の会話ログや同一AI人格を再現する必要はありません。少なくとも次の別々の追試ができます。

1. clone／forkしたGit追跡物からvalidatorとunit testを実行する
2. GitHub Actionsが同じ受入条件を実行することを確認する
3. PLIから別coding agentへ実装依頼し、生成差分が同じrepository contractとCIを通るか確認する
4. 失敗時に`unknown`、test failure、Issue／receiptが保持されるか確認する

第三者再現が増えた場合、それは「特定modelが賢かった」仮説と「repository側の制御面が効いた」仮説を
切り分ける追加Evidenceになります。現時点で第三者再現件数は`unknown`です。

## 8. 受入条件

- Atlantis固有runner未実装と、機械検証面実装済みを別fieldで表示する
- GitHub-hosted runnerをAtlantis standalone runnerへ数えない
- PLIをCLIの偽物へ降格しない
- CLI／CI greenを意味・神学・全runtimeのsystem greenへ拡張しない
- workflow run、revision、command、未試験範囲を追跡できる
- 未実装・未試験・unknownをpassへ丸めない

## 9. 関連

- [Prompt Line InterfaceとCommand Line Interface](prompt-line-and-command-line-interface.ja.md)
- [Forge Map／Quest Map](../status/forge-and-quest-map.ja.md)
- [`status/forge-map.json`](../../status/forge-map.json)
- [`verify.yml`](../../.github/workflows/verify.yml)
- [`note-pr.yml`](../../.github/workflows/note-pr.yml)
