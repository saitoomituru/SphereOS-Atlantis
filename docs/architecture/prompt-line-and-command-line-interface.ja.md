# Prompt Line InterfaceとCommand Line Interface

状態: `[ALPHA CONTRACT]`

この契約は、自然言語でAtlantisへ意図・文脈・拘束を渡す操作面と、command／argumentで再現可能な
操作を指定する操作面を、真贋や優劣ではなく異なる適性として分離します。

## 用語

| machine ID | 表示名 | layer | 現在の例 |
|---|---|---|---|
| `prompt-line` | Prompt Line Interface（Atlantis PLI） | interaction surface | SaaS AI、Git connector、自然言語prompt |
| `command-line` | Command Line Interface（Atlantis CLI） | interaction surface | `python3 -B -m atlantis_cli ...` |
| `llm-mediated` | Large Language Model Interface（LLMI） | execution envelope | model、provider、connector、token budgetを含み得る媒介境界 |

`PLI`は人間向けのscoped aliasです。既存製品、PL/I、package、file extensionとの衝突を避けるため、
実行コマンド、package名、拡張子には使いません。機械可読IDは`prompt-line`です。

LLMIは利用者の操作面ではなく、PLIまたはCLIを媒介し得るdriver／Execution Envelopeです。
LLMを使っている事実だけから、現在の操作面、Actor role、persona、World、権限、実装状態を決めません。

## 適性は絶対境界ではない

| 操作面 | 主な適性 | 単独状態でのtrade-off | 補完方法 |
|---|---|---|---|
| Prompt Line Interface | D軸。Context Dimension、nD Fold、World、意味、目的、unknownを含む高抽象・低初期拘束の探索 | ピンポイントな高強度拘束が不足しやすい | Schema、tool、approval、fixture、test、receiptを束ねる |
| Command Line Interface | L軸。hardware、POSIX OS、runtime、library／SDK、Appへ届く再現可能な高強度拘束 | 未符号化の意味・目的探索を直接表現しにくい | DSL、script、設定、文書、PLI上の設計を入力する |

PLIもSchemaやtool callで強く拘束できます。CLIもDSLやscriptで高度な抽象構造を扱えます。したがって
「PLIは曖昧」「CLIは抽象を扱えない」を本質的な能力限界として固定しません。Prompt Engineeringと
Information Engineeringを、対象axisと必要拘束強度に応じて組み合わせます。

ここでいう`L`はAtlantis現行文書のhardwareからAppへ至る実装layer軸です。外部ISO規格の特定layerとの
同一性は制定されておらず、現時点では`unknown`です。

## 真贋軸を置かない

- PLIを「CLIを模した表示」「偽CLI」「Pythonを実行できない代用品」と説明しない
- CLIを「自然言語を理解できない下位interface」と説明しない
- 自然言語をprogramming languageの偽物、imitation、低精度版として扱わない
- interfaceからmerge権限、repository write権限、runtime実装済み、回答の正しさを推定しない
- connectorがhost上でPythonを実行できない場合は、そのconnectorのcapability境界として説明する

自然言語、形式言語、programming languageは射程と拘束方法が異なります。自然言語による学術・設計・
神学・法・物語・会話の営みや、それを処理するAI／hardware／model開発を、CLI実行可否の説明で
サイレントに格下げしません。

## 現在の操作面を表示する

local CLIから`help`を起動した場合、現在の操作面は`command-line`です。

```bash
python3 -B -m atlantis_cli help
python3 -B -m atlantis_cli interfaces
python3 -B -m atlantis_cli interfaces --id prompt-line --json
```

SaaS AIまたはGit connectorから自然言語で案内・設計・Note PRを行う場合は`prompt-line`です。ただし、
利用中のmodel、provider、Actor role、persona、World、権限は別fieldで確認します。将来のCompanion、NPC、
persona chatもprofileが異なるため、PLIという名前だけで同一化しません。

正本は[`help/interfaces.json`](../../help/interfaces.json)です。`atlantis interfaces`は正本を
読み取り専用で表示するだけで、PLI runner、model inference、standalone Atlantis runtimeを起動しません。

## 受入条件

- `prompt-line`にcommand名またはfile extensionがない
- PLI／CLIのprimary fitをD／Lとして表示しつつ、絶対能力境界にしない
- execution envelopeが操作面を自動選択しない
- interfaceがActor role、persona、World、権限、実装状態を推定しない
- `help`／`interfaces`がnetwork接続とrepository変更を行わない
- 真贋rankingを追加する変更をtestが拒否する

検証実装は[`atlantis_cli/help_mode.py`](../../atlantis_cli/help_mode.py)、negative testは
[`tests/test_help_mode.py`](../../tests/test_help_mode.py)に置きます。
