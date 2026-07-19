# 複数repository workspaceとSphere-DOS最小展開

状態: `[ALPHA]` `[LOCAL UNIT TESTED]` `[PINNED WORKSPACE]` `[NETWORK CLONE NOT TESTED IN THIS CHANGE]`

この導線は、SphereOS Atlantis本体、共通定規、IBD、AAE、ASTROを一つの作業机へ並べます。
隣接repositoryを一つの巨大repositoryへ吸収せず、各repositoryのGit履歴、AGENTS.md、実装正本を保持します。

ここで起動するSphere-DOSは、Atlantis 0.25.1-alpha.1 Prompt Engineering Editionの開発shellです。
standalone OS runtime、model inference、component runtime、7D Fold runtime、Akasha Driver runtimeを
実装済みとは扱いません。

## 1. Atlantis本体の最小環境

macOS／Linux:

```bash
python3 scripts/bootstrap_venv.py
.venv/bin/python -B -m atlantis_cli doctor
```

Windows PowerShell:

```powershell
py -3 scripts/bootstrap_venv.py
.venv\Scripts\python.exe -B -m atlantis_cli doctor
```

## 2. 展開前のoffline plan

```bash
.venv/bin/python -B -m atlantis_cli workspace plan --json
```

Windowsでは`.venv\Scripts\python.exe`へ読み替えます。

planはnetworkへ接続せず、次だけを調べます。

- `workspace/components.json`の形式
- componentの配置先
- 既存Git checkoutのoriginとHEAD
- 固定revisionとの一致
- cloneが必要か、既存pathを保護して停止するか

## 3. 固定revisionからcomponentを展開

network利用を明示して実行します。

```bash
.venv/bin/python -B -m atlantis_cli workspace init --json
```

venv作成前でも、次のwrapperを利用できます。

```bash
python3 scripts/bootstrap_workspace.py --apply --json
```

展開先は`.atlantis/workspace/components/`です。`.atlantis/`はGit追跡対象外です。
既存checkoutをpull、reset、clean、rebaseせず、不一致pathは保持して`blocked`を返します。

対象を絞る場合:

```bash
.venv/bin/python -B -m atlantis_cli workspace init \
  --component ZeroRoomLab-manifest \
  --component IBD \
  --json
```

## 4. VS Code multi-root workspace

展開後、次が生成されます。

```text
.atlantis/SphereOS-Atlantis.code-workspace
```

このworkspaceにはAtlantis本体と、固定revisionへ一致したcomponentだけが入ります。
workspaceへ入ったことは、隣接repositoryへの編集権限、依存関係、同一license、同一Worldを意味しません。
componentを編集する前に、そのrepositoryのAGENTS.mdと正本文書を読みます。

## 5. Sphere-DOS開発shellをboot

```bash
.venv/bin/python -B -m atlantis_cli sphere-dos boot --json
.venv/bin/python -B -m atlantis_cli sphere-dos status --json
```

bootが行うこと:

- `sphere-dos/profile.json`を検証する
- 現在配置済みのcomponentを観測する
- VS Code multi-root workspaceを再生成する
- `.atlantis/sphere-dos/sessions/`へlocal session receiptを書く
- `.atlantis/sphere-dos/current.json`へ現在sessionのpointerを書く

bootが行わないこと:

- model call
- provider login
- secret探索
- network access
- component runtime起動
- database migration
- container起動
- standalone OS runtimeの提供

componentが未展開でも、Atlantis本体だけの`development-shell-partial`としてbootできます。
これは故障の隠蔽ではなく、使える器だけで作業を開始し、欠けたcomponentをreceiptへ残す縮退運転です。

## 6. revision更新

`tracking_ref`は上流更新を観測するための情報であり、自動追従命令ではありません。
再現対象は`revision`の40桁Git SHAです。

上流を更新する場合は、次を別変更として扱います。

1. 上流repositoryの新revisionとAGENTS.mdを読む
2. component固有testを実行する
3. `workspace/components.json`のrevisionを更新する
4. Atlantis側のunit test、doctor、workspace plan、Sphere-DOS bootを再実行する
5. 互換範囲と未試験範囲をPRへ記録する

## 7. 証拠境界

clone成功はcomponent runtimeの動作確認ではありません。
この導線が証明するのは、固定revisionを別Git履歴のまま配置し、作業workspaceとlocal session receiptを
再構成できることまでです。

network clone、container build、各component runtime、hardware profile、production deploymentは、
それぞれ独立した試験票を必要とします。

GitHub Codespacesではrepository、devcontainer、venv promptまでの画面観測がありますが、quota超過により
tutorial、unit test、clean-roomの完走は未確認です。火力を提供できる参加者は
[community test Issue #2](https://github.com/saitoomituru/SphereOS-Atlantis/issues/2)へ環境と結果を残してください。
