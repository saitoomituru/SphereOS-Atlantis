# USAD SDK／UPBGE World Driver Alpha選定

> Status: `[TARGET-SPEC]` `[ALPHA-CANDIDATE]` `[NOT IMPLEMENTED]`
>
> 制定日: 2026-07-29
>
> 横断方針: ZeroRoomLab-manifest `docs/projects/sphere-renderer-runtime-selection-20260729.ja.md`

## 1. 決定

SphereOS AtlantisのWorld／scene／physics接続について、Alpha実装のReference Driver対象をUPBGEとする。

SDK名は次を現行候補とする。

> **USAD SDK = UPBGE SphereOS Atlantis Driver SDK**

Atlantisはrendering engineではない。Atlantis World Stateをsource of truthとし、UPBGE sceneはprojection／cache／simulation Vesselとして扱う。

```text
Atlantis World State
        ↓ explicit projection
USAD Core SDK
        ↓ engine binding
USAD for UPBGE
        ↓
UPBGE scene／physics／animation／input
```

## 2. Meaning／Vessel／Bridge／Supply

### Meaning

- World Stateを特定3D engineへ閉じ込めず、sceneへ投影する
- World authority、Entity、state、command、event、receiptを分離する
- Blender／UPBGEのasset authoring、physics、animationをAtlantis World研究へ接続する
- adapterが失われてもWorld Stateとasset参照を回収可能にする

### Vessel

- USAD Core SDKのSchema、validator、fixture、event envelope
- UPBGE adapter
- UPBGE service lifecycle
- explicit World fixture

### Bridge

- Atlantis World StateとUPBGE scene graphの間の双方向adapter
- GLB／glTF asset参照
- process分離またはpackage分離の候補境界

### Supply

- SDK revision
- dependencyとlicense
- fixture World
- tested UPBGE／Blender version
- capability receipt
- 未試験範囲

## 3. Atlantis World Stateを正本にする

UPBGE scene内のGameObject、Collection、animation、physics bodyはAtlantis World Stateのprojectionである。

次を禁止する。

- sceneが表示されたことをWorld整合性の証明にする
- UPBGE内変更をauthority確認なしにAtlantis正本へ書き戻す
- object nameだけでEntity identityを確定する
- physics resultをWorldの普遍的自然法則へ昇格する
- adapter停止をWorld消滅として表示する

Worldからsceneへの投影は再生成可能であることを目標にする。sceneからWorldへの書戻しは、explicit command、authority、conflict policy、receiptを要求する。

## 4. Package境界

### 4.1 USAD Core SDK

Apache-2.0候補のengine-neutral領域。

```text
usad-core/
  schemas/
  world_projection/
  entity_mapping/
  events/
  commands/
  receipts/
  capability/
  asset_refs/
  fixtures/
```

責務候補:

- World／Entity／componentのprojection contract
- stable Entity IDとengine-local object IDのmapping
- command／event envelope
- append-only receipt
- capability negotiation
- async asset loader abstraction
- World manifest／asset reference
- authorityとwrite policyの伝搬

### 4.2 USAD for UPBGE

UPBGE／Blender APIへ接続する薄いadapter。GPL-compatible package境界候補として分離する。

```text
usad-upbge-adapter/
  bge_binding/
  scene_binding/
  collection_binding/
  game_object_binding/
  transform_projection/
  animation_projection/
  physics_projection/
  input_events/
  collision_events/
  service_lifecycle/
```

Core側へ`bge`型、Blender内部path、scene object pointerを漏らさない。

## 5. Alpha contract候補

### WorldからUPBGE

```json
{
  "operation": "project_entity",
  "world_id": "<stable-world-id>",
  "entity_id": "<stable-entity-id>",
  "revision": "<world-revision>",
  "asset_ref": "<explicit-glb-or-library-ref>",
  "transform": {
    "position": [0, 0, 0],
    "rotation": [0, 0, 0, 1],
    "scale": [1, 1, 1]
  },
  "authority": "world-authority-ref",
  "receipt_required": true
}
```

### UPBGEからAtlantis

```json
{
  "event": "physics_observation",
  "world_id": "<stable-world-id>",
  "entity_id": "<stable-entity-id>",
  "adapter_id": "usad-upbge/<revision>",
  "observed_transform": {},
  "simulation_time": 0,
  "write_intent": false,
  "authority": "unknown",
  "receipt": "<receipt-ref>"
}
```

物理観測eventは既定で観測であり、正本更新命令ではない。`write_intent=true`でもauthorityとconflict policyが解決しなければ書き戻さない。

## 6. Capability negotiation

UPBGE adapterは少なくとも次を申告する。

```text
rendering
rigid_body
soft_body
animation
input
collision
scene_spawn
scene_despawn
asset_glb
round_trip_transform
```

値は`AVAILABLE`、`NOT IMPLEMENTED`、`NOT TESTED`、`UNAVAILABLE`、`UNKNOWN`を区別する。package存在やimport成功だけで`AVAILABLE`にしない。

## 7. Asset pipeline

```text
Blender authoring
  ↓
GLB／glTF export
  ↓
explicit asset receipt
  ↓
Atlantis World asset_ref
  ↓
USAD projection
  ↓
UPBGE runtime
```

`.blend`を唯一の配布正本にしない。研究用sourceとして保持できるが、Worldが参照するassetにはrevision、license、provenance、hashを付ける。

## 8. SphereASTROとの境界

SphereASTROのGodot Reference RuntimeはPresentation consumerであり、USAD for UPBGEを直接importする前提にしない。

共有する候補は次である。

- GLB／VRM／ASTRO avatar asset
- engine-neutral BodyEvent／World event
- stable Entity／World ID
- capability／receipt envelope

ASTROのavatar manifestationとAtlantisのWorld simulationを同一scene graphへ固定しない。

## 9. Alpha実装順

1. explicit World fixtureを一つ作る
2. USAD CoreのEntity mappingとprojection requestを定義する
3. UPBGEでGLB objectをspawnする
4. World transformをsceneへ反映する
5. physics観測をreceiptとして戻す
6. authority不明時に正本writeを停止する
7. adapterを外してもWorld fixtureとasset receiptが読めることを確認する
8. version、test condition、failure receiptを残す

## 10. 過去データーマイニング待ち

USAD SDKには過去会話・設計断片が存在するが、現時点で完全な歴史仕様を回収していない。

確認済みの核:

- USAD = UPBGE SphereOS Atlantis Driver SDK
- Atlantis World Stateがsource of truth
- USAD CoreはApache-2.0候補
- UPBGE adapterはGPL-compatible境界候補
- UPBGEがrendering／physics／animation／input／game loopを担当

未回収fieldや旧APIを現在の推論で捏造しない。詳細発掘後は、旧定義、新定義、互換、migration、test fixtureを並べて更新する。

## 11. Non-goals

- Atlantis本体をUPBGE pluginへ縮退しない
- UPBGEを唯一のWorld engineにしない
- Godot、Unity、Unreal等の全adapterをAlphaで同時実装しない
- scene object名をSphere identity正本にしない
- physics simulationを形而上学または自然科学の普遍証明にしない
