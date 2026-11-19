"""Create NightJar's three environments in a clone: dev, staging (a copy of production) and production.
Production has a bad import: the 7 March nights were imported twice, and the user later added a note to one copy."""
import shutil, sqlite3, sys
from pathlib import Path
from nightjar.diary import Diary, parse_csv
R = Path(sys.argv[1])
nights = parse_csv((R / "data/sample_nights.csv").read_text(encoding="utf-8"))
for env in ("dev", "prod"):
    p = R / f"nightjar-{env}.db"; p.unlink(missing_ok=True)
    Diary(p).add_nights(nights)
prod = R / "nightjar-prod.db"
with sqlite3.connect(prod) as c:
    c.execute("""INSERT INTO nights (bedtime_utc, wake_time_utc, timezone, notes)
                 SELECT bedtime_utc, wake_time_utc, timezone, notes FROM nights
                 WHERE bedtime_utc >= '2026-03-13' ORDER BY id""")
    dup = c.execute("SELECT max(id) FROM nights WHERE bedtime_utc LIKE '2026-03-16%'").fetchone()[0]
    c.execute("UPDATE nights SET notes = 'Woke up once around 3am, back to sleep quickly.' WHERE id = ?", (dup,))
shutil.copy(prod, R / "nightjar-staging.db")
for env in ("dev", "staging", "prod"):
    with sqlite3.connect(R / f"nightjar-{env}.db") as c:
        print(env, c.execute("select count(*) from nights").fetchone()[0], "nights")
