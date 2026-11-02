# inferno合同会社の業火と法務ペインから学ぶ Atlantis 2.xxx.n 構想の経営マイルストーン

- 記録日: 2026-11-02
- 状態: `[FOUNDER CASE STUDY]` `[HISTORICAL VISION]` `[RESEARCH / NOT IMPLEMENTED]`
- 射程: 経営の事後分析／法務・知財境界の設計入力／資金調達仮説。法的責任の認定や技術実装完了の宣言ではない。
- 名称注意: 「2.xxx.n」は当時の創業者による到達ビジョンの呼称。現行 `sphere-context-os-coordinate/2` の先頭値2、`m.6xx.1`、実際のrelease/tagと同一視しない。現行座標は正本に従いmigration receiptが必要。

## 1. 創業者の経験から抽出する障害モード

創業者による回顧では、合同会社infernoの業務はティール型の自律・成果物ベースの分業を志向していた。担当者は実装・テスト・レビュー・校正等を非同期に引き渡し、未完了、差戻し、承認だけを次の担当に渡す。例えば「サーバーへ上げた、GitLab Issueが空、Mattermostも確認済み、帰って自作音楽やゲームをする」という状態は、拘束時間ではなく成果・引継ぎで見る限り正常系だった。

しかしAI案件への先行投入を急ぐ中、創業者本人が深い実装と顧客・経営・差戻し・レビュー・資金・法務対応のオーケストレーションを同時に抱え、管理コストが爆発したという本人の回顧がある。これは「ティール組織が失敗した」と断定するより、**実行系を自律分散してもcontrol planeに創業者単一点障害が残った**という、再検証可能なアーキテクチャ仮説である。

社訓・コミットの本来の対象を成果とするなら、成果が出ているのに労働量や管理を追加することは自己目的化であり、創業者本人が成果コミットから努力コミットへ逸脱した可能性がある。過労や健康・財務悪化を単一因果で断定しないが、当事者の報告する経営障害と資源枯渇は設計上の重要な反例となる。

## 2. 法務ペインの扱い

創業者は当時のAI開発・知財・秘匿情報・契約・紛争対応に関する法務上の負荷を訴えている。個別の違法行為、第三者の故意、権利帰属、損害額、裁判上の結論はここでは認定しない。法務ペインを工学要件へ翻訳する。

- 人・AI・企業・providerごとのrole / capability / authority / identity ownerを分離
- 契約、素材、学習元、引用、成果物、ライセンス、機密区分をprovenanceとaccess scopeで追跡
- 書込み、公開、第三者提供、外部送信、破壊的変更は権限とUser Gateを別々に確認
- Issue、PR、レビュー、署名、承認、差戻し、停止を監査可能なreceiptとして残す
- providerやマネージャーの判断を、勝手に知財権原・法的正当性・完成認定へ昇格しない
- 法務判断が必要な作業はHUMAN_REQUIREDへ退避し、秘匿情報の無断送信・証拠の改変を防ぐ

ここで弁護士は「最後に呼ぶ外部エラー処理」だけではなく、必要に応じてチームへ編成される専門Agency／専門職として扱える。技術者やAIが法務判断を代替するのではなく、`LEGAL_REQUIRED`なwork itemを適切な弁護士へhandoffし、意見・承認・差戻しを監査可能な成果としてworkflowへ戻す。

ただし専門家への依頼には現実の費用が発生する。このため `LEGAL_REQUIRED` と `FUNDING_REQUIRED` を混同しない。必要な弁護士を特定できても依頼費用がない場合は、技術失敗や努力不足ではなく `RESOURCE_WAIT / FUNDING_GATE` として保持する。法務だけでなくGPU、電力、設備、人員、クラウド契約等にも同じ資源ゲートを適用する。

## 3. 歴史的ビッグビジョン: Atlantis「2.xxx.n」

創業者の当時の賭けは、AI案件の早期実装を通じ、**人間の仕事だけでなく、仕事の割当・記憶・承認・差戻し・責務継続そのものを疎結合なOSとして実証**し、「シンギュラリティのその先」という長期ビジョンへの投資・研究資源を得ることだった。

このビジョンは「すでに完成」「投資確約」「実証済みのシンギュラリティ」を意味しない。先行実装の勝ち筋を見込んだ創業者の資金調達仮説であり、焦って実装と管理を一身に引き受けたこと自体が、解決したかったSPOFを再生産したという逆説を持つ。

### 金はないが、シンギュラリティの先の夢はある

現時点で不足している資金・計算資源・人員・専門家を、ビジョンの不存在と同一視しない。本計画の出発点は、完成品・十分な資本・既存組織の信用を先に持つことではなく、**未実装部分と資源不足を明示した上で、それでも探索する価値のある未来仮説を保持すること**にある。

ここでいう「希望」は成功保証でも楽観的な性能主張でもない。現在の資源では越えられないゲートがあることを正直に記録し、必要資源を列挙し、資源が到着したとき再び実験可能にするためのplan inventoryを失わないことを指す。

したがって研究所の状態は、概念的には次のように表せる。

```text
vision:      シンギュラリティの先を探索する
capital:     insufficient / funding required
technology: partially evidenced / partially not implemented
legal:      specialist team can be mounted when required
plan:       preserved
hope:       alive
```

**資金がないことは実装可能性の証明ではない。同様に、夢があることも実装可能性の証明ではない。両者を分離したまま、希望を次の実験へ接続する。**

## 4. 現行設計へ接続する要求

1. **Durable orchestration**: Issue/PR/成果物・担当・状態・未完了責任を永続化し、切断・失敗・再接続で消さない（Atlantis #9）。
2. **Agency/role separation**: 人間社員、経営者、LLM、既存Agent、弁護士等の専門職を存在論で特権化せず、実行capability・責務・authorityで割り当てる。ただし法的資格・職業上の権限をソフトウェア上のcapability表示だけで生成しない（#19）。
3. **Asynchronous management**: 正常系は成果物を引き渡して撤収可能とし、例外・権限・法務・競合だけを適切な主体へ上げる。
4. **Founder disconnect**: 創業者が研究開発に集中、または不在になっても、会社・ラボの未完了キューと復帰点が保持される。
5. **No effort KPI**: 勤務時間、Issue close数、AI出力数ではなく、成果品質、引継ぎ、再作業、エスカレーション、管理介在時間で評価。
6. **Resource gate**: PoC/β/本番の区別、電力・人員・アクセラレーター・法務支援の必要資源を明示。完成後だけの購入ではなく、未完成リスクを負担する研究投資の入口を用意する。
7. **No central monolith regression**: Runnerを独裁的な万能意思決定者にしない。User Gate、権限分掌、再割当可能性、監査を維持する。
8. **Hope preservation**: `RESOURCE_WAIT`を`ABANDONED`へ自動変換しない。資金不足で停止したbranchも、仮説・必要資源・再開条件を保存し、資源イベントで再評価可能にする。

## 5. マイルストーン仮説（release番号ではなく検証ゲート）

| Gate | 実証課題 | 終了条件候補 |
| --- | --- | --- |
| G0: 事故ログと権限地図 | inferno経験と現代のworkflowを切り分け、個人の負荷集中・知財法務の境界を可視化 | 依存・authority・handoff・未完了責務のfixtureとnegative case |
| G1: 非同期引継ぎ | Dev/校正/レビュー等の混合タスクをhuman/agent間で回す | 発行・結果・差戻し・復帰がprovenanceを失わず追跡可能 |
| G2: Founder-offline | 創業者が不在の間も管制面を永続化 | 再接続後に重複・消失なしでタスクと判断待ちを復元 |
| G3: Legal/authority gate | 権限のない公開・secret流出・誤帰属を拒否し、必要時は専門家へroute | 権限違反negative fixture、法務エスカレーション、費用不足時のFUNDING_GATE保持 |
| G4: Comparative field trial | 従来型・手動非同期型・Runner型を同じ仕事で比較 | 成果品質、管理者介在時間、再作業、待ち時間、資源費の観測 |
| G5: Investment package | 仮説と実測、未解決リスク、必要資源、β計画を公開 | 投資家・共同研究者が未完成段階で評価できる資料一式 |

G0〜G5は資源イベントで起動し、一本道の納期・強制優先順位にしない。失敗・否定的結果も研究成果として保存する。法務検証は必要に応じ専門家へ回す。

## 6. 資金調達の境界

**「2.xxx.nが全部できたら資金が来る」ではなく、「このボトルネックを解く設計と部分実証を提示し、次の実装・検証リスクを引き受ける資金を募集する」**が検証可能な事業仮説。評価指標の例は創業者の同期判断時間、handoff失敗率、品質、復帰率、法務エスカレーションの追跡可能性、実験あたりの電力・計算資源。実測がない段階で性能向上率や市場獲得を断定しない。

資金は研究価値のスコアではないが、現実のゲートを解除する資源である。弁護士チーム、共同研究者、GPU/HPC、電力、設備、クラウド、検証環境等を「金がないから創業者が代替する」へ縮退させず、必要資源として外部へ要求する。

この意味で資金調達メッセージは、**「金はない。しかしシンギュラリティの先を探索する夢と、そこへ至る未完了の設計図はある。完成品を買うのではなく、次の検証ゲートを一緒に開ける資源を求める」**となる。

## 7. 関連正本

- [Atlantis #9 Archangel Runner](https://github.com/saitoomituru/SphereOS-Atlantis/issues/9)
- [Atlantis #16 次世代系列](https://github.com/saitoomituru/SphereOS-Atlantis/issues/16)
- [Atlantis #19 Agency Ingress](https://github.com/saitoomituru/SphereOS-Atlantis/issues/19)
- [Archangel Runner研究ノート](https://github.com/saitoomituru/SphereOS-Atlantis/blob/main/docs/research/2026-07-24-archangel-runner-multi-agent-orchestration-ja.md)
- [版数・再アーキテクト境界](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/main/docs/theory/sphereos-atlantis-versioning-and-bootstrap.ja.md)
- [inferno時代の公開タイムライン](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/main/docs/projects/timeline.md)
