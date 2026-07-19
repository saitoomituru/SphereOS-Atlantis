# Experience Receipt運用

状態: `[ALPHA]`

Experience Receiptは、スピリチュアル実践者の「波動が合わない」「ずれる」、ゲーマーの
「面白くない」「クソゲーフラグ」、操作や認知上の違和感等を、即時に排除も仕様変更もせず受理する
repository-nativeなUX観測票です。語彙の学術的正当性を入口の審査条件にしません。

## 分離するもの

```text
raw experience signal   本人の表現を保つ
self-declared cluster   宗派、プレイスタイル等。AIは推定しない
hypothesis              原因候補。報告そのものではない
evidence                再現、集計、実験結果
disposition             review、実験、World分岐、仕様判断等
```

一件の報告から「実装バグ」「プレイが下手」「仕様変更」「多数派の総意」を自動確定しません。
同族というラベルも一枚岩にせず、RTA、TAS、縛り、効率、エンジョイ、ネタプレイ、宗派、実践流儀等を
本人申告clusterとして保持します。registryの例示は閉じたenumではありません。

## 作成

```bash
python3 -m atlantis_cli experience new \
  --summary '祈りUIで世界とのずれを感じる' \
  --signal '波動が合わない感じがする' \
  --self-cluster '律令神道の実践者' \
  --world 'shrine-world-prototype' \
  --request-cluster-review
```

正本は[`experience/registry.json`](../../experience/registry.json)、個別票は`experience/receipts/`です。
生成時は`received / single-report-unaggregated / pending`で、codeや仕様を変更しません。

## disposition

- 同じclusterまたは別clusterへ追加reviewを募る
- UX／情報子／データ工学上の実験を設計する
- WorldまたはPresentation Profileをsplitする
- 解決する
- 理由と再検討条件を添えてscope内の仕様と判断する
- 理由を添えて採用しない

`by-design-with-scope`は「仕様です」の一言では成立しません。主張scope、evidence、再検討triggerを
揃えます。仕様を決める自由と、体験報告の存在を消すことを分けます。

脆弱性、資格情報、個人情報を含む報告は公開Receiptにせず、非公開のsecurity連絡経路へ分けます。
