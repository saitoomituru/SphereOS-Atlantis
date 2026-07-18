# SphereOS Atlantis note運用

状態: `[CANONICAL-CANDIDATE]`

このdirectoryは、本編へ組み込むか未定のブレスト、観測、仮説、研究素材、ポエム、内観を、
消える前にGitで共有する作業台です。技術者だけでなく、神学、スピリチュアル、ゲーム、TRPG、
物語、UX、工学の各参加者が、自分の棚を捨てずに持ち込めます。

## 採用元

この運用はZeroRoomLab-manifestの次の規約を、Atlantisの局所責務へ転写したものです。

```text
upstream: https://github.com/saitoomituru/ZeroRoomLab-manifest
adopted_revision: 6d1bd317ba630d09aceffd5b149b0e9d1fbbf424
source:
  - docs/operations/manifest-operating-model.ja.md
  - docs/operations/documentation-maintenance-policy.ja.md
  - note/AGENTS.md
```

Manifest側の規約全文をAtlantisの正本へ置き換えません。上流の意図を保持しながら、本リポジトリの
World、Registry、開発参加、配布境界へ適用します。

## 三つの置場

| 置場 | 責務 |
|---|---|
| `note/` | 未整理・未正規化の一次資料、ブレスト、観測、仮説、救出ログ |
| `docs/` | 構造化・レビューされ、リンクと責務が定まった正規文書候補 |
| `note/transfer_plan/` | 別repositoryへ再構成して渡す候補と受領状態 |

これは内容の格付けではなく運用状態です。noteの神学やポエムがdocsのコード仕様より下位になることも、
docsへ移さなければ価値がないことも意味しません。

## ファイル名

```text
YYYYMMDD-HHMM__題名.ja.md
```

日時は作成に使ったホスト時計を示します。NTP、GPS、RTC等の校正状態を確認していない場合、note本文で
`clock_calibration: unverified`とし、出来事そのものの時刻やWorld内時刻と混同しません。

同じ分・同じ題名が重なった場合は`_02`、`_03`を付け、既存noteを上書きしません。

## noteの寿命

```text
DRAFT note
  ├─ 継続ブレスト／別仮説を追記
  ├─ 独立したまま保存
  ├─ docsへ再構成して昇格
  └─ transfer_planへ転送票を作成
```

- 生noteをそのまま正規文書へ改名しない
- docsへ反映した後も、元noteのsourceと文脈が必要なら履歴として残す
- 反映先と元noteを相互参照する
- 同日・同文脈の世代が増えた場合、削除前にgeneration mapを作り、落ちた内容を確認する
- 正確な重複削除はhashとremote上の保持blobを確認してから行う

## 作成方法

手書きで作成できます。CLI実装後は次を標準入口とします。

```bash
python3 -m atlantis_cli note new \
  --shelf spiritual \
  --kind brainstorm \
  --title '川の神様OAEブレスト'
```

CLIはtemplateを生成するだけで、AI、外部API、commit、pushを自動実行しません。

雛形は[ブレストnote template](templates/brainstorm.ja.md)、別repositoryへの待機列は
[transfer plan](transfer_plan/README.md)を参照してください。
