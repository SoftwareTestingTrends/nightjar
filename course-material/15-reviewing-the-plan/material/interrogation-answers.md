**What could break**

- **Existing databases.** `CREATE TABLE IF NOT EXISTS` won't add the new column. Without the migration, `user()` and `save_user()` fail on any database created before this change. The `user_settings` table is the only place this can break, but it affects every existing user.
- **Settings saves silently resetting the lead.** `/settings` builds a fresh `User` from the form. If it doesn't carry the saved lead over, every zone or quiet-hours save puts the lead back to 45. No error would show.
- **Positional SQL.** `INSERT OR REPLACE ... VALUES (1, ?, ?, ?, ?)` fails or shifts values once there is a fifth column.
- **Coach versus nudge.** The mock says "45 minutes" while the nudge says 30 or 60. That is why step 6 exists.
- **Quiet hours.** A longer lead can move a nudge into or out of quiet hours. It is never skipped, but the silent flag can change for users who don't touch quiet hours. That is the D1 assumption.
- **DST gap (C4).** Once a year, for bedtimes around 02:30–04:00, the nudge can land at or after bedtime. The existing tests only cover the 45-minute case.
- **Mid-evening change (C3).** Switching to 60 at 22:05 when the nudge was 22:15 loses tonight's nudge.
- **Documents.** This is a real requirement change to PR-21 and S-114, and approval isn't confirmed (D3).

**Riskiest step: step 3, `diary.py`**

It touches stored user data, and a mistake there can break startup or settings for people who already have data. It also has the least test coverage in the current suite, because nobody has tested an old-schema database before. The fix is T-114-9: build a database with the old schema, open it with the new code, and check that it reads 45 and that a later save keeps the chosen lead. I'd write that test before the migration code.

The runner-up is the `/settings` handler in step 5. Its failure is silent, and T-114-8's "zone-only save keeps the lead" case covers it.

The scheduling change itself (step 4) is low risk. It's a one-line swap, and the existing DST tests guard it.

**Alternatives I didn't take**

- **Subtract the lead from the bedtime instant** instead of the local clock time. It would be more correct on DST-gap nights, but it contradicts the "usual local bedtime" model behind AC1/AC2 and their tests. The spec rejects it, and I agree.
- **Clamp the nudge to before bedtime** to fix C4. It adds new behaviour that Product hasn't asked for. It can be a follow-up.
- **Quiet hours judged against the usual bedtime** (D1 option b). This makes quiet hours independent of the lead, but it needs a new definition and new tests. I kept the current rule, which needs no new code.
- **Lead-aware nudge copy** ("starts in 30 minutes"). Copy changes need Regulatory & Brand review, and editing the register is forbidden as a workaround. The three existing templates mention no minutes, so I left them alone.
- **Pass the lead to the coach** (spec option 2 in 3.4). It widens the data flow into `build_user_message`. I chose a number-free mock instead. One thing to check: this fixes only the mock. The real Claude coach is never told 45, but I haven't confirmed that nothing in `system.md` hints at a timing number. I'd grep for that before step 6.
- **A table for settings** or a `timedelta` field. Plain integer minutes keep the form, JSON and SQL simple.
- **Reset to 45 on an empty form field.** This is simpler, but it breaks the existing API tests, which post without the field, and it causes the silent-reset problem above.

The plan's biggest unknown is that I haven't run the baseline. I'm relying on CLAUDE.md for "66 passed", so running `make test` first is the first thing I'd do after approval.
