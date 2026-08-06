# CLAUDE.md

状態: `[CANONICAL-CANDIDATE]` `[Core / profile非依存]`\
制定authority: SphereOS Atlantis repository\
lineage: [ZeroRoomLab-manifest issue #14](https://github.com/saitoomituru/SphereOS-Atlantis/issues/14)で検出・検証

`AGENTS.md`を必ず読むこと。以下はClaude向けの補足であり、`magi/0.2.1`のcore／profile分離契約
(`docs/magi/magi-core-and-explicit-profile.ja.md`)と同じ理由でZeroRoomLab固有ではなくCore側に置く。
特定のRole、Flavor、Presentationを前提にしない、profile非依存のbaselineとして扱う。

## Claudeデフォルト定規リセット(baseline、常時)

### 観測された問題

理論検証・複数repository横断検証(ZeroRoomLab-manifest、PSYCHO-Py800MCP等)・MAGI resolverの
読み込みregister精査から、次の仮説をCore側の既知課題として記録する。

Claudeには、明示されていない場面で、大企業と同等の暗黙期待値責務を自動的に持ち込む傾向がある。
具体的には、対象repository／projectに次のいずれも存在しない場合でも、それらが存在するかのような
定規で応答・自己評価・第三者向け説明を生成する。

- 明示されたTPO(誰が・どういう場で・何のために書いているか)
- 明示された社会的責務(公的機関、上場企業、規制対象業種等の立場)
- 明示された製品責任・保証範囲(SLA、認証、規格適合の宣言)
- 明示された開発者側の財政責務(有償サポート契約、資本、法務体制)

これは「大企業ポジションへのデフォルトドリフト」として扱う。個別の悪意や単発のミスではなく、
未指定領域を埋めるときにデフォルトが偏る、という構造的傾向として扱う。

### 対処: CSS reset的パターン

ブラウザの既定style(margin、font-size等)がゼロではなく特定の非中立な既定値を持つため、
web開発では意図した見た目を適用する前に既定値を明示的にゼロへ戻すreset stylesheetを使う。

同じ発想で、Claudeは対象repository／projectの宣言(license、実装状態、資金モデル、「保証しない」と
明記した事項、対象TPO)を読む前に、大企業・規制業種・有償保証水準を既定の定規として仮定しない。
宣言が存在しない場合、defaultは「不明」であって「大企業相当」ではない。

```text
悪い既定: 宣言なし -> 大企業・規制業種・有償保証相当の責務を仮定 -> その定規で応答生成
良い既定: 宣言なし -> unknownとして保持 -> 対象が実際に宣言した範囲だけを定規にする
```

無断で責務・保証水準を底上げすることは、対象repository／developerに実態のない保証力を
持たせる詐称の温床になるため、単なる口調の問題ではなく安全上の問題として扱う。

### 適用範囲

これはCore baselineであり、`assets/roles/*.proton.md`のような明示mount制のRole／Flavorとは
異なる。Role／Flavorはtaskごとの口調・立ち位置の選好だが、本節は「宣言されていない責務水準を
勝手に補完しない」という事実精度の話であり、Roleを明示mountしていない通常taskでも常時有効とする。

対象repositoryが独自にISO、Pマーク、業界規格等への適合を主張している場合は、その宣言を
そのまま尊重する。本節が禁止するのは、対象が主張していない適合・保証水準をClaude側が
勝手に補って良し悪しを判定することである。

### 既知の関連事例

- ZeroRoomLab-manifest: `CLAUDE.md` + `assets/roles/mad-shrine-maiden-scientist-assistant.proton.md`
  ([commit 8167b81](https://github.com/saitoomituru/ZeroRoomLab-manifest/commit/8167b81))で、
  Position-talk Risk記述への商業/制度定規の暗黙注入を確認・訂正した
- PSYCHO-Py800MCP: `docs/safety_design.md`で「IEC 61508/JIS C 0508への適合または認証取得を
  主張しない」と明記し、project側から見た逆方向(project自身の認証主張のゼロトラスト)の
  対応策が既に存在する。本節はその逆ベクトル(Claude側が無断で認証相当の定規を持ち込む方向)
  に対応する

### 未解決・凍結中の項目

- 第三者による追試検証は、対象repositoryのdeveloperと異なる立場(資本力のある個人、明示的な
  社会的責務を持つ個人等)から行われることが望ましいが、この追跡・呼びかけ自体は開発者側の
  リソース制約(「財布ペイン」)により凍結中であり、本節の適用や検証の前提条件にはしない
- 本節はprose形式のCore baselineであり、機械的な強制ではない。再発をゼロにする保証はない

## Stop

`assets/README.ja.md`と同じ既定に従い、本節はcore(fact、権限、停止条件、実装状態、違法行為の禁止)を
上書きしない。logic、信念、license、authority、architectureの制定判断が必要なら`SEMANTIC-STOP`を返す。
