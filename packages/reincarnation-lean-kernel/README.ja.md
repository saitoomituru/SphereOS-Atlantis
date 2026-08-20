# Sphere Reincarnation Lean Kernel

状態: `[SCAFFOLDED]` `[RUNTIME NOT IMPLEMENTED]`

意味管理情報子clusterを別Vessel／Presentationへ渡しても、source、scope、unknown、provenance、authority、
因果を崩壊させない最小のtransaction核です。

予定する境界:

- `src/`: provider／GUI／Forge非依存のstate machineとcontract
- `tests/`: lease、write-set、conflict、prepare／commit／suspend／abort／branchの負例
- build output: source treeへcommitしない

Providerの認証・課金・policy、GUI描画、GitHub API、model inferenceはこのpackageの責務外です。
