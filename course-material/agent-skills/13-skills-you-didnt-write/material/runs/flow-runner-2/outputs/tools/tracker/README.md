# NightJar's bug tracker

A small local tracker that stands in for Jira in the course. Issues have keys
like `NJ-12`, a summary, a description, a status and comments.

```bash
make tracker                       # start it with the seed issues
cat ~/.nightjar-tracker/tokens.json   # created on first start, kept after that
export NJ_TRACKER_TOKEN=<read or write token>
python3 tools/tracker/tracker.py search import csv
python3 tools/tracker/tracker.py get NJ-12
```

- **Two tokens.** The read token can search and read. Only the write token can
  create issues or add comments (the server answers 403 otherwise).
- **Search** returns issues whose summary or description contain every word
  you give (a word matches the start of a word, so `import` finds `imported`).
- **Data and tokens** live in `~/.nightjar-tracker/` (or `$NJ_TRACKER_HOME`), outside the
  repository.
