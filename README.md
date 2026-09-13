# Dream to Action

**One chosen goal. One real barrier. One usable next step. An honest review.**

A person-directed, local-first prototype inspired by this project's founding discussion of the American way and the American dream: a fair chance to build a life you value, without denying that freedom to somebody else.

The person chooses the goal. The tool separates individual effort from support or institutional change, records what actually happened, and leaves unresolved matters unresolved. It does not rank people, promise outcomes, or treat hardship as proof of personal failure.

## Run it

Download this repository and open `index.html` in a modern browser with JavaScript enabled. The identical standalone application is also available as `prototype/dream-to-action.html`. No account, server, build step, or external application service is required. Normal local-file launch must still be checked on the intended device; the original managed test environment blocked navigation.

Start with four questions:

1. What improvement do you want in your life?
2. What is preventing it?
3. What is one concrete next action you choose?
4. What observable change would count as progress?

Save a plan snapshot, check that its conditions are actually available, and record an observation. **Export before closing:** the app keeps entries in page memory rather than automatically saving them. Exported files are unencrypted.

## Project contents

- [`prototype/`](prototype/) preserves all 12 files from the original v0.1 package, including source, the single-file application, the fictional example, original test results, and the original 11-file SHA-256 manifest.
- [`docs/FOUNDING_CONVERSATION.md`](docs/FOUNDING_CONVERSATION.md) preserves the task's founding exchange with human requests and assistant proposals attributed separately. It is not an official national definition or evidence of public consensus.
- [`prototype/PILOT.md`](prototype/PILOT.md) describes a proposed one-person, one-barrier pilot and a plain-text alternative. The pilot has not started.
- [`prototype/TESTING.md`](prototype/TESTING.md) and [`prototype/test-results.json`](prototype/test-results.json) retain the original validation record and its limitations.
- [`PROVENANCE.md`](PROVENANCE.md) separates the original package from repository additions and later verification.

## Build and check

Python 3 regenerates the original application:

```sh
python prototype/build.py
```

The original browser harness requires Python Playwright and a Chromium browser, which are development dependencies only. Run it in a disposable copy to avoid replacing the preserved release test results:

```sh
python tools/verify.py
python tools/test_browser.py
```

`build.py` is the source of truth for `prototype/app.js`, `prototype/style.css`, and `prototype/dream-to-action.html`. The repository entry point, `index.html`, is a byte-identical copy of that generated HTML.

## Evidence and limits

The original package records **43 passing automated browser checks** using the complete HTML supplied through Playwright `page.set_content`. Those checks are not screen-reader certification, a full WCAG audit, an independent security review, or evidence of real-world benefit. Later checks are recorded separately rather than overwriting the release evidence.

The app does not supply housing, employment, funding, care, legal rights, or another person's agreement. A named helper is not a confirmed commitment. A review date does not create a reminder. Imported content and timestamps are unverified user data, and the journal is not a tamper-proof audit log.

This is an English-language prototype. It has native labeled controls and announced feedback, but actual assistive-technology and participant testing remain necessary.

## Privacy and scope

No participant records or unrelated private conversation history belong in this repository. The included work-report example is fictional. Do not put passwords, account identifiers, confidential work, or unnecessary information about other people into a journal or a public issue.

The original application makes no application network requests and uses no browser-storage APIs. Browser, operating-system, extension, hosting, or backup behavior is outside that claim. Publishing source on GitHub does not itself configure or verify a GitHub Pages deployment.

## Reuse

The original package did not include a license. This import does not silently apply another project's license or alter third-party terms. A project-specific license remains a maintainer decision.

**The next real milestone is somebody gaining a usable choice that was previously blocked—not merely completing a planner.**
