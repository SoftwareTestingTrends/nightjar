Yes, it reproduces, but the 03:30 itself is correct. The defect is that the diary changes your input and doesn't tell you.

On 8 March 2026 Toronto clocks jump from 02:00 to 03:00, so 02:30 never happened that night. NightJar tags your input with the pre-jump offset (−05:00), which is 07:30 UTC, which is 03:30 EDT. The app gives no error or warning.

No requirement says what should happen for a time that doesn't exist. BR-07 only asks for correctness across DST changes. I wrote "Not specified" under Expected and added a question for product: reject it, shift it with a notice, or something else.

I ran `repro.py` three times, and each run exited 1, printing `BUG: entered 02:30, diary shows 03:30, with no warning`. It exits 0 if the input is rejected with an error or shown as entered. Product's answer may change what "fixed" means.

Files, in `bugs/` (gitignored):
- `bugs/D-1-dst-gap-bedtime/repro.py`
- `bugs/D-1-dst-gap-bedtime/report.md`
- `bugs/ledger.md`, with D-1 as `confirmed`, tracker `not filed`

You asked for `bugs/<short-name>/repro.py`. I used `bugs/D-1-dst-gap-bedtime/` because `docs/bug-bundles.md` requires that folder name.

I haven't filed it, because filing is visible to the team. To file it, run:

`/nightjar-qa:file-bug bugs/D-1-dst-gap-bedtime`