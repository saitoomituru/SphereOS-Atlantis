# Forge Map／Quest Map

状態: `[0.25.1-alpha.1 CANDIDATE]`

工学者が未実装のフレーバーを実装済み機能と誤認せず、神学者、哲学者、スピリチュアル実践者、
ゲーマーが原案を配信済みquestと誤認しないよう、状態を二つのMapと五軸へ分けます。

- [Forge Map](../../status/forge-map.json): code、runner、workspace、module、火力の状態
- [Quest Map](../../status/quest-map.json): Note、物語、倫理探究、UX questの状態
- [状態registry](../../status/registry.json): 軸と許容値

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

```bash
python3 -m atlantis_cli status validate --json
```
