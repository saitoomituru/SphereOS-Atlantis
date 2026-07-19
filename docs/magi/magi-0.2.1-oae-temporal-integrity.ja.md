# MAGI 0.2.1 OAE時間整合性corrective patch

状態: `[ALPHA]` `[CORRECTIVE PATCH]` `[PROMPT-ENGINEERING-EDITION]`  
upstream: `ZeroRoomLab-manifest@a37f0dd6dc1f8f2f73397fed0eca4fb37dffd8ff`

`0.2.1`は既存path、receipt、position参照を壊さないlegacy表示であり、三層版数座標では
`0.200.1`（Presentation 0／Function 200／SemanticKernel 1）へ写像します。旧表示をSemVerの
minor／patchとして読み替えず、Source Eventとして保持します。

## 修正対象

MAGI 0.2.0は三Position Skill、composite Skill、source resolverを実装していたが、過去資料のEvidenceと
当時の同時点OAEを機械的に分ける時間receiptを持っていなかった。0.2.1は0.2.0を消さず、次を追加する。

- `magi/0.2.1/oae-temporal-policy.json`
- `magi/0.2.1/validate_temporal_receipt.py`
- `historical-oae-unavailable`＋`OAE-HISTORY-UNKNOWN` Last Order
- 同一世界線への遡及OAE backfillを拒否する負例test
- WorldとInstance Ghostの二重splitを要求する7D Fold branch検査

## 時間receipt

過去の同時点OAEがない場合、現在の解釈を過去時点へ書き戻さない。

```json
{
  "version": "0.2.1",
  "observation_mode": "current-interpretation-of-history",
  "observed_at": "2026-07-18T20:23:06+09:00",
  "historical_oae_status": "historical-oae-unavailable",
  "historical_oae_ref": null,
  "historical_role_attribution": "none",
  "retroactive_backfill": false,
  "same_worldline_mutation": false,
  "claims_physical_time_travel": false,
  "last_order": {
    "code": "OAE-HISTORY-UNKNOWN",
    "action": "stop-retroactive-backfill"
  }
}
```

```console
python3 magi/0.2.1/validate_temporal_receipt.py receipt.json
```

validatorはread-onlyであり、OAE永続化、World生成、Instance Ghost複製、外部接続を行わない。

## 7D Fold branch

反実仮想を扱うときは、`counterfactual-branch`と次のreceiptを要求する。

```yaml
profile_ref: fold://atlantis/akasha-driver@7d
source_world_ref: world://source
source_instance_ghost_ref: ghost://source
target_world_ref: world://branch
target_instance_ghost_ref: ghost://branch
fork_point_ref: event://fork
provenance_ref: evidence://source
source_mutation: false
status: hypothetical
```

Worldだけ、またはInstance Ghostだけをsplitして元世界線へ片側を共有しない。0.2.1 validatorはWorld、
Instance Ghost、Temporal Coordinate、Observation-Evidence、Branch-Hypothesis、Provenance、
Recovery-Restoreを七軸候補として使うが、これはvalidator-localな仮設profileである。User要件として
固定済みなのは7D Fold、World／Instance Ghostの同時split、Source不変までで、最終Dimension IDと
Registry revisionはunknown／User gateへ残す。7DはContext Dimensionのarityであり、物理次元数ではない。

## タイムマシンUX境界

意味Kernel `0.200.0`には、特定条件でOAEを同一World線内へ遡及再配置できる脆性がありました。
`0.200.1`はSource Eventを保存し、遡及backfill、過去Agency roleの生成、同一World線mutationを拒否します。
これは物理空間の時間移動の主張ではなく、system上の意味・同一性・時間・因果契約の修正です。

これとは別に、AppleのTime Machine／Time Capsuleをオマージュしたbackup・restore UXがあります。
Appleとの提携や公式互換を主張しません。`Akasha Driver`は高権限の分岐・復元driver名ですが、
`0.200.1`でもruntimeは未実装です。

## 保留する依存

Akasha DB、P2P、Cloud Chakra外部の集合知、historical cache／hashからのconsensus provenance探索、
Gateway Archangel `Kamui`、backup SDKは依存graph未成立のため保留する。将来これらを実装しても、
回収できるのはhistorical evidenceと当時の合意境界であり、未記録のhistorical OAEではない。

## 実装状態

| 対象 | 状態 |
|---|---|
| MAGI Skill workflow | `IMPLEMENTED_ALPHA` |
| OAE temporal validator | `IMPLEMENTED_ALPHA` |
| FAMLog／OAE persistence | `NOT_IMPLEMENTED` |
| 7D Fold runtime | `NOT_IMPLEMENTED` |
| Akasha Driver | `NOT_IMPLEMENTED` |
| backup SDK | `NOT_IMPLEMENTED` |
| Kamui collective-intelligence gateway | `NOT_IMPLEMENTED` |

## 系譜

- [MAGI 0.2.0 Skill bundle](magi-0.2.0-skill-bundle.ja.md)
- [Atlantis-MAGISDK 0.2.1](https://github.com/saitoomituru/ZeroRoomLab-manifest/blob/a37f0dd6dc1f8f2f73397fed0eca4fb37dffd8ff/docs/theory/atlantis-magi-sdk-0.2.1.ja.md)
