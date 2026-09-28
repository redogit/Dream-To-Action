# Dream to Action operational workspace

## Design and scope
The requested outcome is a usable visual successor to the original goal/barrier/action/review planner. The human chooses the goal; the system exposes dependencies and uncertainty, not a score of human worth. Preserve the complete original prototype and all unrelated repository contracts and commercial-access rules.

Chosen approach: dependency-free HTML/CSS/JavaScript, with a tested pure state module and a deterministic Python single-file build. Compared with a cosmetic-only overlay, this adds genuine action tracking. Compared with a hosted account/database product, it avoids collecting participant data or requiring infrastructure. No service enrollment, messages, eligibility decisions, or promised social outcomes.

The interface has Overview, Action board, Evidence, and Resources. Visuals derive from the selected workspace. Personal mode starts empty; a clearly labeled, separately held demonstration contains six fictional goals. Six primary-source reference entries carry publisher, checked date, purpose, and confirmation questions; they do not imply eligibility or availability. The original planner stays at prototype/dream-to-action.html.

Operations: goal revisions; action owner, due date, estimated USD/time, support status and rationale, predecessor dependencies; explicit completion with a note; evidence tied to a goal revision; append-only interface history; JSON backup/restore; formula-safe action CSV; readable handoff. Goal changes make unfinished actions require review. A listed provider is never a commitment. No automatic storage: browser backup is explicit opt-in, unencrypted, and separately scoped to personal records. Storage failure must be visible. Links open only by user action; no application network calls.

## Implementation plan
Tech stack: standard JavaScript (Node 22 tests), native DOM/SVG/dialogs, Python 3 builder, optional Playwright browser tests.

- [x] State and tests: tests/operations.test.cjs; operational/core.js. Interfaces: empty, validate, addGoal, reviseGoal, addAction, updateSupport, reviewAction, completeAction, observe, status, metrics, csv, importData. Tests cover readiness, dependencies, stale revisions, atomic validation, references, input bounds, CSV formula safety, and v0.1 retention.
- [x] UI and data: operational/shell.html, style.css, app.js; data/resources.json and demo.json. Native controls, textual chart equivalents, keyboard and narrow-screen support, isolated demo, explicit save/export. Import is replacement only after confirmation; malformed input must preserve the open workspace.
- [x] Build and regressions: tools/build_operations.py; tests/browser_operations.py. Run legacy tests in a disposable copy, new logic tests, new browser workflows, build/hash checks, and syntax checks. Preserve old evidence and record new checks separately.
- [ ] Publish: add the successor entry point and update README/verification integration without touching prototype, license/publication rules, founding text, or unrelated projects. Read back the remote commit and actual CI result. Do not infer a live deployment from a workflow file.

## Review focus
Reject unknown fields and invalid dates/references/cycles before replacement. Keep illustrative outcomes out of personal metrics. Distinguish unknown estimates from zero. Preserve original imported v0.1 payload. Completion and resource discovery are not real-world improvement. Direct screen-reader and human pilot testing remain separate.

## Execution ledger
2026-09-28: remote baseline 4b8957d6dd88d07552b8d58cbbbd549288686748 read through GitHub. Container Git transport has no DNS; use the connected GitHub API for publication, building from mounted original files plus inspected current files. No repository history is rewritten. Task authorized by the user's update request; local design choices follow established no-interruption development preference.

Local results: 24 state tests, 32 browser assertions, 43 original regression checks passed. Browser file navigation remains blocked by environment policy; a fresh page with identical HTML is used for the workflow tests. Prior verifier bytes matched Git blob a1ea5c12dd807d07e70adde90dac3e4d4ad50dce.
