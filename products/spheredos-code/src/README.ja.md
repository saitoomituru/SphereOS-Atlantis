# extension source

状態: `[IMPLEMENTED-ALPHA]` `[MOCK FIXTURE ONLY]`

- `extension.js`: command登録とCockpit lifecycle
- `cockpit-panel.js`: nonce付きCSP、Webview、fixture再読込
- `fixture-transport.js`: 固定allowlistの合成fixture reader
- `cockpit-model.js`: 状態機械を分離するprojectionとHTML escape
- `webview/`: VS Code themeへ追従する表示面

GUIはKernel decisionのprojectionであり、OAE commit authorityまたはdurable state正本にはしません。
Production CTL client adapterは`NOT IMPLEMENTED`です。
