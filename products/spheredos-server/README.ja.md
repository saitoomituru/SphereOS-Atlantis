# SphereDOS Server

状態: `[SCAFFOLDED]` `[RUNTIME NOT IMPLEMENTED]`

VS CodeがなくてもBash／CLIから利用でき、task、lease、OAE transaction、receipt、resumeを保持するheadless CTL
Host候補です。GitHub Actions／CI、local process、将来daemonはHost Profileとして分離します。

- `src/`: CTL HostとKernel adapterの予定地
- `tests/`: crash／resume、duplicate claim、lease timeoutのfixture予定地
- Matchbox: optional distributed Vessel。Fold8Gそのものではない

model inference、provider課金、provider account activationはServerの責務ではありません。
