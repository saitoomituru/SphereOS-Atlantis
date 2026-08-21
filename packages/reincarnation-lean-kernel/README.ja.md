# Sphere Reincarnation Lean Kernel

状態: `[FILESYSTEM HARNESS IMPLEMENTED-ALPHA]` `[PRODUCTION RUNTIME NOT IMPLEMENTED]`

意味管理情報子clusterを別Vessel／Presentationへ渡しても、source、scope、unknown、provenance、authority、
因果を崩壊させない最小のtransaction核です。

予定する境界:

- `src/`: provider／GUI／Forge非依存のstate machineとcontract
- `tests/`: lease、write-set、conflict、prepare／commit／suspend／abort／branchの負例
- build output: source treeへcommitしない

Providerの認証・課金・policy、GUI描画、GitHub API、model inferenceはこのpackageの責務外です。

## Filesystem／Reincarnation Kernel Harness

将来のLean Kernelが扱うfilesystem layoutと拒否条件を、明示された一時rootとsynthetic
fixtureだけで再現する試験Harnessです。production Kernelではありません。

| 対象 | 状態 |
|---|---|
| Filesystem Harness (`sphere_reincarnation_harness`) | `IMPLEMENTED-ALPHA`候補 |
| Synthetic decision fixtures (`fixtures/`) | `IMPLEMENTED-ALPHA`候補 |
| Production Lean Kernel | `NOT IMPLEMENTED` |
| Durable OAE persistence | `NOT IMPLEMENTED` |
| Production lease manager | `NOT IMPLEMENTED` |
| SphereDOS Server integration | `NOT IMPLEMENTED` |
| GUI integration | `NOT IMPLEMENTED` |
| Real provider execution | `NOT IMPLEMENTED` |
| User dotfiles layout (`~/.spheredos`等) | `NOT STANDARDIZED` |

Harnessの完成は、上記のいずれのproduction項目もKernel完成へ昇格しません。

実装、結合、検証、配布物化、公開範囲、保守責任は
[m.6xx.1 能力状態表](../../docs/status/m6xx-capability-matrix.ja.md)で別軸に管理します。

### 使い方

Python標準libraryのみを使用し、dependency追加、network access、package installは行いません。
`--root`は必須であり、home／cwdを既定値にしません。`/`、user home、repository rootそのものは
harness rootとして拒否します。

```bash
PYTHONPATH=packages/reincarnation-lean-kernel/src \
python3 -B -m sphere_reincarnation_harness.cli plan --root /explicit/test/root --json

PYTHONPATH=packages/reincarnation-lean-kernel/src \
python3 -B -m sphere_reincarnation_harness.cli init --root /explicit/test/root --json

PYTHONPATH=packages/reincarnation-lean-kernel/src \
python3 -B -m sphere_reincarnation_harness.cli inspect --root /explicit/test/root --json

PYTHONPATH=packages/reincarnation-lean-kernel/src \
python3 -B -m sphere_reincarnation_harness.cli evaluate \
  --root /explicit/test/root \
  --fixture packages/reincarnation-lean-kernel/fixtures/lease-missing.json \
  --json
```

`plan`と`inspect`はfilesystemを変更しません。`init`と`evaluate`は明示root配下
`.spheredos-harness/`以外へ書き込みません。`evaluate`が返すdecision envelopeは
`accepted`でも`effect_applied: false`を常に維持し、実Effectを適用しません。

### 拒否fixture

`fixtures/`配下のsynthetic fixtureは`harness_only: true` `canonical_contract: false`
`authority: none`を明示し、正式OAE Schemaを名乗りません。

- `lease-missing`: leaseなしwriteをrejected
- `stale-base-revision`: base_revisionとobserved_revisionの不一致をrejected
- `write-set-violation`: write_set外requested_pathsをrejected
- `duplicate-artifact-claim`: 別taskが競合claim済みの同一artifactをrejected
- `provider-exit-zero-not-commit`: provider exit 0をOAE commitへ自動変換せずsuspended
- `valid-prepared`: 上記いずれにも該当しないacceptedの対照例（`effect_applied`はfalseのまま）
