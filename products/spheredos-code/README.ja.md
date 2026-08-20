# SphereDOS Code

状態: `[SCAFFOLDED]` `[GUI NOT IMPLEMENTED]`

VS Code上で各社CLI、task、World／Fold、OAE、diff、receiptを同じCockpitへ投影するPresentation候補です。
GUIはauthorityやtransaction正本ではなく、Lean Kernel／SphereDOS Serverのdecisionを表示するclientです。

- `src/`: extension host／webview／CTL client adapterの予定地
- `tests/`: Kernel decisionとGUI表示の一致fixture予定地
- provider固有GUIの再実装や課金画面の代理提供は非目標

VS Codeが終了してもtaskを失わないこと、Kernel拒否を成功表示しないことを最初の受入境界にします。
