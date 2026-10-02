# Claims policy

NightJar is a wellness product. It may help people relax and keep a regular
routine. It may not claim to diagnose, treat or cure any condition.

The source of truth is [`claims/register.yaml`](../claims/register.yaml), owned by
Regulatory & Brand (fictional). It holds:

- **approved_phrases**: wellness language we may use ("wind down", "relax",
  "build a consistent bedtime routine", ...).
- **nudge_copy**: the only templates the bedtime nudge may show (S-114 AC4).
- **banned**: regular expressions for disease and treatment claims ("insomnia",
  "sleep apnea", "treat", "cure", "diagnose", "anxiety disorder", "prescribe",
  "clinically proven").

## How it is enforced

- `claims.check_text(text) -> list[Violation]` is case-insensitive and uses word
  boundaries ("retreat" is fine, "treat" is not).
- Nudge copy is picked only from `nudge_copy`.
- Every coach answer goes through `check_text`. If it finds a violation, the user
  sees a safe fallback instead, and the violation is logged and written to the trace.

## Known trade-offs

The check is deliberately strict. "Treat yourself to a bath" is flagged. That is
acceptable: a false positive shows the fallback; a false negative ships a disease claim.

Changing the register needs Regulatory review. Don't edit it to make a test pass.
