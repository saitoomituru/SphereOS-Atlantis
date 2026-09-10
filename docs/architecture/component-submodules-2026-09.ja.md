# Atlantis component submodules 2026-09

状態: `[SOURCE-PINNED]` `[RUNTIME-INTEGRATION-PENDING]`
更新日: 2026-09-10

## 目的

SphereOS Atlantis が World / Fold orchestration を実装する際に、FQuery と IBD をコピーや独自forkではなく、それぞれの正本repositoryをrevision固定してlibrary sourceとして参照できるようにする。

## 現在のsubmodule

```text
vendor/FQuery
  source: https://github.com/saitoomituru/FQuery.git
  pinned: 5def6e85a1f448aa9c92cfb761bc655aa07c3bdc

vendor/IBD
  source: https://github.com/saitoomituru/IBD.git
  pinned: 93834835d2da791bfa7c85e18df57cc5354a202b
```

## 責務

```text
FQuery
  FAM selector / traversal / query / fam_ref

IBD
  storage / retrieval / evidence / provenance

Atlantis
  World / Fold / authority / Portal / causal gate orchestration
```

submoduleはsource revisionのpinであり、次を意味しない。

- FQuery / IBDの意味正本をAtlantisへ移す
- submoduleがあるだけでruntime integration済みとする
- IBD検索結果をWorld truthへ昇格する
- FQuery selectorからPortalを暗黙生成する
- runtime起動時に自動network accessする

## clone / update

新規clone:

```bash
git clone --recurse-submodules https://github.com/saitoomituru/SphereOS-Atlantis.git
```

既存clone:

```bash
git submodule update --init --recursive
```

上流revisionを更新する場合、各submoduleで対象commitを明示選択し、親repositoryのgitlink差分をreviewしてcommitする。`main`追随をruntimeで自動実行しない。

## Portalとの関係

```text
FQuery
  describes pointer / route intent
      ↓
Atlantis
  resolves World / Fold compatibility
  direct | Portal | causal gate | Bottom
      ↓
Transformer / runtime
      ↓
OAE receipt
      ↓
IBD
  persists source / result / provenance
```

## 検証状態

- `.gitmodules`: added
- `vendor/FQuery`: gitlink mode `160000`
- `vendor/IBD`: gitlink mode `160000`
- source revisions: pinned
- clean clone + recursive checkout: `NOT TESTED` in this change
- code-level API integration: `NOT IMPLEMENTED` by this change alone
