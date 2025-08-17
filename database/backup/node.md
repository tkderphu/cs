
# Data backup

In PostgreSQL, a backup is a copy of your database (or its parts) that you can restore later in case of:

- Data loss

- Corruption

- Mistakes (like accidental DROP)

- Migration to another server


#  Types of Backups in PostgreSQL

# 1. Logical Backup (via pg_dump)

- Exports the data and structure as SQL commands or a custom format.

- Restored using psql or pg_restore.

```
pg_dump -U postgres -F c -b -v -f backup_file.backup mydb
```

| Tool                  | Command to Restore |
| --------------------- | ------------------ |
| `pg_dump` (custom)    | `pg_restore`       |
| `pg_dump` (plain SQL) | `psql`             |

# 2. Physical Backup (via pg_basebackup)

Backs up the actual database files.

Includes everything (data, indexes, WAL logs, etc.)

```
pg_basebackup -U replication_user -D /backups/mydb -F tar -z -P
```

- Best for: Large databases, replication, point-in-time recovery (PITR)

#  3. Continuous Archiving + WAL Files

You archive WAL (Write-Ahead Logs) to allow Point-in-Time Recovery (PITR).

Requires:

- archive_mode = on

- archive_command = 'cp %p /your/archive/%f'

- Best for: Enterprise setups needing high recovery flexibility

| Scenario                        | Backup Helps You               |
| ------------------------------- | ------------------------------ |
| You accidentally delete a table | Restore from last backup       |
| Hardware failure                | Restore full DB to new machine |
| Move data to new server         | Use `pg_dump` + `pg_restore`   |
| Upgrade PostgreSQL version      | Dump from old, restore to new  |

# Summary

| Method   | Tool                     | Use When                        |
| -------- | ------------------------ | ------------------------------- |
| Logical  | `pg_dump` / `pg_restore` | Portability, partial restore    |
| Physical | `pg_basebackup`          | Replication, full binary copy   |
| PITR     | WAL Archiving            | Need restore to a specific time |
