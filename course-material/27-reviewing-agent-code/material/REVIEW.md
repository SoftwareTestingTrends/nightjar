# NightJar review policy

Review the change in passes. For each finding give the file and line, what's wrong, and a severity: Important or Nit.

1. **Bugs and logic:** wrong results, off-by-one windows, time zone and DST mistakes.
2. **Error handling:** empty input, missing data, bad input, failure paths.
3. **Spec compliance and assumptions:** where the request was ambiguous, which reading did the change pick, did it say so, and who should decide?
4. **Consistency with the existing code:** does it duplicate or contradict logic that already exists, so the product could show a user two different answers?
5. **Tests:** do the tests check the behaviour that matters, or only the example in the request?
6. **Dependencies:** any new package must exist, be maintained, and be pinned.

Skip formatting and anything `make lint` already checks.
