This isn't a bug, so I didn't write a repro script, a bundle or a ledger row.

I logged a 00:15 bedtime on Sunday 15 Nov 2026 in `America/Toronto`. The diary shows it as `Sat 14 Nov`, which matches what you saw.

The diary's date column is the night's "night of" date, meaning the evening the night began. It is not the calendar date of the bedtime. This is deliberate and documented in several places:
- `src/nightjar/models.py:43-45` computes it as local bedtime minus 12 hours. Its docstring says "a 00:15 bedtime on Sunday is Saturday night."
- `tests/test_diary.py:81` is a test that pins this behaviour.
- `docs/stories/S-116.md:17-18` says a 00:15 bedtime on Sunday counts as Saturday night.
- Test case TC-116-8 in `.claude/skills/write-test-cases/SKILL.md` uses this exact example and expects Sat 14 Nov.

The "night of" date is also what the 7-day summary and the coach use, so showing Sunday would break those.

If the date column is confusing, the wording is the issue, not the date logic. A header like "Night of" or a tooltip would help, and that's a UX suggestion rather than a defect. I haven't changed anything.