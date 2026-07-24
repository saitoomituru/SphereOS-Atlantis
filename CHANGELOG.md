# Changelog

SphereOS Atlantisの公開候補に含める変更を記録します。日付はrepository上の公開候補日であり、
全Worldの出来事、実装開始、原案作成時刻を意味しません。

## [0.25.1-alpha.1] - 2026-07-19

状態: release candidate branch。tag未作成、正式releaseではありません。

### Added

- repository-nativeなCORN work item、event log、context closure、scheduler／Forge projection plan
- 宣言的なNote shelf／kind registryと、自己申告persona・主張射程・非越権scope
- 巫女、技術者、哲学者、ゲーマー、宗教実践者等から開始できる宣言的persona tutorial
- ブラウザ／SaaS AIからforkまたはbranch経由でNote PRを送る入口
- secretや書込みtokenを要求しないNote-only PR検査
- 生のUX表現と自己申告clusterを保存するExperience Receipt
- 実装状態とquest状態を五軸で分離するForge Map／Quest Map
- GitHub Codespacesのcommunity test募集Issue
- `Presentation.Function.SemanticKernel`三層座標、legacy alias migration receipt、接続fixture
- SemanticKernel／World Config／capability／World Visaに基づく陸続き、Portal、異因果Gate validator
- 習熟度と実装意図を推定しない読み取り専用Help／能力状態案内
- Prompt Line Interface／Command Line InterfaceとLLMI／Execution Envelopeを分離するmachine registry
- `atlantis interfaces`による操作面契約のread-only表示とdoctor検査
- 明示asset receiptだけを読む贈与コモンズlineage validatorと、Role非越権／commons capture／raw secret／scoped stop fixture

### Changed

- 既存`0.25.1`をSource Eventとして保持し、三層座標`0.250.1`へ写像
- MAGI legacy表示`0.2.1`を意味Kernel座標`0.200.1`へ写像
- `0.200.0`で可能だった同一World線OAE再配置を`0.200.1`で拒否
- workspace IDを`sphereos-atlantis-0.25.1-forge`へ更新
- dirty componentをreadyとして扱わず、部分初期化でも既存ready componentをworkspaceから落とさない
- component remoteのhost固定を外し、GitLab等の分散Forgeへ持ち出せる契約へ変更
- Noteの棚・種別をPython固定列挙から`note/registry.json`へ移動
- 自然言語入口を偽CLIまたはPython CLIの再現物と呼ばず、PLI／CLIをD軸／L軸の主な適性として表示
- 既定Helpを利用可能入口優先の`summary`へ変更し、全状態を`--detail all`／`capabilities`へ分離

### Preserved boundaries

- MAGI SDK／OAE時間整合性policyの既存path・receipt表示`0.2.1`はlegacy aliasとして保持
- standalone Atlantis runtime、model inference、component runtime起動は`NOT IMPLEMENTED`
- scheduler実接続、GitHub／GitLab Issue双方向同期、Forge writeは未実装
- 旧OS 3.x／4.x残骸は削除も再稼働もせず`parked-preserved`
- 哲学・倫理・Flavor束は価値を保持するが、組込み・配信済みquestとは表示しない

### Known limitations

- CodespacesはUIとvenvの存在まで画面観測済み。Quota超過によりtutorialとtestの完走は未確認
- Windows実機、GitLab実同期、第三者SaaS AIからのfork PRは未試験
- `ZeroRoomLab-manifest`側の0.25.1-alpha横断契約が先にmergeされるまで、clean checkoutでは一部sourceが`CONTEXT-INCOMPLETE`になり得る
- 火力、runner、cloud-to-edge module構成は`RESOURCE-WAIT`または設計review待ち
- 異SemanticKernel間の接続はvalidator契約だけで、cross-causal runtime gatewayは未実装
- 複数SaaS AI／mobile clientが新しいPLI表現を採用するかは再観測待ち。repository契約だけでvendor出力を保証しない
- asset scan、auto-mount、pointer config、rights／identity／religious adjudication、marketplaceは未実装

不具合、クソゲーフラグ、未対応環境、説明のずれは
[GitHub Issues](https://github.com/saitoomituru/SphereOS-Atlantis/issues)へ報告してください。
