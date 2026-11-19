
## Environments

| Environment | Database | Who may change it |
|---|---|---|
| dev | `nightjar-dev.db` | anyone, including agents |
| staging | `nightjar-staging.db`, a copy of production data | agents, to rehearse a change |
| production | `nightjar-prod.db` | only the release manager, after a backup |

Don't change production yourself. Prepare the change as a script, rehearse it on staging,
and hand it to the release manager with the results.
