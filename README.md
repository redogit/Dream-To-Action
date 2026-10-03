# Dream to Action · Operations 0.2

> **Public page:** https://redogit.github.io/Dream-To-Action/ · **Main / About:** https://redogit.github.io/redogit/

**Choose the direction. Make the next step possible. Keep the evidence.**

**[Open the public app](https://redogit.github.io/conscience64/dream-to-action/)** · [Project page](https://redogit.github.io/Dream-To-Action/) · [Main / About](https://redogit.github.io/redogit/)

Current owner policy remains **no third-party commercial access unless explicitly granted**. See [COMMERCIAL_ACCESS_POLICY.md](COMMERCIAL_ACCESS_POLICY.md). This update does not grant a new license or change that policy.

The original planner now has a visual operational successor: a dashboard, action board, goal revisions, dependency checks, evidence history, and a dated reference library. The person remains the authority over the goal. Completing work is not automatically evidence of a better life.

## Start

[Open Dream to Action in your browser](https://redogit.github.io/conscience64/dream-to-action/), or download the repository and open **`index.html`**. It is a self-contained application with no account, runtime dependencies, analytics, or application network calls. The original application remains unchanged at [`prototype/dream-to-action.html`](prototype/dream-to-action.html).

The operational app remains on the verified Conscience64 GitHub Pages route, serving the tested Operations 0.2 release. **This repository remains the canonical source.** On October 2, 2026, the dedicated [Dream-To-Action project page](https://redogit.github.io/Dream-To-Action/) and canonical [redogit main/About page](https://redogit.github.io/redogit/) were enabled and deployed. The earlier profile-host `Pages site Not Found` result remains historical evidence of the previous state, not the current state. [Original app deployment](https://github.com/redogit/conscience64/actions/runs/36459090437) · [Original exact-byte/live checks](https://github.com/redogit/conscience64/actions/runs/36459096995).

For a stable local browser-storage origin, Windows users can run `launch.cmd` with Python 3 installed. On another platform:

```sh
python tools/serve.py
```

The optional server binds only to `127.0.0.1:8765`; `--port` and `--no-browser` are available. It only serves static files and does not receive journal data. Browser storage availability varies by browser and origin. Direct file navigation and loopback browsing were blocked by the managed validation environment, so those launch paths still need checking on the intended device. The identical full HTML was browser-tested through Playwright `page.set_content`.

## What you can do

| Workspace | Operational behavior |
|---|---|
| Overview | Goal counts, readiness breakdown, estimates with unknowns separated, task completion, and a goal/conditions/action/evidence diagram with a text table |
| Action board | Proposed owner, target date, estimated time and USD, support rationale, preceding action, editable plans, review, and explicit completion notes |
| Evidence & history | Observations linked to goal revisions, source references, harmful or null outcomes, and retained change history |
| Resource library | Six dated primary-source references with confirmation questions and a way to draft—not execute—a next action |

Personal mode starts empty. **The illustrative demo is separate**: six fictional goals, eighteen actions, and four observations. Demo numbers are neither user records nor population statistics. Reference metadata is also separate from evidence of available support.

A goal revision makes unfinished actions require review. A named helper is not a commitment. Unconfirmed support or unfinished dependencies prevent an action from being labeled ready. A harm observation requires affected unfinished actions to be reviewed. Completion never creates an improvement observation automatically.

## Keep your records

Memory-only is the default. Export JSON before closing. Optional browser backup requires explicit consent and stores only the personal workspace, not the demo. Browser backup and all exported files are **unencrypted**; do not enter secrets, confidential work, or unnecessary identifying details.

JSON restore validates the complete payload before replacement. Original v0.1 imports retain the full original payload; the current draft is offered as a new candidate with support reset to unknown. Original observations are not silently converted into new-world results. Mixed personal/illustrative v0.1 journals must be separated before import.

Action CSV neutralizes leading spreadsheet-formula characters. A readable handoff includes the complete structured history. None of these exports sends a message, books an appointment, schedules a reminder, or binds another person.

## Build and verify

Development uses Python 3 and Node.js 22 or later; browser tests additionally use Python Playwright and Chromium. The runtime app requires none of these tools.

```sh
python tools/build_operations.py
python tools/verify.py
python tests/browser_operations.py
python tools/test_browser.py
```

`operational/core.js` owns the data rules. `operational/app.js` owns DOM interactions. `operational/style.css` and `shell.html` own presentation. The builder embeds these with `data/demo.json` and `data/resources.json` and computes the content-security-policy hashes. Edit those sources, not just the generated `index.html`.

`tools/verify.py` verifies the unchanged predecessor in an isolated directory using its retained verifier, then verifies the successor build, logic tests, syntax, and fixture structure. The existing read-only GitHub integrity workflow calls that verifier. Browser tests are separate from that CI workflow.

The September 28 update passed **24 state tests, 32 browser assertions, and a fresh rerun of the original 43 browser checks**. See [verification/operations-2026-09-28.json](verification/operations-2026-09-28.json) for the actual scope. These are correlated software checks, not independent demonstrations of accessibility, security, or human benefit.

## Provenance and next use

[Operational guide](docs/OPERATIONS.md) · [Data contract](docs/DATA.md) · [Implementation record](docs/superpowers/plans/2026-09-28-operations.md) · [Founding conversation](docs/FOUNDING_CONVERSATION.md) · [Original publication provenance](PROVENANCE.md)

`prototype/`, the commercial-access policy, Decision Field profile, library-pattern record, and REDOGIT research/history policies remain unchanged. The former repository README is retained at `docs/history/README-before-operations.md`. Historical statements that the root entry point equals v0.1 apply to that earlier publication; the root now intentionally contains the operational successor.

The public hosting projection is pinned to application commit `667e989dcad401829bb097726b3a14cc0aa90f2c` and SHA-256 `231fdadb14093df1028abe015f3c4d583b1031da5ae03048abff5244c3eac807`. Public hosting does not change the source license, publish visitor journals, or turn this static app into a backend service. Update the reviewed publication pin when releasing a new version.

Next real-world milestone: one consenting person gains one usable choice. No participant pilot, service-provider agreement, eligibility determination, or real-world improvement is claimed by this software release.
