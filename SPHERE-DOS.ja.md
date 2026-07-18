# Sphere-DOS quick start

SphereOS Atlantis 0.2.1の再現可能な作業机を、固定revisionのcomponent群から組み立てます。

```bash
python3 scripts/bootstrap_venv.py
.venv/bin/python -B -m atlantis_cli workspace plan
.venv/bin/python -B -m atlantis_cli workspace init
.venv/bin/python -B -m atlantis_cli sphere-dos boot
.venv/bin/python -B -m atlantis_cli sphere-dos status
```

`workspace init`だけがnetworkを明示使用します。既存checkoutはpull、reset、clean、rebaseしません。

このbootはPrompt Engineering Editionのlocal development shellです。
standalone OS runtime、model inference、component runtimeを実装済みとは表示しません。

詳細、Windows手順、revision更新、証拠境界は
[複数repository workspaceとSphere-DOS最小展開](docs/development/workspace-and-sphere-dos.ja.md)
を参照してください。
