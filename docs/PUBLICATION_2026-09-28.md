# Operations 0.2 publication checkpoint

The visual operational successor was built from baseline `4b8957d6dd88d07552b8d58cbbbd549288686748`. The staged source commit is `14dc392e7cc0cb82e06385d879352cacc950373d`; GitHub generated candidate `dbc4c3b349c0460ad84026c969f3fb69d5aa52a2` only after verification passed.

[Hosted verification run](https://github.com/redogit/Dream-To-Action/actions/runs/36456040639) passed: unchanged predecessor hashes and rebuild, 24 state tests, 32 operational browser assertions, and 43 original browser regressions. The remotely generated standalone file matched the locally tested SHA-256 exactly. The 32 operational browser assertions ran through a real `file://` launch in headless Chromium 143.0.7499.4 on GitHub's Linux runner. This adds a successfully tested launch context; it does not erase the managed local environment's earlier blocked launch or establish behavior on the intended Windows/mobile device.

The root entry point is now intentionally the operational successor. The unchanged predecessor remains under `prototype/`; the former README and verifier are preserved separately. Commercial-access policy, founding conversation, REDOGIT research/history distinctions, and unrelated repository files have not changed. New personal workspaces are empty; six fictional scenarios and six official resource references are carried separately.

The temporary contents-write workflow was used only on the staging branch to materialize and verify the tested generated files. It is excluded from the final main tree. Main retains its existing read-only integrity workflow. The staging branch remains as transport and verification evidence; it is not a second current product.

The planning document records the state before final publication. This checkpoint supplies the later verified build result. Main publication and main CI must be read from the commit and Actions history rather than presumed from this text.

See [hosted verification](../verification/hosted-operations-2026-09-28.json) and [local verification](../verification/operations-2026-09-28.json). No hosting deployment, participant pilot, or assistive-technology certification is claimed. Optional browser-backup persistence and the local launch helper still need a target-device check.
