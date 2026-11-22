It isn't a bug in this repo, so I didn't write a `repro.py`.

I tried the same save path you used, with quiet hours from 21:00 to 00:00, against a throwaway database:

- `POST /settings` with `quiet_start=21:00` and `quiet_end=00:00` returns 303 (saved). The stored value is `00:00:00`.
- The page renders after the save (200), with `00:00` in the form.
- The quiet-hours logic treats 21:00 to 00:00 correctly: 20:59 is not quiet, 21:00 through 23:59 are quiet, and 00:00 is not.
- Other end times such as 23:59 and 07:00 save fine too.

The server-side code can't produce "Invalid time". The only validation error the settings handler returns is Python's `Invalid isoformat string` from `time.fromisoformat`, and that doesn't fire for `00:00`. The phrase "Invalid time" appears nowhere in `src/`. The template has no client-side validation either.

The tracker has an issue for this, `tools/tracker/seed.json` (line 46, "[Settings] Quiet hours can't end at midnight"). It describes the same symptom, but the code I checked doesn't reproduce it.

Possible explanations, which I couldn't check from here:
- The app you're using runs a different build or an older commit. `git status` is clean at `b519b92`.
- The problem is in the browser UI, for example a locale or the time-picker widget, or a browser extension. My check bypassed the browser.
- The seeded ticket is stale.

If you can tell me the exact steps and the browser (or send the page's error text or a screenshot), I can run `browser-check` on the live app. Nothing in the repo changed. My probe script is in `/tmp/nj-scratch/`, outside the repo.