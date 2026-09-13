# Provenance and publication boundary

## Origin

The repository owner requested a discussion of the American way, asked whether that understanding fits the American dream, and then requested an implementation. ChatGPT proposed and generated Dream to Action v0.1. The user subsequently requested publication of the complete project on GitHub and created the matching `redogit/Dream-To-Action` repository.

The human requests, the assistant's interpretation, the code, and observations about the code remain distinct. This is not an official definition of the American dream, a political consensus claim, or evidence that a social outcome has been achieved.

## Preserved package

Original artifact: `dream_to_action_v0_1.zip`.

Original archive SHA-256:

```text
765770675c800d05a592e07e34f5b1c520657cab03cbffa3466b6bf19c54c1c4
```

Every one of the archive's 12 files is preserved byte-for-byte under `prototype/`. The only path transformation is from the archive's `dream_to_action/` prefix to `prototype/`. The archive container is not duplicated as a redundant binary; its complete extracted contents are committed directly. A GitHub-generated repository ZIP has different paths and archive metadata and is not the original ZIP byte stream.

`prototype/MANIFEST.sha256` is unchanged. It lists 11 file hashes and does not hash itself. The complete 12-file Git tree is:

```text
b371f793363af7633ae34ec8b13456d419bcf85c
```

This tree identity was independently calculated from the local original files and matched the GitHub-created subtree before publication. Hash equality establishes byte identity, not semantic truth, third-party attestation, or independent corroboration.

The root `index.html` is a byte-identical copy of `prototype/dream-to-action.html`:

```text
efa6372b2fd180a52a9024b6caa2b992f19dc50f2f10f84f31c783bfb28aef09
```

## Repository additions

The root README, this provenance document, the founding-conversation record, verification helpers, import-check record, Git settings, and read-only verification workflow were added for publication. They are not represented as part of the original v0.1 archive.

`docs/FOUNDING_CONVERSATION.md` preserves the substantive founding exchange and the publication requests from the visible conversation. Speaker headings were added and temporary attachment links were mapped to repository equivalents. Operational progress messages, tool output, interface timing labels, unrelated memories, and private reasoning are outside that document. It is not a full platform export. The assistant's prose remains attributed to the assistant, not silently reassigned to the human.

The original README's statement that the package had not published a project is retained as historical release wording. This GitHub publication is a later event, not a reason to rewrite the original file.

## Checks and limits

`verification/import-check.json` records the publication-preparation checks. The original 43-check browser suite was rerun in a disposable copy; all 43 checks passed in Chromium 144.0.7559.96. The original test-results file was not overwritten. The rerun produced the same result-file bytes as the preserved result, and its actual execution times are recorded separately.

The repository helper `tools/verify.py` checks the release hashes, exact file membership, root entry point, canonical-LF rebuild outputs, and inline security-policy hashes. `tools/test_browser.py` reruns the original suite in a disposable copy and writes a timestamped record under ignored `.test-output/`. The original harness contains a fixed historical date and environment statement; the wrapper distinguishes those retained strings from the new execution's timing and scope.

The GitHub workflow checks integrity, rebuild consistency, and JavaScript syntax. It does not run the browser suite or certify accessibility. It uses repository-local commands without third-party Actions and has read-only repository permissions. Workflow success must be checked on GitHub rather than inferred from the existence of its YAML file.

Direct local-file launch, hosted deployment, actual screen-reader use, comprehensive accessibility/security evaluation, and a real-world pilot remain outside these import checks. A proposed pilot is not an enrolled participant or a demonstrated benefit.

No unrelated private history, participant journals, credentials, or confidential work records were included. No website deployment settings, service-provider commitments, or scheduled reminders were created by this import. No license was inferred from a different repository.
