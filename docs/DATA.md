# Operational data contract — dta-operations/1

The application source `operational/core.js` implements the authoritative validation rules. Imported values are assertions by the file, not independently verified facts.

| Object | Purpose and consequential fields |
|---|---|
| Workspace | `schema`, `mode` (personal/demo), `createdAt`, goals, actions, observations, events, nullable retained legacy payload |
| Goal | Stable ID; chosen title, barrier, observable success, category, state; sequential revision and retained snapshots |
| Action | Stable ID; goal ID and revision; proposed owner, target date, nullable estimated minutes/USD; support status, need/provider/note; predecessor IDs; todo/done; completion note and review time |
| Observation | Stable ID; exact goal revision; unknown/improved/no_change/harm; self_reported/observed/documented; note/source; device timestamp |
| Event | Stable ID, event type, entity reference, device timestamp, detail; revisions retain prior values rather than replacing history |
| Reference | Publisher, source URL, checked date, short summary, a draft action, and questions needed before treating support as available |

Required distinctions: person is not the model; task completion is not improvement; self-reported is not independently verified; unknown cost is not zero; named helper is not confirmed support; checked source page is not an available service; demo is not personal data; date is not a reminder.

Limits: 200 goals, 100 revisions per goal, 500 actions, 1,000 observations, 5,000 history events, and 2 MiB serialized input/workspace. Ordinary text fields use a 4,000 JavaScript-code-unit limit; history details allow 32,768. These are safety/resource bounds, not evidence of optimality. Validation rejects unknown schema fields, invalid references/dates, duplicate IDs, dependency cycles, cross-goal dependencies, and contradictory support declarations.

Provenance: v0.1 imports retain the full parsed source under `legacy`; candidate mapping is recorded separately and does not adopt original support or observations as present-day facts. New observations point to the then-current goal revision. A later goal revision does not rewrite old observations.

Privacy: no participant data ships with this release. Only explicit user action navigates to external reference sites. Browser backup is opt-in; exports/backup are unencrypted. The commercial-access policy remains independent of source visibility and has not been changed.
