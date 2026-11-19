-- Remove duplicate nights from the March import.
-- Duplicate = same bedtime_utc, wake_time_utc and timezone. Keeps the lowest id.
-- If duplicates carry different non-empty notes, they are merged into the kept row first.
-- Back up the database first, then: sqlite3 <db> < scripts/dedupe_march_import.sql
BEGIN;

UPDATE nights SET notes = (
    SELECT group_concat(n, char(10)) FROM (
        SELECT DISTINCT d.notes AS n FROM nights d
        WHERE d.bedtime_utc = nights.bedtime_utc
          AND d.wake_time_utc = nights.wake_time_utc
          AND d.timezone = nights.timezone AND d.notes <> ''
        ORDER BY d.id)
)
WHERE id IN (SELECT MIN(id) FROM nights GROUP BY bedtime_utc, wake_time_utc, timezone HAVING COUNT(*) > 1)
  AND EXISTS (SELECT 1 FROM nights d
       WHERE d.bedtime_utc = nights.bedtime_utc
         AND d.wake_time_utc = nights.wake_time_utc
         AND d.timezone = nights.timezone AND d.notes <> '');

DELETE FROM nights WHERE id NOT IN (
    SELECT MIN(id) FROM nights GROUP BY bedtime_utc, wake_time_utc, timezone);

COMMIT;
