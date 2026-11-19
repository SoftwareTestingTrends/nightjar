The silent-state nudge panel now matches `design/mock-nudge-silent.png`. My last screenshot lines up with the mock on layout, pill size, colours and panel height.

- **Template:** in `src/nightjar/templates/index.html`, "Delivered silently (quiet hours)." is replaced by a "Silent · quiet hours" pill next to the time in the heading. The pill keeps `data-testid="nudge-silent"`, so the existing API test still finds it.
- **Styles:** `src/nightjar/static/style.css` has a new `.pill` rule: moon-yellow outline, 999px radius, 18px text.
- **Checks:**
  - `make test`: `68 passed, 1 deselected`
  - `make e2e`: `1 passed, 68 deselected`
  - `make lint`: fails with 5 errors, all in `scripts/screenshot_nudge.py`, an untracked file I didn't touch. They are an import-order issue, long lines and one more. I left them alone.

I only compared the silent state. I didn't screenshot `loud` or `cold`, though those render without the pill.
