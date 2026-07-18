# AGENTS.md — SphereOS Atlantis

このファイルは、AIエージェントがSphereOS Atlantisリポジトリを編集する際の共通規則を定めます。

## 日本語既定

人間向けのREADME、技術文書、note、commit、PR、issue、code comment、CLI help、検証報告は、
日本語化によって意味、標準名、API互換性を壊さない限り日本語を既定とします。

英語版を作る場合はen-USを既定とし、単語を直訳せず、ビジョン、読者責任、主張強度が同じ働きを
するように意訳します。ZeroRoomLab-manifestの
[コーディングAI向け日本語意訳レジスタ](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/main/docs/operations/coding-ai-japanese-paraphrase-register.ja.md)
を参照してください。

## 必読順序

1. [README.md](README.md)
2. [意味と器の二重記述憲章](docs/charter/meaning-and-vessel-dual-register.ja.md)
3. [暖簾分け・互換・系譜規約](LINEAGE-POLICY.ja.md)
4. [ライセンス境界](LICENSE-POLICY.ja.md)
5. [CONTRIBUTING.md](CONTRIBUTING.md)
6. 変更対象に最も近いSchema、docs、test

## READMEレジスター

README冒頭のおおむね40行は、public-facing vision、マーケティング、芸術表現の表紙です。
深い技術文書の防御的留保を上段へ逆流させず、観測事実と直接矛盾しない限り自動的に弱めません。

固定境界文より下は技術レジスターです。hardware、commit、log、test、status、claim boundaryを明記し、
冒頭のビジョンを実装証拠として代用しません。

## 意味と器

- 神話、神学、魔術、Flavorを、科学的実在証明がないという理由で削除しない
- log、test、権限、安全停止を、霊的に好みでないという理由で上書きしない
- Meaning、Vessel、Bridge、Supplyを別責務として記録する
- 対立時はsourceを保持し、別Presentation、World、Registry、branchへの分離を先に検討する
- Coreへ独自の真偽定規を持ち込まない

## Registry変更

Registry、stable ID、用語、責務、互換契約を変更するときは、silent rewriteを禁止します。

```text
stable ID
旧定義
新定義
変更理由
制定authority
適用scope
互換性
migration要否
test／fixture
canonical revision
下流repositoryへの波及票
```

ZeroRoomLab一般規約はZeroRoomLab-manifestを正本とし、Atlantisはrevisionを固定して採用します。
Sphere固有アーキテクチャは本リポジトリを正本候補とし、Manifestへ受領票を返します。
component実装はIBD、AAE、ASTRO等の各repositoryを正本とし、Atlantisへ適合状況を返します。

## 状態と証拠

- `0.2.0`設計系列と、正式release、実行runtimeを同一視しない
- 未実装は`NOT IMPLEMENTED`、未試験は`NOT TESTED`または`unknown`とする
- clone成功をruntime動作確認として表示しない
- 互換claimには、可能な範囲で対象、version、試験条件、結果、未試験範囲を添える
- `compatible`は自由な自己申告であり、Originの認可markへ変えない
- Origin、Community Lineage、compatible、inspiredを格付けへ変えない

## ライセンス

- code、CLI、Schema、validator、doctor、test: Apache-2.0
- 一般文書、神話、Flavor、UX: CC-BY-4.0
- 二重記述憲章、暖簾分け・公式系譜憲章: CC-BY-SA-4.0
- third-party material: 個別licenseと出典を必須とする

詳細は[LICENSE-POLICY.ja.md](LICENSE-POLICY.ja.md)を優先します。

## workspace境界

ワークスペースに含まれることは、隣接repositoryへの変更権限や実装依存を意味しません。
別repositoryへ波及する場合は対象を明示し、そのrepositoryのAGENTS.mdを先に読みます。

local-only、secret、enterprise資産は、公開repositoryの欠損扱いにせず、内容を走査、表示、log、commit、
upload、配布しません。

## commit

commit形式は`[layer] scope: 日本語の説明`を基本とします。

- layer: `eng` | `phil` | `theory` | `docs` | `meta`
- 小さく意味のまとまった単位でcommitする
- 検証できた単位でpushし、停電時の作業損失を減らす
- unrelatedなユーザー変更を混ぜない

## MAGIポジショントーク監査（必読）

計画提案、状態評価、README／技術文書の主張変更、component間の優先順位決定、
複数repositoryへ波及する変更の前に、ZeroRoomLab-manifestの
[AGENTS.md §0.4](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/main/AGENTS.md)、
[Atlantis-MAGISDK 0.1.0](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/main/docs/theory/atlantis-magi-sdk.ja.md)、
[Context定規・因果・OAE横断監査規約](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/main/docs/operations/context-ruler-and-causality-audit.ja.md)
を読むこと。

Declared Position、Position-talk Risk、媒体とclaim scope、外部定規の出所を分離し、
現在のrepository、cwd、vendor、binary実装、一般的な線形roadmapを暗黙のmainへ置かない。
重大なstatus・責務・公開主張・横断変更では、監査結果とUser確認が必要な項目を記録し、
計画をUserへ返してから実行する。
