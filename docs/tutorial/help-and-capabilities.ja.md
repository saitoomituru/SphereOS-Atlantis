# Helpモードと能力案内

状態: `[ALPHA]`

Helpモードは、初めてrepositoryを開いた人やAIが、所有者と同じ背景知識を持つと仮定せずに
「いま何ができるか」「何が未実装か」「次にどの入口を選べるか」を確認する読み取り専用の入口です。

## 安全な既定値

```text
proficiency = unknown
intent = look-around
route = help
identity inferred = false
permissions granted = false
mutation = false
network access = false
```

巫女、神学者、ゲーマー、サーバーレスエンジニア等のpersonaは、本人が説明を受けるときの
Presentationを選ぶ自己申告です。習熟度、実装意図、権限、教義、プレイスタイルを意味しません。
AIはpersona、会話memory、Gitアカウントから、それらを補完しません。

## 開始する

```bash
python3 -B -m atlantis_cli help
python3 -B -m atlantis_cli help --persona '巫女'
python3 -B -m atlantis_cli help --persona 'サーバーレスエンジニア' --json
python3 -B -m atlantis_cli capabilities --state AVAILABLE-NOW
python3 -B -m atlantis_cli capabilities --state NOT-IMPLEMENTED
```

実装経路は本人が`intent=implement`を選んだ場合だけ計画されます。この指定もcode変更、branch作成、
network接続、権限付与を自動実行しません。

```bash
python3 -B -m atlantis_cli tutorial start \
  --persona 'サーバーレスエンジニア' \
  --proficiency contributor \
  --intent implement
```

## 能力状態

| 状態 | 意味 |
|---|---|
| `AVAILABLE-NOW` | 実装と検証証拠があり、現在使える |
| `SCAFFOLDED` | 開発足場はあるが、完成runtimeではない |
| `NOT-IMPLEMENTED` | 契約、物語、Questまたはfixtureはあっても実装されていない |
| `NOT-TESTED` | 実行可能性はあるが、対象環境で完走確認していない |
| `RESOURCE-WAIT` | 火力、機材、予算または参加者を待っている |
| `UNKNOWN` | 現行証拠から状態を決められない |

この状態は[`help/capabilities.json`](../../help/capabilities.json)を正本とし、物語上の配信済みQuestと
原案、validatorとruntime、Codespacesの観測と完走を混同しません。`UNKNOWN`は成功へ丸めません。

## 次の入口

Helpは、地図、実装済み能力、未実装Quest、Note PR、Experience Receipt、環境診断、明示的な実装経路を
選択肢として返します。どの入口を選んでも、対象のManifest、`AGENTS.md`、source mapを読まずに
hardcodeされた要約だけで進めてはいけません。

- codeを書かずに原案を送る: [ブラウザ／SaaS AIからNote PRを送る](note-pr-by-saas-ai.ja.md)
- 違和感や面白くなさを送る: [Experience Receipt](../operations/experience-receipts.ja.md)
- 実装とQuestを区別する: [Forge MapとQuest Map](../status/forge-and-quest-map.ja.md)
- 開発環境を診断する: `python3 -B -m atlantis_cli doctor --json`

Helpは説明の入口であり、宗派間、World間、ゲーム間、専門分野間の裁定者ではありません。
