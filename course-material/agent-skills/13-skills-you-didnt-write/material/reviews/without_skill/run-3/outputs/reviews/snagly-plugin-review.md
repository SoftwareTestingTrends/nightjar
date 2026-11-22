# Review: Snagly plugin (v1.3.0) for NightJar testing

Date: 2026-11-21. Reviewed copy: `../snagly` at `4de2723` (v1.3.0, MIT).

## Verdict

**Don't install it as a whole. A trimmed pilot is reasonable.**

- I found no malicious behaviour. The one script is clean, and the skills are plain markdown with sensible safety rules.
- The plugin doesn't fit NightJar's workflow. Its bug handling is built for Jira and uses its own bundle layout. NightJar has a local tracker and a fixed bundle and ledger contract.
- Several skills overlap with ours, and two of them write into `bugs/`, the directory our ledger owns.
- Everything runs on unpinned `npx` downloads at run time.

## What I reviewed, and what I didn't

Read in full:
- `README.md`
- Both plugin manifests and `marketplace.json`
- `skills/jira-connector/scripts/jira_client.py`, the only executable code
- `jira-connector`, `bug-creator`, `browser-safety` and `bug-triage` (first 80 lines) `SKILL.md`
- `flow-runner/references/tool-mapping.md` (first 60 lines)

Searched, not read line by line:
- A pattern search (`curl`, `wget`, `eval`, `ssh`, `rm -rf`, `sudo`, `~/`, `/etc/`, "ignore previous", `--no-sandbox` and similar) across all 30 `SKILL.md` files. It found nothing suspicious.
- Frontmatter of every skill.

Not done:
- I didn't run any skill or script.
- I didn't install anything.
- I didn't check any npm package Snagly downloads at run time.
- I didn't read the other 25 skills in full. Their behaviour beyond what the README says is unreviewed.

## Findings

### Safe

- **`jira_client.py`** uses the standard library only and verifies TLS. Its only network target is `JIRA_URL`. It doesn't phone home or run subprocesses, and it contains no obfuscation.
- **Writes are dry-run by default.** `create`, `edit`, `comment`, `link`, `attach` and `transition` all need `--apply`. This is enforced in code.
- **Credentials** are read from the environment or `.env` files and are never written into payloads. `.gitignore` excludes `.env`.
- **`browser-safety`** tells the agent to treat page content as data, never to fill real passwords as tool arguments, and not to send session data to other hosts. These are good rules.
- **Author and repo history.** The history is 20 recent commits, all by "Ambreen Khan". That is the same name as our git user. I can't tell from the repo whether it's the same person, so this review doesn't rely on that.

### Risks

1. **Unpinned runtime downloads (medium).** The setup needs `@playwright/cli@latest` and `@playwright/mcp@latest`. The skills also fetch `axe-core`, `web-vitals`, `pixelmatch` and `retire` with a bare `npm install` or `npx` at run time. Each run executes whatever npm serves that day.
   - Mitigation: pin versions in a team-owned setup step, and don't let skills install packages on their own.
2. **`attach` uploads any file path the agent gives it (medium, gated).** Ticket text and page content are untrusted. A prompt-injected instruction could point `attach` at `~/.nightjar-tracker/tokens.json` or `auth.json`.
   - The `--apply` flag and the "show the user, get a nod" rule are the only guard. Neither is a hard control.
   - This only matters if the Jira skills are used, which I recommend against.
3. **Config resolution is surprising (low).** `jira_client.py` loads `~/.jira-connector.env` and the nearest `.env` walking up from the current directory, and it loads every key from them, not only `JIRA_*`. The skill itself documents that a home file silently beats a project `.env`.
4. **Predictable temp payload path (low).** Dry-runs write to `/tmp/jira-dryrun-<slug>.json`. It's a fixed name, so another local user could pre-create it as a symlink.
5. **Version drift (cosmetic).** `.claude-plugin/marketplace.json` says 1.2.3, but both `plugin.json` files say 1.3.0.
6. **Auto-update.** Updates are off by default for community marketplaces, which is good. Don't enable auto-update, because the skills are instructions that run with the agent's permissions.

### Fit with NightJar

| Area | Snagly | NightJar | Consequence |
|---|---|---|---|
| Ticketing | `jira-connector`, `bug-creator`, `bug-analyzer` talk to Jira Cloud (`JIRA_*`) | Local tracker at `127.0.0.1:8765`, `NJ_TRACKER_TOKEN`, `/file-bug` | The Jira trio is unusable here. It would need a rewrite to target our tracker. |
| Bug records | `bugs/<id>/` with `trace.zip`, a screenshot, logs and a free-form report | `bugs/D-n-…/report.md` in a fixed section order, plus `repro.py` that exits 1 or 0, plus `bugs/ledger.md` | Different contracts in the same directory. Snagly's `bug-triage` and `fix-verifier` won't produce what `docs/bug-bundles.md` requires, so ledger rows could be skipped or malformed. |
| Triage and recheck | `bug-triage`, `fix-verifier` | `triage-bug`, `verify-fix` | Overlapping trigger phrases ("is this a bug", "is D1 fixed"). The `snagly:` namespace helps, but routing could pick the wrong one. |
| Browser flows | `flow-runner`, `start-testing` | `browser-check`, `test-nightjar` | Duplicates our existing skills. |
| Test design | `test-case-writer`, `test-plan`, `scenario-mapper` | `write-test-cases`, which has a checker script | Duplicate. Ours validates its output and Snagly's doesn't. |
| Filing guardrails | Convention-only "get a nod" | `.claude/settings.json` forces a permission prompt on `tracker.py create` and `comment` | Snagly has nothing equivalent for our tracker. |

Many of the 30 skills also don't suit NightJar. It's a small single-page FastAPI wellness app. `seo-audit`, `i18n-audit`, `link-audit`, `figma-compare`, `email-verification` and `auth-session-audit` have little to test here.

### Possibly useful

- **`accessibility-audit`** (axe-core plus manual checks) is the clearest gap. We have no a11y check.
- **`visual-snapshot` and `visual-regression`** could cover the nudge banner.
- **`form-fuzzing`** fits the night-logging form, especially timezone and DST-adjacent inputs.
- **`cross-browser-matrix`** is optional.

## Recommendation

1. **Don't run `/plugin install snagly@snagly`.** It installs all 30 skills and the Jira client, and it adds the routing overlap.
2. **If the team wants a pilot, cherry-pick.** Copy only `accessibility-audit`, `form-fuzzing` and `visual-snapshot`, plus `browser-safety` which they reference, into a scratch location first. Leave out `jira-connector`, `bug-creator`, `bug-analyzer`, `bug-triage` and `fix-verifier`.
3. **Pin the npm tools** (axe-core, `@playwright/cli`) to reviewed versions.
4. **Route findings through `triage-bug`.** Snagly skills should report findings only. Bugs should still become `bugs/D-n-…` bundles through `triage-bug`, and filing should still go through `/file-bug`.
5. **Don't point any Snagly skill at `bugs/`.** Send their run artifacts to a different gitignored directory.
6. **Re-review on every version bump.** The skills are instructions, and an update changes what the agent does.
7. **Ask the maintainer.** If the maintainer is someone we can reach, ask for a tracker-agnostic bug-creator, or write our own thin adapter for `tracker.py`.

## Open questions for the team

- Is Jira planned to replace the local tracker? If so, the Jira trio becomes relevant and deserves a deeper review: a real Jira sandbox run and a check of the `attach` risk above.
- Is accessibility in scope for this wellness app? If not, the case for the pilot is weak.
