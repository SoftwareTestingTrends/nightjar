---
name: file-bug
description: Files a NightJar bug in the team's tracker. Searches for duplicates first, drafts the ticket from a template, and files it only after a person approves the draft. Use when someone runs /file-bug with a finding (a failed check, a browser-check report, or a defect they describe). Not for investigating why something fails, and not for writing test cases.
disable-model-invocation: true
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: '"${CLAUDE_PROJECT_DIR}"/.claude/skills/file-bug/scripts/check_filing.py'
---

# File a bug

A ticket is read by people who weren't there when you found the bug, and once it's
filed the whole team sees it. Two tickets for one bug split the discussion, and a
ticket nobody can reproduce gets closed. These rules come first.

## Rules

- **A person approves every ticket and comment.** Show the draft and stop. File only
  after they say yes in this conversation. NightJar's project settings also ask
  before any `tracker.py create` or `tracker.py comment` runs.
- **Search before you draft.** At least two searches, with different words.
- **Nothing private leaves the machine.** No real names, email addresses, tokens or
  real journal notes. Use the test data from your reproduction.

## Steps

1. Reproduce the finding, or point to evidence that does: a browser-check report,
   a failing test, or a command and its output. If you can't reproduce it, say so
   and stop. Don't draft a ticket.
2. Search for duplicates: `python3 tools/tracker/tracker.py search <words>`. Search
   at least twice with different words: the symptom, the feature, and the words a
   user would use. Open every close match with `get`.
   - Same bug, still open: don't create a ticket. Draft a comment with your new
     evidence instead.
   - Same bug, Done: it came back. Draft a new ticket with "Regression of NJ-n" in
     the summary.
   - Related but different: draft a new ticket that names the related key.
   - Nothing close: draft a new ticket.
3. Write the draft to `bug-drafts/<short-name>.md`, following
   `${CLAUDE_SKILL_DIR}/assets/bug-template.md`. The summary is
   `[Area] symptom when condition`, specific enough that the next person's search
   finds it. For the expected result, quote the requirement or story. If none says,
   write "Not specified" and add it under Notes as a question for product.
4. Show the draft and what your searches found, ask "File this?", and stop.
5. After a yes, run `python3 tools/tracker/tracker.py create --draft bug-drafts/<short-name>.md`
   (or `comment NJ-n --draft …`). A hook checks the draft first. If it blocks, fix
   what it names and show the draft again.
6. Report the new key, or the key you commented on.
