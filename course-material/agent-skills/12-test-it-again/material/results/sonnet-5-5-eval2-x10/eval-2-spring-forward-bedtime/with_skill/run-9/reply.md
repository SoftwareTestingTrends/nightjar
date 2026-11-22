It's a bug, but a narrow one. I've confirmed it, written a repro and recorded it as D-1.

**Why it happens.** On 8 March 2026 Toronto clocks jump from 02:00 to 03:00, so 02:30 never happens that night. `local_input_to_aware` (`src/nightjar/diary.py:151`) accepts it anyway and treats it as 02:30 at the old UTC−5 offset. That is 03:30 on the new clock. The stored instant is a valid one, so nothing is corrupted. You typed one time and the diary showed another, with no message.

**What should happen is unspecified.** No requirement or story covers a nonexistent local time. I wrote "Not specified" under Expected, with a question for product:
- reject the input,
- accept it and tell the user it was moved to 03:30, or
- keep shifting it silently.

The repro treats "rejected" or "shows 02:30" as fixed. If product picks the "tell the user" option, the repro needs updating.

**Repro.** It exits 1 on all 3 runs, using a throwaway database. The bundle is `bugs/D-1-dst-gap-bedtime-shifted/` (`repro.py` and `report.md`), plus a new `bugs/ledger.md` with status `confirmed` and tracker `not filed`.

```
uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py
```

Filing changes something the team sees, so I haven't done it. To file it, run:

```
/file-bug bugs/D-1-dst-gap-bedtime-shifted
```