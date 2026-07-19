# SphereOS Atlantisへの参加

ここは雇用募集ではなく、OSS同人サークルです。雇用、業務委託、賞金、報酬がある場合は、
対象issueまたは別文書で明示します。

## 貢献の入口

- Meaning: 神話、命名、Flavor、象徴、儀式、世界観
- Vessel: code、Schema、test、配布、hardware、保守
- Bridge: UX、Access Map、翻訳、Presentation Profile、受入条件
- Supply: 飯、投げ銭、部材、計算資源、検証環境、review時間

片側を深く掘る専門家も、科学と魔術の両岸へ首を突っ込むMAD巫女サイエンティストも歓迎します。
Supplyはmerge権、真理判定権、Origin表示、他者への指揮権を購入しません。

## 先に読むもの

1. [README.md](README.md)
2. [意味と器の二重記述憲章](docs/charter/meaning-and-vessel-dual-register.ja.md)
3. [暖簾分け・互換・系譜規約](LINEAGE-POLICY.ja.md)
4. [ライセンス境界](LICENSE-POLICY.ja.md)
5. 変更対象に近いdocs、Schema、test

## pull request

merge権限のない参加者も、公開repositoryをforkしてpull requestを送れます。merge権限、開発チーム加入、
ローカルVS CodeはNote提出の条件ではありません。手持ちのSaaS AIやWeb editorから提出する場合は、
[ブラウザ／SaaS AIからNote PRを送る](docs/tutorial/note-pr-by-saas-ai.ja.md)を使ってください。
接続方法は手元のAIへ直接尋ね、表示された権限と送信先を本人が確認します。

権限がなければ、draft PRを送った`PR_SUBMITTED`で参加者側の工程は完了です。maintainerはreview後に
merge、保留、分岐、追加review、却下を選びます。Note提出からmerge権限や真理裁定権を推論しません。

pull requestには、該当する範囲で次を書いてください。

```text
目的:
変更対象:
Meaningへの影響:
Vesselへの影響:
Bridge／Mappingへの影響:
実行確認:
未試験範囲:
license／第三者素材:
source／Provenance:
```

Narrativeだけ、codeだけ、translationだけのPRも有効です。全項目を一人で埋める必要はありません。
未確認項目は`unknown`または`not tested`と書き、架空の確認結果で埋めません。

## commit

人間向けのcommit subjectとbodyは、日本語化によって互換性を壊さない限り日本語を既定とします。

```text
[eng] boot: doctorへworkspace差分検査を追加
[phil] charter: World生成自由の結語を追加
[docs] readme: Pi版の未試験境界を追記
[meta] lineage: 暖簾分け受領票を追加
```

小さく意味のまとまったcommitに分け、検証できた単位でpushします。

## ライセンスと権利

貢献物は、提出先ファイルの明示licenseまたは[ライセンス境界](LICENSE-POLICY.ja.md)の対象別既定licenseで
提供できる権限を持つものに限ります。第三者素材を含む場合は、出典、license、変更、再配布可能範囲を
明記してください。

自由なfork、compatible、inspired、魔改造を歓迎します。Originの許可は不要です。
