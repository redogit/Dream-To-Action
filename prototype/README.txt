# Dream to Action — prototype 0.1

**One chosen goal. One real barrier. One usable next step. An honest review.**

This is a first, bounded implementation of the aim discussed in this conversation: a fair chance to build a life one values, with dignity, individual effort, genuine opportunity, and respect for other people's freedom. The implementation is an assistant-created proposal, not an official definition of the American dream or evidence of public agreement.

## Start

Open `dream-to-action.html` in a modern browser with JavaScript enabled. The application is a self-contained HTML file: it contains its code and styling and does not require an account, build step, external service, or server. Local-file launch was not verified in this testing environment; see **Validation boundary** below. Managed browsers may impose their own restrictions.

Begin with four required fields: your chosen improvement, the barrier, one concrete action, and the observable change that would count as progress. Optional fields record support, proposed responsibility, constraints, readiness, and a review date. Save a snapshot, try an acceptable action when its conditions are available, and record what actually happened.

`Load an example` inserts an explicitly fictional work-report accessibility scenario. It does not represent the user's history, an actual participant, a provider's commitment, or a successful intervention.

## What is implemented

- Person-directed goals rather than a required definition of success or a human-worth score.
- A distinction between individual action and necessary support or external change. Naming a helper does not bind or contact them.
- Conservative readiness messages: unconfirmed support and contradictory support fields do not become confirmed opportunity. Readiness remains self-reported, not an independent safety assessment.
- Separate plan snapshots and observations linked to the plan they concern. Unsaved plan changes must be recorded before an observation can be attached.
- JSON export/import, a readable text report, and printing of saved snapshots/history. JSON and text exports preserve unfinished drafts as well as recorded entries.
- Native labeled controls, keyboard access, error links, and status feedback. English-language prototype, not a claim of universal accessibility.

## Your data

The application has no account, analytics, application network calls, browser-storage API calls, or automatic upload. It keeps entries in page memory until you export them. Closing or reloading can lose work. JSON export requests a download; confirm that the browser actually saved the file.

**Exports are unencrypted. This is not a secure vault.** A browser, operating system, extension, backup service, shared device, or user-chosen storage location may retain traces. Do not enter passwords, account identifiers, confidential work, or unnecessary information about other people. Clearing the open journal does not delete exported files or device traces.

Imported records are unverified data. The application validates its schema, bounded field lengths, supported options, timestamps, sequential IDs, and plan references. It renders imported content as text, not executable HTML. Limits: 4,000 JavaScript string code units per text field, 500 plan snapshots, 500 observations, and 1 MiB per imported/exported JSON file. The UI's ordinary term “characters” approximates the code-unit limit; some Unicode characters occupy more than one code unit. Smaller journals are preferable. If a journal exceeds the JSON size limit, the text report remains an archival fallback, but it cannot restore editable structure.

History is preserved within the interface; files can be edited externally. Device/imported timestamps are not authenticated. This is not a tamper-proof audit log. A review date does not schedule a reminder.

## From a tool to actual opportunity

A planner cannot supply a job, home, care, funding, institutional access, or somebody else's agreement. The next milestone is a consenting person's real barrier becoming smaller or an important action becoming usable. The tool must not substitute for that change.

`PILOT.md` provides a small real-world trial and a plain-text alternative to the application. No pilot participant has been enrolled, provider contacted, resource committed, message sent, reminder scheduled, or project published by this package.

## Validation boundary

**43 automated browser checks passed** on the final included implementation in Chromium 144.0.7559.96 using Playwright Python. See `test-results.json` and `TESTING.md` for exactly what was checked.

The managed test browser blocked both file-scheme and loopback-HTTP navigation. The same complete HTML was therefore supplied through Playwright's `page.set_content`, without altering its application code or security policy. Direct local-file launch remains unverified. The tests exercise the browser logic, not every deployment context.

No actual JAWS, NVDA, VoiceOver, or other screen-reader session, full WCAG audit, independent security audit, or real-world outcome trial was performed. Automated checks are not certification.

## Source and reproducibility

`build.py` is the source of truth for the HTML, JavaScript, and CSS. Running it with Python 3 regenerates `dream-to-action.html`, `app.js`, and `style.css`, including the embedded content-security-policy hashes. The generated JavaScript and CSS are included for convenient inspection; edit `build.py` before rebuilding rather than editing only these generated copies.

`test_app.py` contains the browser checks. It requires Python with Playwright and a Chromium browser. It looks for `CHROMIUM_PATH`, then Chromium/Google Chrome on PATH, otherwise Playwright's default installed Chromium. These are development dependencies, not application dependencies. The test harness reads and supplies the HTML directly because navigation is restricted in this environment.

Run from this folder:

```text
python build.py
python test_app.py
```

`MANIFEST.sha256` records the packaged files' hashes at release. It establishes package-byte consistency, not third-party attestation or the truth of journal contents.

## Design references

W3C WAI Forms Tutorial — labels, grouping, instructions, validation, and feedback:
https://www.w3.org/WAI/tutorials/forms/

W3C WAI Form Instructions — explicit instructions and associations:
https://www.w3.org/WAI/tutorials/forms/instructions/

W3C WAI ARIA22 — announcing routine status updates:
https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA22

Consulted September 13, 2026. These references inform the interface; they do not certify the implementation.
