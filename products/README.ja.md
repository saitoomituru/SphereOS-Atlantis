# 6xx product family

`products/`は共通packagesを異なるPresentation／Hostへ束ねる製品棚です。

| product | 主な操作面 | 現在地 |
|---|---|---|
| `spheredos-server` | Bash／CLI／CI／常駐処理候補 | 棚と責務境界のみ。本番運用サーバーは未実装・未提供 |
| `spheredos-code` | VS CodeコックピットGUI候補 | 試験ハーネス実装済み。Kernel・receiptとの縦結合試験前 |

実装、結合、検証、配布物化、公開範囲、保守責任は
[m.6xx.1 能力状態表](../docs/status/m6xx-capability-matrix.ja.md)を正本として別軸で確認します。

一般業務向けOpen Inspector、生活支援向けPostPet、third-party Presentationはここへ将来追加できます。
SphereDOS二製品だけを6xx系列の全体へ固定しません。
