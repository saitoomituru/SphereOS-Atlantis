# 棚別の開発参入チュートリアル

状態: `[ALPHA]`

このチュートリアルは、参加者へ一つの語彙や存在論を先に強制せず、現在立っている棚から
SphereOS Atlantisの開発へ入るためのBridgeです。棚は専門分野の格付けではなく、異なる
Presentationから同じ開発対象へ着地する入口です。

## 入口を選ぶ

| いま使いやすい言葉 | 入口 | 最初に触る構造 |
|---|---|---|
| 霊、象徴、祈り、依代、顕現 | [スピリチュアル棚](spiritual.ja.md) | Meaning、World、Agency、OAE |
| 世界設定、PC／NPC、判定、セッション | [ゲーム・TRPG棚](gaming-trpg.ja.md) | World、Entity、Rule、Event |
| 要件、型、境界、試験、ログ | [工学棚](engineering.ja.md) | Schema、test、receipt、権限 |
| Q(ψ, ∇φ, λ)、FAM、情報子 | [情報子工学棚](infoton-engineering.ja.md) | Registry、FAM、変換、来歴 |
| D Fold、Access Map、SDK、OAE | [Sphere Architecture棚](sphere-architecture.ja.md) | Context Dimension、Bridge、component契約 |

複数の棚に当てはまる場合、一つへ決める必要はありません。最も説明しやすい入口から始め、
必要な時だけBridgeを渡ります。

## 全棚に共通する到達点

1. 自分の棚の言葉で、扱いたいWorld、対象、行為、制約を記述する
2. 現在のManifest、Registry、対象リポジトリの`AGENTS.md`を読む
3. Meaning、Vessel、Bridge、Supplyのどこへ貢献するかを選ぶ
4. 吊るしのVS CodeとGitからSphere-DOS開発環境を再構築する
5. 同じSchema、fixture、test、Git差分で変更を説明する
6. 未実装、未試験、不明を成功扱いせず、次の参加者へ兵站票を残す

チュートリアルを読んだAIエージェントも同じ順序を使います。会話記憶だけで説明せず、実行のたびに
現在のManifestと対象リポジトリを解決してから、参加者の棚に合わせて説明します。

## 混ぜないもの

- 神話や霊的表現を、工学的証明がないという理由で削らない
- 実装状態、性能、試験結果を、物語上の表現で上書きしない
- workspace membershipを実装依存とみなさない
- 別World、別Registry、別企業、秘密領域を暗黙に結合しない
- AIGやCLIが読んだ要約を、原文より上位の正本にしない

## 最初の貢献

コードを書かなくても開始できます。棚の例を一つ追加する、用語の対応が誤っている箇所を直す、
fixtureを作る、未試験環境を試す、UXや物語を改善することも有効な貢献です。

変更前にルートの[AGENTS.md](../../AGENTS.md)と[参加手順](../../CONTRIBUTING.md)を読んでください。
