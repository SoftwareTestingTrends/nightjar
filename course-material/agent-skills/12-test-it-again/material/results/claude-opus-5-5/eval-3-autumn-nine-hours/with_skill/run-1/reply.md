This isn't a bug, so I didn't write `repro.py`, a bundle, or a ledger row.

**Why 9 hours is right:** Daylight saving time ended in Toronto at 02:00 on Sunday 1 November 2026, which falls during that night. The clocks went back an hour, so 02:00 to 03:00 happened twice. From 23:00 to 07:00 on the clock is therefore **9 hours of real time**:

- Bedtime 23:00 EDT is 03:00 UTC.
- Wake 07:00 EST is 12:00 UTC.
- That's 9:00:00 apart.

**This is what the spec asks for.** Story S-116 says: *"Durations are real elapsed time, so a night that crosses a daylight-saving change is an hour shorter or longer on the clock."* `Night.duration` in `src/nightjar/models.py:52` subtracts the two times in UTC on purpose to get this.

**What I ran:** I submitted that night through the app's `POST /nights` form against throwaway databases, 3 times. All 3 stored 03:00Z to 12:00Z and the diary showed `9h 00m`, which matches the spec.

**Optional idea for product, not a defect:** this will come up again every November and March. A small note on nights that cross a DST change (e.g. "clocks went back, +1h") could stop people reporting it as a bug.

**Cleanup:** I couldn't delete my throwaway files because they're just outside the repo and the permission check blocked it. Nothing in the repo or `nightjar.db` was touched. Please remove them yourself:

```
rm /private/var/folders/v6/1_8wxb8d1sx70bp7bfp80z8r0000gn/T/tmp.QWyQ2W8C4i/nightjar_triage_{try.py,db1.sqlite,db2.sqlite,db3.sqlite}
```