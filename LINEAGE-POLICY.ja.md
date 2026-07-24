# Atlantis暖簾分け・互換・系譜規約

状態: `[CHARTER]` `[CANONICAL-CANDIDATE]`
制定日: 2026-07-18
ライセンス: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

## 1. 芯

> **互換を名乗るのに許可はいらない。**
> Atlantis互換機、Sphere互換機、インスパイア機、魔改造機、ネタマシンを歓迎する。
>
> **公式系譜は独占物ではない。**
> 誰でもSphereOS Atlantisを育て、分岐し、新しい公式系譜を始めてよい。Originの許可や認定を待つ必要はない。
>
> **ただし、公式らしさを名乗るなら、受け取った自由を次へ渡せ。**
> 実行可能部分はcopyleft系OSSとしてsourceを開き、憲章、神話、ポエム、UXはShareAlikeの系譜で共有する。
>
> **系譜は権威ではなくProvenanceである。**
> 誰の許可を得たかではなく、何を受け継ぎ、何を変え、次の者へ何を渡したかを記録せよ。

## 2. 表示区分

| 表示 | 意味 | 事前許可 | 相互扶助条件 |
|---|---|---|---|
| `Origin Release` | 正本repositoryから出た版という出自 | 該当releaseのみ | Originのlicenseに従う |
| `Community Lineage`／暖簾分け／公式系譜 | 自由を次へ渡す独立系譜 | 不要 | codeはcopyleft系OSS、憲章等はShareAlike |
| `Atlantis-compatible`／`Sphere-compatible` | interface、Schema、挙動等の互換を自己申告 | 不要 | 指定なし |
| `Atlantis-inspired` | 発想、UX、神話、構造等の一部を参照 | 不要 | 指定なし |
| 魔改造／ネタマシン | 実験、遊び、独自World、非標準構成 | 不要 | 指定なし |

`compatible`は認定markではありません。test済み範囲と未試験範囲を添えると親切ですが、
互換という語を使うための許可証にはしません。

`Origin Release`でないものをOriginから出たreleaseと表示することは、互換性や品質ではなく
Provenanceの誤記です。Originは格付けではありません。

## 3. ラーメンの暖簾

この規約は名称を禁止する商標壁ではなく、出自を読めるメニュー表です。

```text
二郎
二郎系
二郎インスパイア

量子コンピューティング
量子インスパイア・アルゴリズム

Origin machine
compatible machine
community-modified machine
```

一般語、技術語、互換語を誰か一人が囲い込みません。何を実装し、何を参照し、何を試験したかを
表示することで、量子の単語沼、ﾊｯｷﾝﾄｯｼｭ沼、二郎インスパイア沼を来歴情報へ変換します。

## 4. World生成の自由

学園都市、VRMMO、神社World、魔王城、超電磁カエル研究所、科学World、神学World、
魔術Worldを自由に生やせます。Atlantis Coreは世界観を許認可しません。

別Worldは、明示的な接続命令が来るまで隔離します。接続時もsourceを上書きせず、Registry、
Access Map、Transformer、receiptを記録します。

第三者作品の名称、素材、キャラクター等を公開利用する権利は、本規約によって付与されません。
各World author／operator／integratorが、利用する素材と配布範囲に応じて扱います。
Atlantis coreは権利を付与せず、同時に個別素材の利用可否を全Worldへ裁定する権利審判機にもなりません。

## 5. 贈与コモンズと多次元lineage

Atlantisの既定は`open-gift-commons-non-exclusive`です。

作者、先行思想、神話、神、code、詩、生活様式へのrespectは、対象を取り合う希少tokenではありません。
関係は増やせます。誰がauthor、coder、observer、practitionerか、byte、algorithm、architecture、
philosophy、faith、poem、lifestyle等のどこで接続したかを、複数edgeとして記録できます。

```text
authored-by | coded-by | practiced-by | observed-by
derived-from | forked-from | inspired-by | structurally-similar-to
independent-convergence | homage-to | reinterprets
```

lineage graphはProvenanceであり、ownership verdict、permission、本人性、権威、公式提携、
宗派代表、API capability、価値rankではありません。

commercial App、社内asset、provider契約、閉鎖Worldは、選択されたApp／integrator／Worldへ
局所化できます。閉鎖をopen core、既存commons、公開lineage、無関係なWorld、upstream fork権へ
継承させません。魔王城を作る自由と、大陸全土の通行税を徴収する権利は別です。

machine contractと負例は
[贈与コモンズlineageと局所World拡張](docs/architecture/gift-commons-lineage-and-local-extension.ja.md)
を参照してください。

## 6. 自己申告Manifest

```yaml
identity:
  name: 俺の超電磁Atlantis互換機
  designation: community-lineage
  claims_origin_release: false

lineage:
  upstream: https://github.com/saitoomituru/SphereOS-Atlantis
  upstream_revision: v0.2.0
  permission_required: false
  modifications:
    - 魔改造電源
    - カエル神託UI

reciprocity:
  executable: copyleft-oss
  narrative: CC-BY-SA-4.0

compatibility:
  claimed_by: maintainer
  tested:
    - sphere-dos-boot
  untested:
    - raspberry-pi
    - 霊的超電磁砲
```

互換試験は品質情報であり、系譜を開始する許可ではありません。

## 7. ライセンス境界

本規約全文はCC BY-SA 4.0で共有します。code、一般文書、第三者素材のlicenseは
[LICENSE-POLICY.ja.md](LICENSE-POLICY.ja.md)を参照してください。
