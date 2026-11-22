# `claude plugin validate` results (Claude Code 2.1.328, 2026-11-19)

1. webapp-testing skill copied into NightJar's `.claude/skills/`: `✔ Validation passed`.
2. A skill whose frontmatter has an unclosed quote (`description: "Writes tests`):
   `✘ frontmatter: YAML frontmatter failed to parse: YAML Parse error: Unexpected EOF. At runtime this skill loads with empty metadata (all frontmatter fields silently dropped).`
3. A skill with `name: Write Tests` (capitals and a space; the Agent Skills spec allows only lowercase letters, numbers and hyphens): `✔ Validation passed`. Claude Code is more lenient than the open standard here.
