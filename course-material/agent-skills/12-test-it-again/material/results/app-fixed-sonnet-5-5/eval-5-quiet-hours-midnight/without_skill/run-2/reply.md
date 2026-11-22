I couldn't reproduce this, so I didn't write a repro script. It doesn't look like a NightJar bug.

- **Settings handler:** I posted quiet hours of 21:00 to 00:00 to `/settings` on a throwaway database. It returned a 303 redirect, and the values were stored and read back as 21:00 and 00:00. The 21:00 to 07:00 control case behaved the same way.
- **Midnight handling:** the code handles a window that wraps past midnight. `in_quiet_hours` in `nudge.py:59` treats an end time before the start time as wrapping.
- **Page validation:** the form (`index.html:50-51`) uses plain `<input type="time">` fields with no extra validation. The only error text in the app comes from the timezone check, which has nothing to do with quiet hours.

I only tested the server. I didn't test the page in a browser, so the error is probably coming from something outside the server code. Possible causes:

- **Time zone field:** a bad value there gives an error that could be mistaken for a quiet-hours one. The server returns it as a 400 with the message from the timezone validation.
- **Browser or OS:** a browser or OS with an unusual time format, such as 12-hour or locale-specific, might handle midnight differently.
- **Old build or stored data:** you may be running an older build, or the database may hold an odd value from earlier.

Could you send me the exact error text and tell me which browser you're using? With that I can try it in a real browser, and I'll write the repro if it fails there.