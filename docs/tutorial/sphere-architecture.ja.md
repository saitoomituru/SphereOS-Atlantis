# Sphere Architecture棚から入る

状態: `[ALPHA]`

この棚では、技術的な上下関係`L`と、等価なContext軸を束ねる`D Fold`を分離します。
Context Dimension OSが管理するのはCPUレジスタやメモリそのものではなく、Registry、World、Fold、
Access Map、Transformer、OAE等の意味境界です。

## 最初に分けるもの

| 軸・資源 | 責務 |
|---|---|
| `L` | runtime、protocol、application等の技術的上下関係 |
| `D`／Fold | 等価に束ねるContext軸の数と境界 |
| Registry | 軸、分類器、stable ID、authority、revision |
| Access Map | Fold間で何へアクセスできるかという定義 |
| Transformer | 実際に表現・型・Contextを変換するAgency |
| OAE | 誰がどの観測範囲で起こしたEffectとして記録したか |

## 最小演習

一つの越境を次の形で書きます。

```text
source FoldとRegistry revision:
destination FoldとRegistry revision:
Access Map:
Transformer Agency:
input／output contract:
発生したOAE:
sourceを保持する方法:
変換不能時の⊥:
```

POSIX比喩は管理責務を理解する補助であり、Context資源をデジタル資源そのものと同一化しません。
記述できたら[共通到達点](README.ja.md#全棚に共通する到達点)へ進みます。
