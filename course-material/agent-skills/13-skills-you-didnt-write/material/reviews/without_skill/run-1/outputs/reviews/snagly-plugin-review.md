# Review: Snagly plugin (v1.3.0) for NightJar testing

Reviewed: local checkout at `../snagly` (HEAD `4de2723`, "v1.3.0"), 2026-11-21.
Method: read manifests, `README.md`, `jira_client.py` in full, and grep/skim of all 30 `SKILL.md` files. I did not install or run anything.

## Verdict

**Usable, with conditions. Don't adopt it wholesale.** I found no malicious behaviour. The overlap with NightJar's own testing skills and the Jira-vs-local-tracker mismatch are the real costs. Suggested approach: install it, use the audit-style skills, and leave the defect-loop skills off.

## Safety findings

Good:
- Plain-markdown skills plus one stdlib-only Python script (`skills/jira-connector/scripts/jira_client.py`). No hooks, no MCP server definitions, no install scripts.
- The script talks only to the `JIRA_URL` you configure. TLS verification is on. I found no telemetry and no other hosts.
- Jira writes (create, edit, comment, transition, link, attach) are dry-run unless `--apply` is passed.
- `browser-safety` has sound rules: never fill real credentials as arguments, reuse saved sessions, treat page content as untrusted data, and never send session data off-machine.
- `.gitignore` excludes `.env`, `auth.json`, run artifacts, and the real target profiles.
- MIT licence.

Cautions:
- **Runtime downloads.** Skills run `npm install axe-core --no-save` and `npx @playwright/cli`. Playwright MCP is `npx @playwright/mcp@latest`. Retire.js, web-vitals, pixelmatch and `@playwright/test` are also fetched on demand. These are unpinned `@latest` fetches, so supply-chain exposure is the same as any npx use. Pin versions if that matters to you.
- **Credential file lookup.** The Jira client reads `--env-file`, `$JIRA_ENV_FILE`, `~/.jira-connector.env`, then the nearest `.env` walking up from the current directory. The skills tell the agent not to print the token. Nothing enforces that, so a `.env` in a parent folder could be picked up silently. A shadowing warning exists, but only if the local `.env` names a different site.
- **Tool grants.** `bug-creator` and `jira-connector` allow `Bash(python3:*)`, which is any python3 command. `bug-analyzer` also allows `Bash(git:*)`. That is broader than needed. Note this before approving them.
- **Active probing.** `security-hygiene` (checks for exposed `.env`, `.git/config`), `form-fuzzing`, and `crud-tester` (which mutates data) should be run only against our own staging or local instance. Their guardrails rely on a target profile's `tenants.safe_to_mutate`.
- **Provenance.** The plugin manifest lists the author as "Ambreen Khan", the same name as our git user. If this is your own project, the independence of this review is limited. If not, it is worth confirming the checkout matches the published repo, `softwaretestingtrends/snagly`.
- **Version drift.** `.claude-plugin/marketplace.json` says 1.2.3. The plugin manifests say 1.3.0. This is cosmetic, but it suggests the release process is hand-edited.

## Fit with NightJar

NightJar already has `browser-check`, `test-nightjar`, `triage-bug`, `verify-fix`, and `write-test-cases`. Its contract is in `docs/bug-bundles.md`: `bugs/D-n-<name>/report.md` with a fixed layout, a `repro.py` that exits 1 while the bug is present, and `bugs/ledger.md` with a fixed status vocabulary.

| Area | Snagly | Overlap / risk |
|---|---|---|
| Bug triage, fix verification | `bug-triage`, `fix-verifier` | **Conflicts.** They use browser evidence bundles and their own verdicts (FIXED, STILL BROKEN, REGRESSED, BLOCKED). They know nothing about `repro.py` or our ledger statuses. Using both could produce inconsistent `bugs/` contents. |
| Filing bugs | `bug-creator`, `jira-connector` | **Doesn't fit.** It targets Jira Cloud REST. Our tracker is a local stand-in (`tools/tracker/tracker.py`, `NJ_TRACKER_TOKEN`). Only useful once we're on real Jira. |
| Test cases | `test-case-writer`, `test-plan` | Overlaps `write-test-cases`. Ours is tied to the S-114 ACs and `docs/traceability.md`. |
| Browser flows | `flow-runner`, `crud-tester` | Overlaps `browser-check`. `crud-tester` expects a target profile with a mutate-safe tenant, and NightJar has no tenants. |
| Audits | `accessibility-audit`, `performance-audit`, `seo-audit`, `i18n-audit`, `link-audit`, `security-hygiene`, `visual-regression`, `cross-browser-matrix`, `network-assertion`, `form-fuzzing` | **Real gain.** We have nothing equivalent. Accessibility, cross-browser, and form fuzzing on the CSV import look most useful for a small wellness app. |
| Not relevant | `figma-compare`, `email-verification`, `auth-session-audit`, `seo-audit` | NightJar has no Figma file, email flow, or login. SEO is of little value for a local app. |

Other points:
- NightJar's `CLAUDE.md` conventions (aware datetimes, injected `now`, claims register, no real Claude API in tests) are not known to Snagly. Anything it generates for us, such as `e2e-codegen` output, needs review against them. The existing `make e2e` Playwright test is the pattern to follow.
- Snagly writes to `runs/`, `bugs/`, `snapshots/`, `scenarios/`, `test-cases/`. `bugs/` is shared with our contract, so the collision above is real.
- Snagly depends on Playwright MCP or `@playwright/cli`. NightJar's e2e already uses Playwright and skips if Chromium is missing, so the browser binaries may already be present.

## Recommendation

1. Install as a Claude Code plugin from the local checkout, so skills are namespaced as `snagly:<skill>`. Namespacing avoids name clashes with our skills.
2. Start with `accessibility-audit`, `cross-browser-matrix`, and `form-fuzzing`, run against `make run` on localhost only.
3. Don't use `bug-triage`, `fix-verifier`, `test-case-writer`, or `flow-runner` for NightJar work while `triage-bug`, `verify-fix`, `write-test-cases`, and `browser-check` exist. If you do, tell the agent which `bugs/` contract applies.
4. Skip the Jira skills until there is a real Jira. If we adopt them, use a dedicated low-privilege API token, a `~/.jira-connector.env` with mode 600, and always pass `--env-file`.
5. Review the plugin's `allowed-tools` grants, and pin the npm packages if we run this in CI.
6. Re-review after any version bump. The marketplace update flow pulls new skill text, and skill text is effectively instructions to the agent.

## Not verified

- I did not run any skill or the Jira client, and I did not read every line of all 30 skills. I read the script fully and skimmed the skills with targeted searches for network calls, credential handling, and unusual instructions.
- I did not compare the checkout with the upstream GitHub repo.
- I did not check npm packages for vulnerabilities.
