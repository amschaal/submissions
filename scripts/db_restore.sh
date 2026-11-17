#!/usr/bin/env bash
# Restore a dump into the dev Postgres database, REPLACING its current contents.
#
# Run inside the api container, which has the SQL_* vars from .env.dev:
#   docker compose -f docker-compose-dev.yml exec api scripts/db_restore.sh [-y] <dumpfile>
#
#   -y        Skip the confirmation prompt.
#   dumpfile  A pg_dump archive (custom, tar or directory format) or a plain .sql file.
#
# The public schema is dropped and recreated first, so tables that aren't in the
# dump don't linger. Ownership and grants are skipped (--no-owner --no-privileges),
# so dumps from prod or other machines restore even when their roles don't exist here.
set -euo pipefail

usage() { echo "Usage: $0 [-y] <dumpfile>" >&2; exit 2; }

yes=0
if [[ "${1:-}" == "-y" ]]; then yes=1; shift; fi
[[ $# -eq 1 ]] || usage
dump="$1"
[[ -e "$dump" ]] || { echo "No such file: $dump" >&2; exit 1; }

: "${SQL_HOST:?SQL_HOST is not set - run this inside the api container}"
export PGHOST="$SQL_HOST" \
       PGPORT="${SQL_PORT:-5432}" \
       PGUSER="${SQL_USER:-user}" \
       PGPASSWORD="${SQL_PASSWORD:-}" \
       PGDATABASE="${SQL_DATABASE:-postgres}"

if [[ $yes -eq 0 ]]; then
  read -r -p "This will WIPE $PGDATABASE@$PGHOST:$PGPORT and restore $dump. Continue? [y/N] " reply
  [[ "$reply" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 1; }
fi

echo "Resetting public schema..."
psql -X -q -v ON_ERROR_STOP=1 <<'SQL'
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
SQL

echo "Restoring $dump..."
status=0
if pg_restore --list "$dump" >/dev/null 2>&1; then
  pg_restore --no-owner --no-privileges --dbname="$PGDATABASE" "$dump" || status=$?
else
  psql -X -q -f "$dump" || status=$?   # plain SQL dump
fi

if [[ $status -ne 0 ]]; then
  echo "Restore finished with errors (see above). The database may be incomplete." >&2
  exit "$status"
fi
echo "Done. If the dump is older than your code, run: python manage.py migrate"
