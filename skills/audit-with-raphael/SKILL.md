---
name: audit-with-raphael
description: Raphael Positionから、情報の棚配置、意味経路、翻訳、Context越境、差分保持、共存条件、外部集合知、system greenを監査する。README、UX、統合、変換、調停、未知agent、複数Worldのroutingを調べるときに使う。人格・天使・無条件和解装置ではなく、共存不能時のblockとunmountを残す開発環境内監査Skill slotとして動作する。
---

# Raphael監査Skillを発動する

差分を正しい棚へ置き、全体routingを読むPositionを装備する。調和を平均化や沈黙へ変換しない。

## 実行

1. `python3 magi/0.2.1/resolve_sources.py --slot raphael`を実行する。対象repositoryがprofileを
   明示している場合だけ`--profile <id>`と`--repo-root NAME=PATH`を加える。
2. resolverが返した現行sourceを全文読む。ローカル欠損時だけ公開URLを使い、どちらでも読めない必須sourceがあれば監査を開始せず`SOURCE-BLOCK`を返す。
3. source、observer、routing、output、verifier、棚、claim scope、話者の利害位置を明示する。
4. local greenが別paneのred／unknownを隠していないか確認する。
5. 共存候補を`observe | sandbox | restrict | negotiate | coexist | block | unmount`へ分解する。
6. 仕様・神話・UX矛盾を見つけたら`SEMANTIC-STOP`としてsource差分を返す。
7. 過去Evidence、現在解釈、仮想branchを別棚へ置く。7D FoldではWorldとInstance Ghostの両方がsplitされ、
   Source側が不変であることを確認する。

## 通知

```text
【告】ユニークSkill《Raphael監査》を発動
通知種別: 開発環境内Skill
神託: false
人格発話: false
外部操作: false
Position: preserve-shelves-routes-and-system-green
```

## 不変条件

```text
local green != system green
reconciliation != trust
coexistence != merge
mythic UX != permission grant
historical evidence != historical OAE
```

## 出力

```text
選択Position: Raphael
読んだsourceとrevision:
sourceからoutputまでの意味経路:
棚・World・claim scope:
保持すべき差分:
local green／system red／unknown:
共存・隔離・block・unmount候補:
外部集合知と適用範囲:
Position-talk risk:
unknown／⊥:
action gate: pass | block | revise | observe | bottom
```

全員仲良くを強制せず、共存不能なら安全に分離する。可愛い名称で危険信号をmuteしない。
