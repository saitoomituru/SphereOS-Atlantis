# MAGI coreと明示profile責務契約

状態: `[CANONICAL-CANDIDATE]` `[IMPLEMENTED-ALPHA]` `[0.200.1]`  
stable ID: `contract://atlantis/magi-core-explicit-profile@0.200.1`  
制定authority: SphereOS Atlantis repository  
適用scope: `magi/0.2.1` resolver、Position Skill、validator、test

## 旧定義

`magi/0.2.1/source-map.json`は、Atlantis内のMAGI bundleを解決するときも
ZeroRoomLab-manifestのAGENTS、理論、運用、哲学文書をrequired sourceとしていた。

これはZeroRoomLab運用では完全な監査deckを作れた一方、次の責務混線を起こした。

- Atlantisの汎用MAGI coreだけを使う第三者もZeroRoomLab-manifestを必須取得する
- MAGIのresolver／validator／Skill実装正本がManifestにあるように見える
- ZeroRoomLab固有の定規、Role、Flavorと、三Position coreの境界がmachine source mapで分かれない

## 新定義

MAGIの責務を次へ分ける。

```text
SphereOS Atlantis
  MAGI bundle / Position Skill / resolver / validator / test
  generic core source map
  explicit profile mount contract

Target Manifest / repository
  local policy / public claims / role / flavor / presentation
  explicit profile declaration
  foldlog / receipt destination
```

default resolverはAtlantis coreだけを解決する。対象repositoryが明示した場合だけ
`--profile <id>`で追加sourceを読む。profile指定は自動repository scanではなく、呼出側の明示操作である。

現行のZeroRoomLab profile IDは`zeroroomlab`とする。

```console
# Atlantis coreだけ
python3 -B magi/0.2.1/resolve_sources.py --slot composite --require-local

# Manifestが明示したZeroRoomLab追加定規をmount
python3 -B magi/0.2.1/resolve_sources.py \
  --slot composite \
  --profile zeroroomlab \
  --repo-root ZeroRoomLab-manifest=/path/to/ZeroRoomLab-manifest \
  --require-local
```

## Position core

三Positionは人格、神託、真理投票ではなく、同じ対象を異なるfailure surfaceから読む監査slotである。

- Maxwell: 目的、資源、生存、探索branch、過剰拘束
- Uriel: source、fact scope、再現、証拠、translation、receipt
- Raphael: 責務、Meaning／Vessel／Bridge／Supply、破局、回復、unmounted meaning

profileは問い、局所定規、Flavor、Presentationを追加できるが、次を上書きしない。

- 三Positionを多数決の真理判定へ変えない
- `unknown`をpassへ変えない
- Position Skillを永続人格へ変えない
- Flavorから権限、外部操作、課金、daemonを生成しない
- 未実装runtimeを実装済みへ変えない
- historical OAEを現在推論から遡及生成しない

## Role／Flavor asset

第三者developerは、自分のManifestまたはrepositoryにRole／Flavor／Presentation assetを置ける。
Atlantis coreへ特定作品・人物・宗派のRoleを同梱する必要はない。

現段階では、対象AGENTS／READMEが必要assetをファイル単位で明示する。暗黙scan、priority merge、
auto-mount、remote downloadは`NOT IMPLEMENTED`である。

第三者作品・実在人物を参照するassetは、対象Manifest側でlicense、provenance、名称利用、適用scopeを
判断する。profileがあること自体は、権利やOrigin認定を生成しない。

## Foldlog

MAGI coreは監査結果の保存先を一律に所有しない。呼出側は対象repositoryの規則に従い、
foldlog、note、Issue、PR comment等から保存先を明示する。

ZeroRoomLab-manifestは`foldlog/`を監査・実行receiptの置場として使う。これはAtlantisの
FAMLog／OAE persistence、scheduler、daemonの実装ではない。

## 互換性とmigration

- `magi/0.2.1` path、legacy version、canonical coordinate、Position IDは維持する
- profile未指定の既存commandは、ZeroRoomLab追加sourceを読まないcore監査へ意味が狭まる
- 従来と同じZeroRoomLab deckが必要な呼出側は`--profile zeroroomlab`を明示する
- Manifest制定期の`Atlantis-MAGISDK 0.2.1`文書とlineage revisionは消さない
- `ATLANTIS_MANIFEST_ROOT`は`zeroroomlab` profile選択時だけ参照する

この変更はsilent rewriteではない。旧source graphはGit履歴とbundle lineageへ保持し、新しい責務境界を
本書、source map schema、test、下流foldlogへ記録する。

## test／fixture

受入条件:

1. 隔離cloneでManifestがなくてもcoreのrequired sourceが0件欠損となる
2. `--profile zeroroomlab`時だけManifest sourceが追加される
3. profile指定時にManifestがなければ`--require-local`が成功を返さない
4. resolverはnetwork accessやsecret scanを行わない
5. bundleがAtlantisをimplementation ownerとして宣言する

## 実装状態

| 対象 | 状態 |
|---|---|
| core/profile source分離 | `IMPLEMENTED_ALPHA` |
| `--profile zeroroomlab` | `IMPLEMENTED_ALPHA` |
| 明示local root | `IMPLEMENTED_ALPHA` |
| repository暗黙asset scan | `NOT IMPLEMENTED` |
| pointer config (`Atlantis.json`等) | `NOT IMPLEMENTED` |
| FAMLog／OAE persistence | `NOT IMPLEMENTED` |
| scheduler／daemon | `NOT IMPLEMENTED` |

## 下流波及票

- ZeroRoomLab-manifest: AGENTS／foldlogから`zeroroomlab` profileを明示する
- third-party Manifest: profile ID、source、assetを自分の責務で宣言する
- 0.2.0以前: 変更せずhistorical artifactとして保持する
