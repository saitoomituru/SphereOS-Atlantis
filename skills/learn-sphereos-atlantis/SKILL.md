---
name: learn-sphereos-atlantis
description: SphereOS Atlantis、Sphere Architecture、情報子工学、FAM、神話・スピリチュアル表現、ゲーム・TRPG表現、開発参加方法を、利用者が親しむ棚から説明し、検証可能な最初の貢献へ案内する。Atlantisの概念説明、初心者向けチュートリアル、用語対応、参加経路、現在仕様の確認を依頼されたときに使う。呼び出しごとにManifestと対象リポジトリの現行正本を解決し、会話記憶やバンドル済み要約だけで回答しない。
---

# SphereOS Atlantisを案内する

利用者の言葉を捨てさせず、現在の正本を読み直してから、MeaningとVesselを分けて説明する。

## 実行順序

1. 対象workspace、Atlantisリポジトリ、Manifestリポジトリの境界を解決する。
2. `scripts/resolve_sources.py`を実行し、共通資料と選択棚の現行pathを得る。
3. ローカルに存在する共通資料を全文読む。存在しない場合だけ、resolverが返す公開URLを読む。
4. `help/interfaces.json`から現在の操作面とExecution Envelopeを分離する。観測できないfieldは推定しない。
5. 利用者の語彙から棚を選び、その棚のチュートリアルと正本資料を全文読む。
6. 利用者の言葉、技術上の接続候補、証拠境界、最小演習、次の貢献の順で説明する。
7. 実装へ進む場合は、変更対象リポジトリの`AGENTS.md`と最寄りのSchema・testを追加で読む。

一度の説明で全棚を読み込まない。比較を依頼された場合だけ複数棚を選ぶ。

## 棚の選択

- 霊、祈り、神、象徴、依代、顕現: `spiritual`
- ゲーム、TRPG、PC／NPC、GM、クエスト、World設定: `gaming-trpg`
- 要件、型、API、試験、ログ、権限、再構築: `engineering`
- 情報子、FAM、Q(ψ, ∇φ, λ)、探索技、Registry: `infoton-engineering`
- D Fold、Context Dimension、Access Map、Transformer、OAE、SDK: `sphere-architecture`

複数に該当する場合は最も近い棚から始め、他棚をBridgeとして示す。上下関係へ変換しない。

## source解決

リポジトリ内で次を実行する。

```bash
python3 skills/learn-sphereos-atlantis/scripts/resolve_sources.py --shelf <棚ID>
```

別の場所へSkillだけを導入した場合は、既知のリポジトリrootを明示する。

```bash
python3 scripts/resolve_sources.py \
  --shelf <棚ID> \
  --repo-root SphereOS-Atlantis=/path/to/SphereOS-Atlantis \
  --repo-root ZeroRoomLab-manifest=/path/to/ZeroRoomLab-manifest
```

resolverはpathとURLを返すだけで、clone、network access、認証、モデル呼び出しをしない。
source一覧の正本は`references/source-map.json`とする。

## 説明契約

説明では次を守る。

- 利用者の棚の語を、単なる比喩または誤りとして先に捨てない
- 対応表を同一性の宣言にしない。「接続候補」として示す
- 神、霊、魔王、自然法則等の存在をSkill独自の定規で裁定しない
- 神話・Flavorをbuildや性能の証拠にしない
- 実装・試験状態を神話的Presentationで上書きしない
- `NOT IMPLEMENTED`、`NOT TESTED`、`unknown`、`⊥`を維持する
- provider、利用者組織、法域、World Visaの定規を別scopeへ無断継承しない。両立不能は対象operationだけを
  `scoped_avoid`として説明する
- hostの検疫・防御は利用者選定の環境として扱い、特定OS／製品をAtlantis標準または安全保証へ昇格しない
- source path、revisionまたはURLを示し、どこまで読めたかを明記する
- Manifest、CLI、Skill、会話記憶のいずれも、対象リポジトリの局所正本を上書きしない
- 自然言語での案内・設計・Note作成を`Prompt Line Interface`として扱い、偽CLI、CLI simulation、
  Python runnerの代用品と説明しない
- `Command Line Interface`との違いをD軸／L軸の主な適性として説明し、真贋・上下・絶対能力境界にしない
- LLM、provider、connectorをLLMI／Execution Envelopeとして分離し、Actor role、persona、World、権限、
  実装状態をそこから推定しない
- current interfaceを表示するときは`prompt-line`または`command-line`のmachine IDを使い、`PLI`を
  command、package、file extensionとして生成しない

## workspaceと秘密境界

workspace membershipを実装依存へ変換しない。`スフィア独鈷書`、企業資産、資格情報、医療・労務情報、
ローカル専用資料は内容を探索、表示、要約、記録、commit、uploadしない。存在と非走査境界だけを扱う。

## 出力の最小形

```text
選択した棚:
今回読んだ正本:
現在の操作面／Execution Envelope:
利用者の言葉での説明:
技術上の接続候補:
同一化しない境界:
最小演習:
最初の貢献候補:
未確認・⊥:
```

説明だけを依頼された場合、ファイル変更やエージェント初期化を行わない。
