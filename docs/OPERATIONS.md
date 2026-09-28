# Operating Dream to Action

## One complete pass

1. Open the personal workspace. Describe one chosen improvement, the actual barrier, and an observable change. Do not start from a required lifestyle or a system-generated ranking.
2. Add one action. State a proposed owner, target date, estimates, and support needed. Blank estimates remain unknown. Confirmed support requires a provider and a recorded basis; a name or directory listing is insufficient. A date does not create a reminder.
3. Resolve support or the preceding action. Review changed goals and harm observations explicitly. Ready means conditions recorded by the user, not an independent feasibility or safety assessment.
4. Try only an acceptable, authorized action. Record completion with a note, then separately record what changed, the basis of that observation, and remaining uncertainty. No change, harm, pause, and a changed direction are valid records.
5. Export JSON and confirm the downloaded file. Review with the person before expanding the work. A completed planner does not establish opportunity or benefit.

## Visuals and reference data

The overview counts only the selected workspace. The board can be filtered by goal and searched by action, owner, or barrier. Progress bars count recorded task completions, not probability of success. The connected diagram has a text table; its arrows do not establish causality. Known cost/time estimates and missing estimates are reported separately.

The demo contains six synthetic scenarios; personal mode is a different in-memory object. No real participant or provider is represented. Source pages in the reference library were checked on 2026-09-28. The stored title, publisher, URL, summary, confirmation questions, and check date are navigation metadata, not a live inventory or eligibility assessment. Clicking an external source sends no journal fields in the link; the destination has its own privacy behavior. Recheck current rules before relying on a resource.

Reference coverage: USAGov benefit finder, housing help, and libraries/archives; Department of Labor American Job Centers and apprenticeship finder; SBA local assistance. The directory contains six references, not every available service. No result in its search is not evidence that no help exists.

## Persistence and recovery

Memory-only is the default. Native browser backup is opt-in, personal-workspace-only, unencrypted, and origin-specific. It may be unavailable under local-file or browser policy restrictions. An existing backup is not silently displayed on launch: restore it explicitly. A write failure is shown and does not destroy the in-memory workspace. Removing the app's browser backup does not delete exported files, other storage, or device traces.

Import size is at most 2 MiB. Full schema validation precedes replacement, and an import racing with a workspace edit is rejected. JSON is rendered as data, never executable markup. A confirmed import replaces its matching personal/demo workspace; it does not merge. Keep both exports when reconciling independent edits.

The legacy import retains the exact parsed v0.1 payload, including snapshots, observations, and unfinished drafts. It maps only the current draft to a new candidate and resets support to unknown. Empty/incomplete drafts can remain retained sources without an operational goal. Mixed personal/illustrative sources are rejected rather than silently blended. Export retained original data from Evidence & history.

CSV is an action handoff, not a restore format. The readable report contains the full structured record as well as a summary. Neither format is encrypted. Browser download requests do not prove a file was saved. Unsaved open-editor fields are not part of workspace exports: save or cancel an editor before leaving.

## Deployment boundary

The release is a self-contained static application. `tools/serve.py` is an optional loopback-only server; it does not accept journal uploads. The current GitHub workflow validates code but does not publish GitHub Pages. A repository URL is not a live application URL. No hosting account, deployment setting, database, third-party service, or scheduled monitor was created here.

## Checks, known limitations, and repair priority

The new full HTML passed synthetic browser workflows at 320, 390, and 768 CSS-pixel widths, plus desktop screenshot inspection. Direct file navigation reproduced `ERR_BLOCKED_BY_ADMINISTRATOR`; the test used the identical HTML through `page.set_content`. Native browser-backup persistence and the optional loopback launch require verification on the target browser. No managed-browser policy was disabled.

Keyboard checks cover labels, initial skip navigation, and modal interactions, not a complete assistive-technology audit. Screen-reader output, zoom combinations, full contrast audit, third-party security review, exhaustive fuzzing, maximum-size responsiveness, and actual participant benefit remain unverified. The dashboard renders bounded records eagerly; performance at the maximum size needs measurement.

The UI's predecessor picker creates one dependency per action. Multiple dependencies are supported in validated imported data; the edit form refuses to silently replace multiple predecessors with one. Completed actions are retained history rather than editable success claims; create a successor action for further work. The journal is not tamper-proof and imported evidence classifications are not authenticated.

Smallest next operational validation: on the intended device, create a synthetic personal goal, export it, restore it, test an opt-in browser backup at a stable local origin, then evaluate a single consensual real task. Preserve failures and added burdens instead of counting them as progress.
