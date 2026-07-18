# Web検証ブラウザ・コンテナ結界 移管票

状態: `[QUEUED]`

```yaml
source_note: note/20260718-1648__Web検証ブラウザをコンテナ結界へ封印するブレスト.ja.md
target_repository: SphereOS-Atlantis
target_responsibility: 開発環境のbrowser観測profile、観測receipt、offline fixture
reason: 標準Venv／Dev Containerの安定を維持しながら、Web実行を別の破棄可能境界へ隔離するため
meaning_to_preserve:
  - コンテナ結界は完全防御または安全性保証ではない
  - 検索snapshot、HTTP観測、browser観測、origin freshnessを混同しない
  - SaaS vendor内部の検疫方式を未観測のまま断定しない
  - browser profileを標準開発環境へ常駐させない
required_restructuring:
  - noteの比喩をdocsの権限契約とtest可能なacceptance criteriaへ写像する
  - browser依存を標準Python依存から分離する
  - offline fixtureを先に実装し、公開URLのsmoke testを後段にする
license_provenance:
  - repositoryのLICENSESと第三者browser／driver licenseを採用時に確認する
status: queued
target_commit_document: unknown
```

## 発火ゲート

- [x] 標準Venvとclean-room testが通る
- [x] 標準Dev Container定義がコードreview可能な状態にある
- [ ] DockerまたはPodmanで標準Dev Containerを実buildできる
- [ ] 観測receipt、network、mount、cleanupの契約をreviewする
- [ ] browser imageの費用、取得元、version固定、更新方針を決める

未完了ゲートを実装済み扱いしない。Docker／Podmanのない現在のhostでは、browser branchを発火させない。

## 移管タスク

1. `docs/development/browser-source-observation.ja.md`へ観測クラスとreceipt Schemaを起こす。
2. `.devcontainer/browser/`を標準profileとは別に作り、認証情報・Docker socket・host browser profileを
   mountしない静的contract testを追加する。
3. local static fixtureだけでSelenium／headless Chromiumを試験する。
4. timeout、process kill、一時profile、artifact、container／volumeの清掃receiptを得る。
5. 外部実行は、明示承認された非認証URL一件の単発smoke testから開始する。

## 停止条件

- source／license／利用規約／robots／privacyのauthorityが不明
- 認証済みCookie、秘密値、host filesystem write、Docker socketが必要になる
- narrative上の「結界」が実際の安全保証として誤表示される
- VS Code UXが標準profileと観測profileを区別できず、browserが暗黙起動する
- 取得物の保存が第三者著作物、個人情報、秘密情報を過剰保持する

機械的な依存、PATH、browser／driver version、fixtureの不具合は、上記境界を変えない範囲で自動debugしてよい。
