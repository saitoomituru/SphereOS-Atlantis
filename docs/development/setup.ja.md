# Sphere-DOS開発環境の最小再構築

状態: `[ALPHA]` `[LOCAL VENV TESTED]` `[DEVCONTAINER STATIC VALIDATED]` `[CONTAINER BUILD NOT TESTED]`

目的は、吊るしのVS CodeとPythonから、いま人間とcoding agentが会話・実装・検証している最小環境を
再構築することです。個人のtheme、秘密値、認証、特定vendorのmodel設定は焼き込みません。

## 1. 必要なもの

- Git
- Python 3.11以上
- VS Code（推奨。CLIだけでもcore testは実行可能）
- container経路を使う場合だけDocker／PodmanまたはGitHub Codespaces

VS CodeのPython拡張はworkspace内のvirtual environmentを検出できます。このrepositoryではOS間で
interpreter実体pathが違っても共有できるよう、`python.defaultInterpreterPath`へ`${workspaceFolder}/.venv`
というdirectoryを指定します。

公式資料:

- [VS Code Python settings reference](https://code.visualstudio.com/docs/python/settings-reference)
- [VS Code command line interface](https://code.visualstudio.com/docs/configure/command-line)
- [GitHub Codespaces: Introduction to dev containers](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers)

## 2. Local venv

macOS／Linux:

```bash
python3 scripts/bootstrap_venv.py
.venv/bin/python -B -m atlantis_cli doctor
.venv/bin/python -B -m unittest discover -s tests -v
```

Windows PowerShell:

```powershell
py -3 scripts/bootstrap_venv.py
.venv\Scripts\python.exe -B -m atlantis_cli doctor
.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

既定bootstrapは標準libraryの`venv`とbundled `ensurepip`だけを使い、外部packageを取得しません。
Skill validator用PyYAML等を導入する場合だけ、network利用可能性を明示した次を実行します。

```bash
python3 scripts/bootstrap_venv.py --install-dev
```

bootstrapはmodelを呼ばず、provider認証を開始せず、`.env`や秘密資産を探索しません。

## 3. 吊るしのVS Code

1. repository rootをVS Codeで開く。
2. 推奨されたPython、Pylance、Dev Containers拡張のうち必要なものを導入する。
3. `Terminal > Run Task > Atlantis: venv作成（offline）`を実行する。
4. Python interpreterが`.venv`であることをstatus barで確認する。
5. `Atlantis: doctor`と`Atlantis: unit test`を実行する。

macOSでVS Codeアプリはあるが`code`がPATHにない場合は、Command Paletteから
`Shell Command: Install 'code' command in PATH`を選ぶか、GUIからrepositoryを開けます。
`doctor`はアプリ内CLIの存在を検出してWARNを返しますが、勝手にPATHを書き換えません。

`.vscode/settings.json`は共同作業に必要なinterpreter、test、watch除外だけを持ちます。theme、font、
keybinding等の個人設定は利用者側に残します。

## 4. Coding agent deck

検出はCLIの存在だけを読み、起動、ログイン、課金、model callを行いません。

```bash
.venv/bin/python -B -m atlantis_cli agent detect --json
.venv/bin/python -B -m atlantis_cli agent plan --json
```

session contractを実際に生成する場合だけ`init`を使います。これもmodelは呼びません。

```bash
.venv/bin/python -B -m atlantis_cli agent init --provider codex --json
.venv/bin/python -B -m atlantis_cli agent verify --provider codex --json
```

複数agentが同時に書く場合は同じworking treeを共有せず、分離git worktreeを使います。

## 5. GitHub Codespacesとcode-serverの区別

GitHub CodespacesはGitHubが提供するremote development environmentで、repositoryの
`.devcontainer/devcontainer.json`を読めます。起動時間とmachine sizeに応じて費用が発生し得るため、
Atlantisのagent初期化やtestから自動起動しません。

現在のprofileはMicrosoft公式`mcr.microsoft.com/devcontainers/python:3-3.12-bookworm`を使い、
追加repository権限、host directory mount、port forward、secret推奨を定義しません。container作成を
明示的に選んだ後の`postCreateCommand`でのみdev依存を導入します。

一般に`code-server`と呼ばれるブラウザ版VS Code互換serverは別project・別運用です。GitHub Codespacesを
「Gitそのものの公式code-server」とは呼びません。最初の再構築対象はlocal VS Code、Dev Containers、
GitHub Codespaces互換の一つの`.devcontainer`契約です。

## 6. 現在の実測

2026-07-18時点の主検証hostでは次を観測しています。

| 項目 | 状態 |
|---|---|
| Python 3.14.6 `.venv` | `TESTED` |
| local unit test | `TESTED` |
| VS Code application | `OBSERVED` |
| `code` on PATH | `NOT AVAILABLE`／app内CLIは観測 |
| Docker／Podman | `NOT AVAILABLE` |
| Dev Container build | `NOT TESTED` |
| GitHub Codespaces create | `NOT TESTED`／自動起動禁止 |

host時計はAsia/Tokyoを表示していますが、NTP等の校正証跡はこのtestで取得していないため、doctor receiptは
`calibration: unverified`を保持します。

## 7. CIとclean-room

GitHub ActionsはPython 3.11／3.14でVenv、全unit test、read-only doctorを実行します。3.14 jobではさらに、
Git追跡済みrevisionだけを一時directoryへ展開するclean-room testを実行します。

localで現在のcommitを同じ条件へ通す場合:

```bash
.venv/bin/python -B scripts/clean_room_test.py --json
```

clean-roomは`git archive`対象だけを読み、untracked file、local-only asset、秘密directoryを探索・複製しません。
外部packageを導入せず、model、認証、Codespaces、containerを起動しません。

CIのGitHub token権限は`contents: read`のみで、checkout後のcredential保持も無効です。CIからcommit、push、
release、外部service書込みを行いません。
