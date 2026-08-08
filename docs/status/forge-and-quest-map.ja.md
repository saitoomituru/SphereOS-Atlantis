# Forge Map／Quest Map

状態: `[0.250.1]` `[LEGACY 0.25.1-alpha.1 CANDIDATE]`

工学者が未実装のフレーバーを実装済み機能と誤認せず、神学者、哲学者、スピリチュアル実践者、
ゲーマーが原案を配信済みquestと誤認しないよう、状態を二つのMapと五軸へ分けます。

- [Forge Map](../../status/forge-map.json): code、runner、workspace、module、火力の状態
- [Quest Map](../../status/quest-map.json): Note、物語、倫理探究、UX questの状態
- [状態registry](../../status/registry.json): 軸と許容値

Mapの正規座標は`0.250.1`で、`0.25.1-alpha.1`は配布互換aliasです。Map itemの状態と
SemanticKernel座標は別軸であり、`engineering_state`の変化をKernel変更として扱いません。

```text
content_maturity    原案／討論中／採用契約
engineering_state  未着手／設計中／実装中／local検証済み／保存放置
distribution_state 未配信／branchのみ／alpha候補／release済み
resource_state     火力あり／火力待ち／community test募集
review_state       review未募集／募集／進行／受理
```

一つの`DONE`へ潰しません。たとえば哲学・倫理束は価値があっても`engineering_state: not-started`、
CORNはlocal testを通っていてもmerge前なら`distribution_state: branch-only`です。

現在の全体像は「凍結」ではありません。サルベージと開発足場の一部は開いて動き、runnerやedge moduleは
火力待ち、旧3.x／4.x残骸は保存放置です。`resource-wait`は却下でも完成でもなく、第三者参入を待てる状態です。

## 2026-08-08: runnerと機械拘束を別軸で読む

`standalone-runner`が`not-started`であることを、Atlantis全体に機械拘束が存在しないという意味へ拡張しません。
現行のAtlantis固有standalone runtime、model inference、常駐scheduler／daemonは未実装です。一方で、
repository内にはCLI、validator、unit test、GitHub Actionsによる機械検証面があり、Git追跡物だけから
再構築・検査する経路が動いています。

```text
Prompt Line Interface      = 自然言語で意図・文脈・拘束を渡す操作面
Command Line Interface     = command／argumentへ落とす再現可能な操作面
Mechanical verification   = CLI、validator、unit test、GitHub Actionsによる合否拘束
Receipt / provenance       = commit SHA、workflow run、test結果、Git履歴
Atlantis standalone runner = NOT IMPLEMENTED
```

GitHub Actions自身はGitHub-hosted runner上で実行されますが、これはAtlantis固有のstandalone runnerが
実装済みという意味ではありません。逆に、Atlantis固有runnerが未実装だからといって、CI、CLI、validator、
Git receiptまで未実装へ丸めることもできません。詳細は
[runner・機械拘束・証跡の分離契約](../architecture/runner-and-mechanical-verification-boundary.ja.md)を参照してください。

2026-08-08の状態更新そのものが機械拘束の自己追試になりました。Forge Mapへ9個目のitemを追加したcommit
`400eb480f83d740dbaf24facaec384f0bf8746ed`に対する`最小再構築検証` run 42は、status map testが
旧fixture `[8, 5]`に固定されていたため、実測`[9, 5]`を拒否して`failure`になりました。fixtureを
9件へ追従したcommit `87768f5b1051d92cffc0dab93e418c089b02f446`ではrun 43が`success`となり、Python 3.11／3.14の
unit test、doctor、各offline validator、Sphere-DOS scaffold検査が通り、3.14ではclean-room再構築まで
成功しています。`Note-only PR検証` run 9も既存の成功証跡として保持します。

この系列は「CIが存在する」という文書自己申告だけでなく、状態契約の差分を実際に拒否し、fixture修正後に
再受理したreceiptです。ただし、列挙checkがそのrevisionでgreenであることを示すだけで、全component runtime、
production環境、第三者fork、未列挙条件までsystem greenへ昇格する証拠ではありません。

```bash
python3 -B -m atlantis_cli status validate --json
```
