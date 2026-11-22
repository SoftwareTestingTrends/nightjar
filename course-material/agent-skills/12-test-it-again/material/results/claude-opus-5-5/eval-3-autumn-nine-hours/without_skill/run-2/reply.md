This isn't a bug, so I didn't write a repro script.

In 2026, Toronto's clocks went back an hour at 02:00 on Sunday 1 November: daylight time (EDT, UTC−4) ended and standard time (EST, UTC−5) began. That falls inside your night, so 02:00 to 03:00 happened twice:

- Bedtime 23:00 EDT on Sat 31 Oct = 03:00 UTC
- Wake 07:00 EST on Sun 1 Nov = 12:00 UTC
- Real time between them: **9 hours**

The clock only moved forward 8 hours, but 9 hours actually passed. NightJar works it out correctly: `Night.duration` (`src/nightjar/models.py:52`) converts both times to UTC before subtracting. I ran that night through the real code and got offsets of −4h at bedtime, −5h at wake, and a duration of `9:00:00`.

A naive wall-clock calculation would show 8h. That would be the bug, and the project notes warn against it.

The opposite happens on the spring-forward night (8 March 2027): 23:00 to 07:00 will show 7h, and that will be correct too.