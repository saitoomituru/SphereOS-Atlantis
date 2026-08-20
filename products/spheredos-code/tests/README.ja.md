# presentation tests

状態: `[IMPLEMENTED-ALPHA]`

Node標準`node:test`だけで、次を検査します。

- package／command／CSP契約
- 4件の合成fixture contract
- provider exit 0とOAE commitの分離
- Kernel rejectと成功toneの分離
- provider controlとchat回答の分離
- disconnectとabortの分離
- detected／registered／approved／dispatchableの独立表示
- missing fieldのunknown保持
- fixture由来HTML／scriptのescape

VS Code Extension Host目視試験はこのtest suiteの対象外です。
