# Atlantis note transfer plan

状態: `[CANONICAL-CANDIDATE]`

ここは、Atlantisのnoteから別repositoryへ反映する候補の待機列です。ここへ置いたことは、転送先への
変更権限、採用決定、実装依存を意味しません。

転送票には次を記録します。

```text
source note:
target repository:
target responsibility:
reason:
meaning to preserve:
required restructuring:
license／Provenance:
status: queued | accepted | transferred | rejected | superseded
target commit／document:
```

生noteをそのままコピーせず、転送先の`AGENTS.md`、Schema、文書レジスターに合わせて再構成します。
転送後は元noteと転送票から、反映先のcommitまたは文書を参照します。
