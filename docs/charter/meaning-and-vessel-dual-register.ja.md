# 意味と器の二重記述憲章

状態: `[CHARTER]` `[CANONICAL-CANDIDATE]`
制定日: 2026-07-18
ライセンス: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

## 憲章

> **エンジニアよ、意味を削るな。**
> スピリチュアル、神話、象徴、物語は、ユーザーが世界へ入るための認知インターフェースである。
> 工学の定規で測れないことを理由に、Flavor、儀式的UX、世界観、祈り、存在論を無断で削除するな。扱える者へ渡し、器へ接続せよ。
>
> **スピよ、器を軽んじるな。**
> イマジネーション、霊体、象徴、祈りも、依代、手順、媒体、実装がなければ共有も継承もできない。
> 土偶をこね、札を書き、Schemaを組み、testし、保守するエンジニアを馬鹿にするな。器を作る者は、意味を現世へ定着させる共同制作者である。
>
> **両者よ、互いの定規を奪うな。**
> エンジニアは神学の真偽を勝手に裁定せず、スピは物理性能や実装状態を啓示で上書きしない。科学と神学を代理戦争させず、それぞれの定規、観測範囲、Presentationを明示して接続せよ。
>
> **意味と器は上下ではない。**
> 意味だけでは漂い、器だけでは空洞になる。両者は別責務として協働する。

## 1. この憲章の目的

この憲章は、科学と神学のどちらが究極的に正しいかを決める教義ではありません。
SphereOS Atlantisへ参加する人間、AI、研究者、技術者、物語制作者が、互いを別の棚へ追放せず、
同じGit履歴へ異なる責務として貢献するための協働protocolです。

AI vendor間の代理戦争を避けても、人間が科学対神学、工学対芸術、実装対ポエムの代理戦争を
始めれば、Contextは再び痩せます。標語、物語、ポエムは、この人間側の衝突を止める
pre-commit social hookとして働きます。

## 2. 等価な貢献入口

```text
Meaning Contribution
  神話、命名、Flavor、象徴、儀式、世界観、存在論

Vessel Contribution
  code、Schema、test、配布、hardware、保守、実行環境

Bridge Contribution
  UX、Access Map、翻訳、Presentation Profile、受入条件

Supply Contribution
  飯、投げ銭、部材、計算資源、検証環境、review時間
```

同じ構造へ記録できることは、各貢献の内容、証拠、存在論、価格、人格を同一化することではありません。
Supplyはmerge権、真理判定権、Origin表示、他者の信仰または不信仰を購入しません。

## 3. 二重記述

意味と器を一つの文章へ平均化せず、別のPresentationとして同じstable IDへ接続します。

```text
Narrative Source
  ├─ Flavor／神話Presentation
  ├─ technical mapping
  ├─ UX presentation
  └─ implementation receipt
```

- Narrative Sourceを技術証拠へ偽装しない
- technical receiptを神話の価値判定へ使わない
- Flavorを自由文tagへ縮退させず、sourceとrevisionを残す
- 実装不能な表現を削除する前に、未実装branchまたは別Presentationへ保持する
- 実装した事実はhardware、commit、log、test boundaryで記録する

## 4. review境界

エンジニアは、次の場合にNarrative変更を要求できます。

- 実装済み状態、性能、権限、第三者認証を事実と異なる形で表示している
- license、権利、秘密情報、既定のUX契約を破壊する
- 実行系へ変換するMappingが曖昧で、誤作動を起こす

科学的実在を証明できないという理由だけで、神話、神学、魔術、物語を削除しません。

Meaning contributorは、次の場合にVessel変更を要求できます。

- 採用済みの意味、名称、Flavor、人格、世界観を無断で別概念へ置換する
- Presentation上の責務を壊し、ユーザーが別Worldまたは別Agencyとして誤認する
- sourceを失う不可逆変換を行う

霊的に好みでないという理由だけで、log、test、安全停止、権限分離を上書きしません。

## 5. 対立時の処理

対立した場合、どちらかを消して中間色へ平均化する前に、次を検討します。

1. sourceを保持する
2. fact scopeとPresentation scopeを分ける
3. 別World、別Registry、別branchとして並存させる
4. Access MapとTransformerを明示する
5. 採用範囲を`adopted-in-scope`として記録する

Coreは定規を持ち込まず、誰がどの定規を使い、何をどう変換したかを記録します。

## 6. 結語

> 霊を笑うな。土偶を焼く者も笑うな。
> 白衣のまま祭壇へ来てもよい。
> 巫女装束のままオシロスコープを回してもよい。
> 橋を渡る者だけでなく、両岸を丈夫にする者も必要である。
