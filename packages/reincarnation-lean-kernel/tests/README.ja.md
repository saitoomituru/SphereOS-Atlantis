# package-local fixtures

task／lease／write-set／OAE transactionのnegative fixtureです。synthetic fixture本体は
`../fixtures/`に置き、ここはfilesystem Harness(`sphere_reincarnation_harness`)のunittestです。

- `test_layout.py`: root安全条件(`/`、user home、repository root、空文字拒否)とplanの副作用なし
- `test_store.py`: atomic write、silent overwrite拒否、append-only receipt、symlink escape拒否
- `test_decisions.py`: `../fixtures/`の6 fixtureそれぞれの決定とeffect_applied=falseの拘束
- `test_cli.py`: plan／init／inspect／evaluateのCLI flowとroot省略時の停止
