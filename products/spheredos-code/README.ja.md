# SphereDOS Code

状態: `[GUI HARNESS IMPLEMENTED-ALPHA]` `[INTEGRATION TEST PENDING]` `[PRODUCTION RUNTIME NOT IMPLEMENTED]`

VS Code上でtask、World／Fold、provider control、OAE、receiptを同じCockpitへ投影するPresentation候補です。
現段階はrepository内の合成fixtureだけを読むGUI Harnessです。GUIはauthorityやtransaction正本ではなく、
将来のLean Kernel／SphereDOS Server decisionを表示するclientです。

## 実装状態

| 対象 | 状態 |
|---|---|
| GUI Harness | `IMPLEMENTED-ALPHA` |
| Mock fixture transport | `IMPLEMENTED-ALPHA` |
| Production CTL connection | `NOT IMPLEMENTED` |
| Lean Kernel runtime | `NOT IMPLEMENTED` |
| SphereDOS Server runtime | `NOT IMPLEMENTED` |
| Provider execution | `NOT IMPLEMENTED` |
| Durable OAE persistence | `NOT IMPLEMENTED` |
| VS Code Extension Host目視試験 | `NOT TESTED` |

複数軸の現在地は[m.6xx.1 能力状態表](../../docs/status/m6xx-capability-matrix.ja.md)を正本とします。
`products/registry.json`は本ハーネスの実装状態と正本参照を持ちますが、結合済み、本番配布済み、
保守対象へ自動昇格しません。

## Command

Command Paletteから次を呼び出します。

- `SphereDOS Code: Cockpitを開く` (`spheredosCode.openCockpit`)
- `SphereDOS Code: prepared fixtureを表示`
- `SphereDOS Code: Kernel rejected fixtureを表示`
- `SphereDOS Code: provider auth required fixtureを表示`
- `SphereDOS Code: disconnected recoverable fixtureを表示`
- `SphereDOS Code: Cockpit fixtureを再読込`

Extension Development Hostで確認する場合は、このrepositoryをVS Codeで開き、
`products/spheredos-code`をextension development pathとして起動します。外部dependency、build、
provider login、network接続は不要です。今回の実行環境ではVS Code CLIを確認できなかったため、
Extension Hostでの目視結果は`NOT TESTED`です。

## Harnessの責務

- `fixtures/`の合成JSONだけを固定allowlistから読む
- Coordinate、World／Fold、Task／Lease、Kernel、Provider、OAE、Receipt、GUI transportを別sectionで表示する
- providerのauth／quota／refusal／opaque出力をchat回答へ変換しない
- Kernel rejectを成功色へ変換しない
- disconnectをabortまたは永続データ消失の確定へ変換しない
- missing fieldを`unknown`または`not provided`として表示する
- fixture由来の表示値をHTML escapeし、Webviewへnonce付きContent Security Policyを設定する

次の状態機械は互いの代用品ではありません。

```text
provider exit 0 != OAE commit
provider refusal != Mission failure
Issue close != Mission completion
GUI success display != Effect applied
detected != registered != approved != dispatchable
```

## 検証

```console
node --test products/spheredos-code/tests/*.test.js
```

`src/`はextension host、projection model、mock transport、Webviewを保持します。`tests/`はfixture contract、
負例projection、HTML escape、CSP、package contractを検査します。

## 非責務

production Kernel、daemon、scheduler、Cron、OAE永続化、GitHub API write、provider CLI実行・install・login・
token取得、課金・quota購入、model inference、GUIからのOAE commit／Issue close、Matchbox／Fold8G runtimeは
実装していません。Cockpitが表示した状態をEffect適用、durable state、製品完成の証拠へ昇格させません。
