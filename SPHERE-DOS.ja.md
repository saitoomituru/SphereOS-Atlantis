# Sphere-DOS quick start

SphereOS Atlantis `main`（stable基準線）のSphere-DOSには、用途と拘束強度が異なる4つの導入Surfaceがあります。

同じものを4通りに包装しているのではありません。
Prompt／Contextだけを借りる軽量利用から、Git／CLI／containerまで含めたNative Engineering Surfaceまで、必要な責務だけを選びます。

## 導入Surface一覧

| Surface | 配置 | 主な用途 | 機械拘束 | GitHub / CLI | 状態 |
|---|---|---|---|---|---|
| 1. Sphere-DOS workspace / fork展開 | Sphere-DOS側のworkspace配下へcomponentを固定revisionで展開 | Atlantis本体・AAE・IBD・ASTRO等を横断開発 | 強い | 前提 | 実装済み |
| 2. `.vendor` submodule埋め込み | 利用側repositoryからSphereOS Atlantisをsubmoduleとして保持 | 他projectへ開発足場・CLI・監査器を持ち込む | 強い | 前提 | 運用実績あり |
| 3. PLI Context Alias | 利用側へ小さなMarkdown入口を置き、Sphere-DOSのMarkdown / AGENTS系contextを参照 | Prompt Engineering、設計規約、FQuery等のcontext注入 | 軽い | 不要 | 現行運用あり |
| 4. Fork-on-Live / Dev Container | SphereOS Atlantis自身をCodespaces / devcontainer等でlive起動 | 自分のprojectへSphereを埋めず、Native Surfaceを一時利用 | 強い | GitHub環境向け | 起動確認済み・大規模自動開発は未検証 |

### どれを選ぶか

- **Sphereそのものを鍛造する／複数componentを横断する** → 1
- **自分のrepositoryへCLI・MAGI・監査器まで固定して持ち込みたい** → 2
- **AIへ設計文脈だけ渡したい／Git依存を増やしたくない** → 3
- **Codespaces等で重い開発面を一時的に使い、自分のrepositoryへSphereを埋めたくない** → 4

`MAGI`、GitHub Actions、CLI監査、filesystemやtestを伴う機械拘束を利用する場合は、原則としてSurface 1 / 2 / 4のNative Engineering Surfaceを使用します。
Surface 3はPrompt Line Interface上のcontext aliasであり、CLIを実行したこと、GitHub Actionsを走らせたこと、MAGI resolverを実行したことの代替証拠にはなりません。

## 1. Sphere-DOS workspace / fork展開

SphereOS Atlantis 0.25.1-alpha.1の再現可能な作業机を、固定revisionのcomponent群から組み立てます。

```bash
python3 scripts/bootstrap_venv.py
.venv/bin/python -B -m atlantis_cli workspace plan
.venv/bin/python -B -m atlantis_cli workspace init
.venv/bin/python -B -m atlantis_cli sphere-dos boot
.venv/bin/python -B -m atlantis_cli sphere-dos status
.venv/bin/python -B -m atlantis_cli status validate
```

`workspace init`だけがnetworkを明示使用します。既存checkoutはpull、reset、clean、rebaseしません。

このSurfaceではSphere-DOS側がcomponentの固定revisionとworkspaceを所有し、各component repositoryのGit履歴と`AGENTS.md`を保持したまま展開します。

## 2. `.vendor` submodule埋め込み

既存project側からSphereOS AtlantisをGit submoduleとして固定し、Sphere-DOSのCLI、規約、監査器、開発足場を利用する方式です。

概念配置:

```text
YourProject/
├─ AGENTS.md
├─ src/
└─ .vendor/
   └─ SphereOS-Atlantis/   # git submodule
```

この方式はGit revisionを明示固定できるため、GitHub Actions、CLI、MAGI等の機械拘束と相性があります。
一方で、依存repository同士が互いをsubmoduleとして所有する循環参照は避けます。
実行時・Context上の相互参照が必要でも、Git所有グラフはDAGとして保ちます。

具体的なsubmodule追加コマンドや更新policyは、利用側repositoryの責務・branch policyに合わせて管理してください。

## 3. PLI Context Alias

SphereOS Atlantis本体をGit submoduleとして埋め込まず、利用側repositoryに小さなMarkdown入口を置き、AI agentからSphere-DOSのMarkdown、`AGENTS.md`、設計契約へ辿らせる方式です。

概念配置:

```text
YourProject/
├─ AGENTS.md
└─ SPHERE-DOS.md
```

`AGENTS.md`から`SPHERE-DOS.md`を入口として読み、その先で明示されたSphere側contextだけを探索します。
これはPrompt Line Interface上の**Context Alias**であり、Git submoduleでもpackage installでもありません。

用途:

- 設計規約・責務境界だけ借りる
- FQuery等、repository間でcontext参照が循環しうる機能にGitの循環所有を持ち込まない
- agentの探索範囲を明示された境界内に限定する
- GitHub CLIやActionsを必要としない軽量なPrompt Engineering利用

このSurfaceでは、Markdownを読めることと、CLI・MAGI・GitHub Actionsが実行可能であることを混同しません。
機械拘束が必要になった時点でSurface 1 / 2 / 4へ昇格します。

## 4. Fork-on-Live / Dev Container

SphereOS Atlantis repository自体をGitHub Codespaces、VS Code Dev Containers等でlive起動し、Native Engineering Surfaceを利用します。

repositoryには`.devcontainer/devcontainer.json`があり、Python 3.12系containerと`postCreateCommand`によるdevelopment venv初期化を定義しています。

この方式では、自分のprojectへSphereOS Atlantisをsubmoduleとして埋め込まず、liveなSphere-DOS側から対象projectを扱えます。

向いている用途:

- Codespaces / GitHub Copilot等のGitHub統合環境
- temporaryなNative Engineering Surface
- CLI、filesystem、test、Git操作を伴う作業
- 自分のprojectのGit所有グラフへSphereを追加したくない場合

現時点ではdevcontainer起動と簡単なrepository maintenanceの観測があります。
大規模な自動開発、長時間runner、全componentを含むclean-room完走を一般化できるほどの検証はまだありません。
quota、provider、agent、repository権限はSphere-DOSそのものとは別のExecution Envelopeとして扱います。

## 実行境界

このbootはPrompt Engineering Editionのlocal development shellです。
standalone OS runtime、model inference、component runtimeを実装済みとは表示しません。

Surface 1 / 2 / 4はNative Engineering Surfaceへ接続できますが、「配置した」「cloneできた」「containerが起動した」だけでcomponent runtimeやMAGI監査の合格を意味しません。
Surface 3はcontext注入面であり、Native実行の証拠にはなりません。

詳細、Windows手順、revision更新、証拠境界は
[複数repository workspaceとSphere-DOS最小展開](docs/development/workspace-and-sphere-dos.ja.md)
を参照してください。
