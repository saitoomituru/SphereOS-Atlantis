# ブラウザ／SaaS AIからNote PRを送る

状態: `[ALPHA]`

この入口は、ローカルVS CodeやAtlantisのmerge権限を持たない参加者が、哲学、神学、信仰実践、
ゲーム体験、フレーバーテキスト、UX上の違和感、仮説を`note/`へ提案する正規ルートです。
コードを書けること、開発チームへ加入すること、merge権限を持つことを参加条件にしません。

## 必要なもの

1. GitHub等、提出先Forgeのアカウント
2. リポジトリをforkまたはbranchへ書ける権限
3. Git connectorを備えたSaaS AI、またはWeb editor

SaaS AIごとの接続手順、料金、対応Forge、権限表示は変わり得ます。手元のAIへ
「このリポジトリをforkし、Noteだけをbranchへcommitしてdraft pull requestを送る方法を教えて」
と尋ね、表示された権限と送信先を自分で確認してください。Atlantisは第三者AIの資格情報を預かりません。

## 最小ルート

```text
公開repositoryを読む
  -> forkまたは許可されたbranchを作る
  -> note/registry.jsonから棚と種別を選ぶ
  -> note templateで一件だけ作る
  -> 差分と公開範囲を本人が確認する
  -> draft pull requestを送る
  -> merge権限がなければ PR_SUBMITTED で完了
```

公開repositoryでは、maintainer権限を配らなくてもforkからpull requestを受け取れます。ただしForge、
組織、repositoryの設定によりforkやPRが制限される場合があります。参加者へmerge権限、secret、Actionsの
書込みtokenを要求しません。

## AIへ渡すprompt

```text
SphereOS AtlantisのAGENTS.md、note/AGENTS.md、note/README.ja.md、
note/registry.json、ZeroRoomLab-manifestのAGENTS.mdを先に読んでください。
「スフィア独鈷書」は走査も転記もしないでください。

私が自己申告した立場: <任意。未申告ならnot-declared>
主張する範囲: <このNoteが扱う範囲>
裁定しない範囲: <別宗派、別World、別作品、別専門領域>
棚: <registryにあるshelf id>
種別: <registryにあるkind>
題名: <題名>
本文素材: <ここへ自分の観測、違和感、ポエム、仮説を書く>

事実、解釈、仮説、内観を分離し、unknownを残してください。
既存ファイルを上書きせず、新しいnote一件だけを作ってください。
commit前に公開してよい情報だけか私へ確認し、forkのbranchへ日本語commitを作り、
draft pull requestを送ってください。mergeはしないでください。
```

会話memoryから宗派、病歴、所属、プレイスタイル等を勝手に補完させないでください。memory由来の記述を
公開する場合は、生成後の本文を本人が確認し、Note metadataを`memory_publication_consent: confirmed`へ
明示変更します。

## reviewの期待値

- ポエムや信仰実践のNoteへ、工学仕様と同じ実証要求を置かない
- 工学的成功、性能、安全性を、ポエムやフレーバーテキストだけで確定しない
- 「波動が合わない」「面白くない」等も体験報告として受理し、即時に仕様であるとして潰さない
- 採用、保留、World分岐、追加cluster review、scope外を区別する
- 通常の異論や不快感と、脆弱性・資格情報漏えいの非公開報告を混同しない

不具合や未対応環境はIssueへ報告できます。資源不足で実行できなかった場合も、`RESOURCE-WAIT`、
試した範囲、未実行範囲を書けば有効な引継ぎです。
