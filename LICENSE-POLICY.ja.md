# SphereOS Atlantis ライセンス境界

状態: `[CANONICAL-CANDIDATE]`  
制定日: 2026-07-18  
対象: 本リポジトリのコード、Schema、文書、神話、UX、憲章、貢献物

## 1. 結論

SphereOS Atlantisは、一つのライセンスでコード、神話、UX、憲章を平板化しません。
対象物の働きに応じて、次のライセンスを適用します。

| 対象 | 既定ライセンス | SPDX識別子 |
|---|---|---|
| source code、CLI、script、validator、doctor、test | Apache License 2.0 | `Apache-2.0` |
| JSON Schema、machine-readable manifest、設定template | Apache License 2.0 | `Apache-2.0` |
| 一般文書、ふさもふ神話、Flavor、UX、画像・音声等の別途指定素材 | CC BY 4.0 | `CC-BY-4.0` |
| 意味と器の二重記述憲章、暖簾分け憲章、公式系譜憲章 | CC BY-SA 4.0 | `CC-BY-SA-4.0` |
| 第三者素材 | 各権利者の指定 | 個別表示 |

ルートの[LICENSE](LICENSE)は、software部分へ適用するApache License 2.0の全文です。
明示的にCCライセンスを指定した文書・素材へ、ルートLICENSEを上書き適用しません。

## 2. Apache License 2.0の範囲

コードと実行可能な構成要素はApache License 2.0で配布します。

- 利用、改変、再配布、商用利用を許可する
- 改変ファイルでは変更を明示する
- 適用されるcopyright、patent、trademark、attribution noticeを保持する
- `NOTICE`を含む配布物では、必要なattribution noticeを保持する
- Apache-2.0はcopyleftではなく、派生物へ同一ライセンスを一律強制しない

公式系譜を名乗るcommunity distributionがcopyleftを採用する場合も、取り込んだ
Apache-2.0部分のLICENSE、NOTICE、必要な表示を消しません。採用するcopyleft licenseとの
互換性は、各distributionが配布前に確認します。

## 3. CC BY 4.0の範囲

一般文書、神話、Flavor、UX等は、個別指定がない限りCC BY 4.0を使用します。

再利用者は、合理的な方法で次を示します。

- 原作者または指定されたattribution主体
- 作品名または対象material
- CC BY 4.0へのリンク
- 変更した場合は、その事実
- Originまたは作者が利用者を推薦・公認したと誤認させない表示

## 4. CC BY-SA 4.0の範囲

次の文書はCC BY-SA 4.0を正本ライセンスとします。

- `docs/charter/meaning-and-vessel-dual-register.ja.md`
- `LINEAGE-POLICY.ja.md`内の憲章本文
- ファイル内でCC BY-SA 4.0を明示した派生憲章

これらを翻案して公開する場合は、CC BY-SA 4.0または同ライセンスが認める互換条件で共有します。
単なる参照、独立した発想、互換機という名称の使用へShareAlikeを拡張しません。

README.mdは複合文書です。通常部分はCC BY 4.0とし、次の文章を含む憲章抜粋は
CC BY-SA 4.0とします。

- 「エンジニアよ、意味を削るな。」から始まる段落
- 「スピよ、器を軽んじるな。」から始まる段落
- 「意味だけでは漂い、器だけでは空洞になります。」から続く結語

## 5. 互換・インスパイア・系譜とライセンス

`Atlantis互換`、`Sphere互換`、`Atlantis-inspired`、魔改造、ネタマシンという表示は自由です。
これらの語を使うために、copyleftまたはShareAlikeを要求しません。

一方、`Community Lineage`、暖簾分け、公式系譜を自称するdistributionは、受け取った自由を
次へ渡す意思表示として、実行可能部分にcopyleft系OSS license、憲章・神話・UXに
CC BY-SA系licenseを採用します。これはOriginによる許可制ではなく、系譜側の継承責任です。

`Origin Release`は正本repositoryから出たというProvenanceであり、互換機より偉いという格付けではありません。

## 6. 貢献物

pull request、patch、issue添付等として意図的に提出された貢献物は、提出先ファイルに明示された
ライセンス、または本規約の対象別既定ライセンスで提供できる権限を、提出者が持つものとして扱います。

第三者のコード、文章、画像、音声、キャラクター、商標等を含める場合は、出典、license、変更、
再配布可能範囲を明示してください。権限を確認できない素材は、公開配布物へ取り込みません。

## 7. ライセンス索引

- Apache License 2.0: <https://www.apache.org/licenses/LICENSE-2.0>
- CC BY 4.0: <https://creativecommons.org/licenses/by/4.0/>
- CC BY-SA 4.0: <https://creativecommons.org/licenses/by-sa/4.0/>
- 詳細索引: [LICENSES/README.md](LICENSES/README.md)

この文書はリポジトリ内の適用範囲を示す運用正本候補です。個別ファイルの明示指定、第三者license、
適用法令上の例外・制限を上書きするものではありません。
