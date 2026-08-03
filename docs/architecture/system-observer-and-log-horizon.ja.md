# system-level ObserverとLog Horizon

状態: `[ALPHA CONTRACT]` `[RUNTIME NOT IMPLEMENTED]`

制定日: 2026-08-03

命名正本: ZeroRoomLab-manifest
[Log Horizon](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/2c68eb63672e68e600518ba46679542b0914757b/docs/theory/log-horizon.ja.md)

## 1. SphereOSでの位置

SphereOS Atlantisは物理粒子の測定器を置換しない。物理Observerの考え方をsystem-levelへ拡張し、model、agent、
API、MCP、Tool、sensor、FAM、OAEが、どのWorldとExecution Envelopeから何を観測できたかを管理する。

`Log Horizon`は、OAEが完全source状態へ到達できず、部分投影だけを取得できる情報子単位のログ境界である。

## 2. 分離する単位

```text
Observer          誰／どのinstanceが観測したか
World             どの規則とfact scopeで観測したか
Execution Envelope どのprovider、権限、tool、runtimeを使えたか
Instrument        embedding model、API、MCP、sensor等
Projection        traffic、vector、output、reading、hash、receipt
Agency            何を採用・実行・再解釈したか
Effect            Worldへ何が作用したか
Unresolved        Horizonの先として残ったもの
```

一つのRun Traceから複数OAEが生じる場合も、OAE candidateが生じない場合もある。trafficが存在するだけで、
その内容がWorldの命令、証拠、冗談、信仰、評価のどれとして成立したかは決まらない。

## 3. 観測envelope候補

次は説明用であり、stable schemaまたは実装済みruntimeではない。

```json
{
  "observer_ref": "observer://instance/001",
  "world_ref": "world://example/001",
  "execution_envelope_ref": "envelope://provider/001",
  "instrument_ref": "instrument://embedding-or-sensor/001",
  "observation_boundary": {
    "kind": "log_horizon",
    "complete_source_observed": false
  },
  "projection_refs": [
    "fam://projection/001"
  ],
  "agency_refs": [],
  "effect_refs": [],
  "unresolved": [
    "provider_internal_state"
  ],
  "last_order_refs": []
}
```

## 4. ElementalとAstral

API traffic、status、syscall、sensor reading、latency、実請求はElemental observationである。それを「便利」、
「腐った」、「この目的ではメシまず」と評価した記録は、主体、目的`λ`、制約`Q`を持つAstral truthである。

SphereOSは両方を第一級に保持し、Astralを主観だから削除せず、Astral評価を全World共通のElemental判決にも変換しない。

## 5. 非主張と停止

- 物理event horizon、Hawking radiation、Higgs粒子を観測したとは主張しない
- provider、model、sensor、Hostの完全内部状態を取得できるとは主張しない
- OAE共通schema、Log Horizon validator、FAM JSONP resolverが実装済みとは表示しない
- Horizonの先は`unknown`、`unreachable`、`permission-denied`等として保持し、架空補完しない
- 再帰pointer、World越境、side effectにはauthority、cycle stop、Last Orderを要求する

## 6. component境界

- Manifest: 名称、哲学、横断claim boundary
- SphereOS Atlantis: Observer、World、Agency、Effect、Execution Envelope契約
- IBD: FAM JSONP、projection、hash、freshness、OAE ref、Last Orderの保存・検索
- Q Atlantis: 公開研究説明と物理／情報子の棚分離
- AAE／adapter: 実際のmodel、network、sensor観測とreceipt生成
