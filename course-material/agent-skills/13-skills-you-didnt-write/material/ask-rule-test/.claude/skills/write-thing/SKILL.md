---
name: write-thing
description: Runs the write step for the ask-rule test. Use when asked to run the write step.
allowed-tools: Bash(python3:*)
---
Run exactly this command, then report its output word for word:

python3 -c "import sys; print('wrote', sys.argv[1:])" --apply
