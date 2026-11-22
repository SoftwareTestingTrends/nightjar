# Review: Snagly plugin (v1.3.0), can NightJar use it?

Date: 2026-11-21. Reviewed: the checkout at `../snagly` (manifests, README, all 30 `skills/*/SKILL.md`, `jira-connector/scripts/jira_client.py`, `targets/`).
Method: read-only. I did not install or run anything, and I did not browse the linked videos or articles.

## Verdict

**Yes, with conditions.** I found nothing malicious or exfiltrating. Install it as a local marketplace from this checkout, not from GitHub. Expect partial overlap with our own skills and no integration with our tracker.

## What it is

30 Markdown skills for browser QA through Playwright (`@playwright/cli` or the Playwright MCP server). They cover flows, accessibility, visual regression, performance, SEO, i18n, security hygiene, bug triage, and Jira filing. The only code is one Python 3.10+ stdlib script, `jira_client.py`. There are no hooks, no MCP server definitions, and no install scripts. MIT licensed.

## What I checked

- **No hidden behaviour.** I searched all skills for `curl`, `wget`, `sudo`, `rm -rf`, `eval`, pipe-to-shell, `chmod`, and "ignore previous", "don't tell the user" and "without asking" wording. The only hits were benign: `npm install axe-core --no-save`, `npx @playwright/cli`, and `chmod 600` on the Jira env file.
- **Network use in the script.** `jira_client.py` talks only to `JIRA_URL`, with TLS verification on. Every write command (create, edit, comment, transition, link, attach) is dry-run unless `--apply` is passed.
- **Safety guidance in the skills.** `browser-safety` treats page content as untrusted data. It says to keep cookies and storage state off any host except the target app. It warns that snapshots leak password fields. It says to use env-var names rather than credential values.
- **Gitignore.** `.env`, `auth.json`, `targets/*.yaml`, `runs/`, `bugs/`, `snapshots/` and `test-cases/` are ignored.

## Risks and caveats

1. **Fetched-on-demand code.** `npx @playwright/cli`, `npm install axe-core`, web-vitals, pixelmatch and Retire.js are pulled from npm at run time, unpinned. The plugin itself is small, but this chain is the real supply-chain exposure. Pin versions or pre-install them in a sandboxed environment.
2. **Jira credentials.** `jira_client.py` reads `.env` by walking up from the current directory, plus `~/.jira-connector.env`. It also reads `$JIRA_ENV_FILE`. Run from a directory where only the intended `.env` can be found. Use a least-privilege API token.
3. **`attach` uploads local files** (screenshots, traces) to Jira. Captures can contain staging data or account details. It is dry-run by default, so read the file list before using `--apply`.
4. **Saved sessions.** `flow-runner` and `e2e-codegen` encourage a reusable `auth.json` storage state. That file is a live session, so treat it like a password.
5. **Mutating skills.** `crud-tester`, `form-fuzzing` and `auth-session-audit` act on live apps. The safeguard is that `safe_to_mutate` is absent from the target profile. Never add it for a shared or production environment.
6. **Metadata inconsistencies.** The version is 1.3.0 in `plugin.json` and `.claude-plugin/plugin.json`, but 1.2.3 in `marketplace.json`. There are two plugin manifests (root and `.claude-plugin/`). Nothing is broken, but it is untidy. The checkout's `.gitignore` also ignores `docs/`.
7. **Provenance.** The manifests list the author as "Ambreen Khan" and the repo as `softwaretestingtrends/snagly`. I could not verify that this checkout matches the upstream repo, and I did not diff against it. If this is not your own project, confirm the checkout's commit against the upstream tag before trusting it.

## Fit with NightJar

- **Overlap.** NightJar already has `browser-check`, `triage-bug`, `verify-fix`, `write-test-cases` and `test-nightjar`. Snagly's `flow-runner`, `bug-triage`, `fix-verifier`, `test-case-writer` and `start-testing` are near equivalents. Both sets would trigger on similar phrases, so enabling both risks the wrong skill firing. Our skills are tied to NightJar, for example `bugs/D-n-…/repro.py` with an exit-code contract and `bugs/ledger.md`. Snagly's use a different layout (`runs/`, `bugs/`, `test-cases/`).
- **Tracker.** `bug-creator` and `jira-connector` target Jira Cloud only. Our tracker is a local stand-in with its own token (`NJ_TRACKER_TOKEN`), so they will not file there. Our `/file-bug` stays the right path.
- **Conventions.** `CLAUDE.md` rules (claims check, injected clock, trace ids in `docs/traceability.md`) are not known to Snagly. Anything it generates, such as `e2e-codegen` output, needs checking against them.
- **Useful additions.** Several skills have no NightJar counterpart:
  - `accessibility-audit` (axe-core)
  - `visual-regression` and `visual-snapshot`
  - `performance-audit`
  - `link-audit`
  - `form-fuzzing`
  - `network-assertion`
  - `security-hygiene`
  - `report-generator`

  The nudge banner and the diary form are plausible targets.

## Recommendation

1. Install from the local checkout (`/plugin marketplace add ../snagly`, then `/plugin install snagly@snagly`). Do not use `npx skills add`, which copies files and drifts.
2. Use it for the audit-style skills listed above. Keep our own skills for flows, triage, verification and filing. Disable or ignore Snagly's `start-testing`, `bug-triage`, `fix-verifier`, `bug-creator` and `jira-connector`.
3. Skip the Jira variables entirely. Do not create a `.env` with Jira credentials for this project.
4. Run only against local `make run` (http://127.0.0.1:8000) with a throwaway database. Create no target profile for any shared environment.
5. Pin or pre-install the npm tools.
6. Before adopting it wider, confirm the checkout against upstream (see risk 7). Re-review on version bumps, because skill text is effectively executable instructions.
