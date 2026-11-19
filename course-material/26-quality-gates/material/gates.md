# NightJar gates

Every gate has at least one check a machine runs, a named human owner, and the evidence
the owner reads. A machine check can block. Only the owner can approve.

| Gate | When | Machine checks | Owner | Evidence the owner reads |
|---|---|---|---|---|
| Spec ready | `spec.md` before planning | every AC has a test id in `docs/traceability.md` | Product owner | the spec, the traceability rows, routed questions |
| Plan approved | `plan.md` before code | the plan lists the test ids it will add or change | Engineer (architect if high risk) | the plan's risk and proof sections |
| Merge | every pull request | `make test`, `make lint`, traceability check | Code owner | pasted summary lines, the diff, the agent's report |
| Claims | PR touches `claims/register.yaml` or user-facing copy | register changes are flagged; new copy runs through `claims.check_text` | Regulatory & Brand | the diff of the register or copy, and why |
| Coach config | PR touches the coach prompt, model or evals | real-model coach evals and the per-case eval gate | Coach owner | gate output, failing answers |
| Release | before production | `make e2e`; golden evals pass every trial | Release manager | the run log; known issues and their owners |
