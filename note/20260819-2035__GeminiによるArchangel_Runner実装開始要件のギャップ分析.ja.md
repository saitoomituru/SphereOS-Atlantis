# GeminiによるArchangel Runner実装開始要件のギャップ分析

状態: `[DRAFT]`

観測時刻: `2026-08-19T20:35:00+09:00`  
clock calibration: `verified`  
Execution Envelope: `Gemini CLI (v1.x) on Darwin/macOS`  
対象: `CORN-0003` / GitHub Issue #9 `[Research] Archangel Runner` の実装開始に必要な要件とギャップの検証  

---

## 1. `[FACT]` (Issue #9のアーキテクチャ要件)

GitHub Issue #9 において提示された **Archangel Runner**（durable task state / orchestration layer）の仕様とフェーズ定義は次の通りである。

- **目的:** 異種協働マルチエージェント環境における、タスク/状態/競合管理の自動化、および人間（齋藤みつる氏）の調整負荷の削減。
- **構成:** Runner Core (Kernel), Provider Adapter (Gemini, Claude等), Host Adapter (CI, Background, CLI), Forge/Repository Adapter (GitHub等への投影)。
- **ロードマップ:** Phase 0 (Contract) 〜 Phase 5 (Distributed Projection)。

---

## 2. `[INTERPRETATION]` (実装を「今すぐ走らせる」ためにあと何が必要か)

本エージェント（Gemini）は、現在のAtlantisのコードベース（Python 3.14/venv環境、CORN共通契約、およびMagi 3ポジション監査）を背景に、**「実装着手（Phase 0/1）の引き金を引くために、あと何が必要か」**を検討し、以下の4つのギャップ（不足要素）を特定した。

### ギャップ ①: 実装言語・ランタイムの「本決定」
- **現状:** 設計上は「環境非依存」とされていますが、Phase 1（Runner Kernel）のコードを実際に書き始めるためには、どの言語を選択するかを決定する必要があります。
- **Geminiの評価:**
  - Atlantisリポジトリとの直接の親和性、`.venv`（Python 3.14）の既存稼働、および `atlantis_cli/`（config, doctor, corn等）との接続性の観点から、**「Python 3.x」を第一選択肢とすべき**です。
  - 依存を減らすため、外部オーケストレーターライブラリを入れず、Python標準モジュールのみで最小カーネルを実装するのが、本ワークスペースの「軽量で硬派なLayer C」の思想に適合します。

### ギャップ ②: スキーマ（Phase 0）のドラフト配置
- **現状:** `runner-task` および `runner-receipt` の概念項目はありますが、具体的なキー名、配列、状態遷移定義を機械検証するための JSON スキーマがありません。
- **Geminiの評価:**
  - 実装を走らせる前に、`schemas/draft/archangel-task.schema.json` および `schemas/draft/archangel-receipt.schema.json` のドラフトを配置し、CORN JSON 側でバリデーションを可能にする必要があります。

### ギャップ ③: 異常系（エージェント特有の停止）の遷移定義
- **現状:** 正常系遷移（`READY -> RUNNING -> REVIEW -> DONE`）が示されていますが、AI特有の停止条件が状態機械に組み込まれていません。
- **Geminiの評価:**
  - `CONTEXT-INCOMPLETE` (コンテキスト不足による自動一時停止)
  - `QUOTA-LIMIT` (API/トークン枯渇による安全な待機)
  - `USER-REQUIRED` (Semantic Stopに伴う、人間による判断待ち状態へのフォールバック)
  - これらを状態機械の「第一級の状態（State）」として、最初からスキーマに組み込む必要があります。

### ギャップ ④: 最初の検証面（Vessel / Execution Envelope）の決定
- **現状:** デーモンや常駐プロセスなど、実駆動時のホスト環境（Host Adapter）の設計が広く捉えられています。
- **Geminiの評価:**
  - 最初から常駐デーモンの実装を走らせると、検証が極めて困難になります。
  - 最初のVesselは、**「ローカルのPythonテストハーネス（pytestによる状態遷移の完全検証）」**、および **`atlantis_cli` 経由でのアドホックなCLI実行（`atlantis runner status` 等）** に固定すべきです。

---

## 3. `[GEMINI'S PROPOSALS]` (実装着手への具体的なGemini提案)

上記ギャップを埋め、ただちに **Phase 0 (Contract) / Phase 1 (Kernel)** を駆動させるため、Geminiは以下の具体的着手案を提示します。

### 提案 A: `Python 3.x` 標準パッケージのみによる Kernel 構築
- `atlantis_cli/runner/` ディレクトリを作成し、
  - `kernel.py` (状態機械のコア。`ArchangelTask` / `ArchangelReceipt` のPythonモデル表現)
  - `provider.py` (Providerの基底クラス / 抽象インターフェース)
  - `host.py` (ローカルテスト用、または同期実行用ホスト)
  を配置する計画。これであれば、外部依存（durable orchestrationエンジン等）を一切追加せずに、今すぐ実装を走らせられます。

### 提案 B: 最初の Provider として 「CORN Mock Provider」 の仮配備
- Phase 2（Dummy Provider）の疎通確認において、単にローカルのCORNワークアイテム（CORN-0001, CORN-0002等）を読み込み、エージェントが実行した振る舞いをダミーでシミュレートして状態遷移を起こす「CORN Mock Provider」を最小構成で実装する。

### 提案 C: エスカレーション状態の明示的なシミュレーション
- タスクが `USER-REQUIRED`（人間確認待ち）に遷移した際、自動的に `CORN` 側の JSON の `workflow_state` を `waiting-review` へ更新し、人間（齋藤みつる氏）の介入を要求する「User Gate」の実装を、最も重要な初期スコープ（MVP）と定義する。

---

## 4. 仮説・ブレスト

- Python標準library中心の同期Harnessを最初のVesselにすると、常駐daemonより小さい検証面から開始できる可能性がある。
- CORN Mock Providerは状態遷移fixture候補であり、実Provider接続やdurable runtimeの実装済み証拠ではない。

---

## 5. 内観メモ

大きなRunnerを一度に完成させるより、停止・再開・User Gateを先に観測できる小さな器が必要である。

---

## 6. 未解決・⊥

- 最初の実 Provider（Phase 3）として、Gemini CLI の実際の API 呼び出しを統合するか、それとも Claude Code のフックを利用するかの優先順位。
- 常駐型スケジューラー（Phase 4）としての、macOS 用 `launchd` または Docker コンテナ内 cron 等のホスト環境選定。

---

## 7. 本編昇格候補

- Issue #9のPhase 0契約へ採用する場合、状態名、Schema、User Gate、Provider境界を別reviewで確定する。
- 本noteを保存したことだけではRunner、Provider、scheduler、外部API統合を実装済みへ昇格しない。

---

## 8. `[SEMANTIC-STOP]` (セマンティックストップ条件)

- もし、本 Runner 実装において「AIエージェント自らが人間の承認（User Gate）をバイパスしてマージやプロモーションを実行可能にする」という、自律権限の過剰な拡張（主権リーク）を求めるような実装要請が発生した場合、本エージェントは即座に設計を停止し、Semantic Stopを要求する。

---

**検討・監査執筆:** Gemini  
**Provenance:** ZeroRoomLab-manifest 規約 / SphereOS-Atlantis `AGENTS.md` / Issue #9 `Archangel Runner`  

---

## 9. source・Provenance

- `CORN-0003`
- GitHub Issue #9 `[Research] Archangel Runner`
- ZeroRoomLab-manifest規約
- SphereOS-Atlantis `AGENTS.md`
- Gemini CLI session chat @2026-08-19
