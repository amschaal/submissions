#!/usr/bin/env bash
# Dump the dev Postgres database to a custom-format (-Fc) archive.
#
# Run inside the api container, which has the SQL_* vars from .env.dev:
#   docker compose -f docker-compose-dev.yml exec api scripts/db_dump.sh [name]
#
#   name  Optional. Defaults to coreomics_<YYYY-MM-DD_HHMMSS>.
#         ".dump" is appended when the name has no extension.
#         A bare name is written to $DUMP_DIR (default: <repo>/dumps);
#         a name containing "/" is used as the output path as-is.
#
# Restore with scripts/db_restore.sh <file>.
set -euo pipefail

: "${SQL_HOST:?SQL_HOST is not set - run this inside the api container}"
export PGHOST="$SQL_HOST" \
       PGPORT="${SQL_PORT:-5432}" \
       PGUSER="${SQL_USER:-user}" \
       PGPASSWORD="${SQL_PASSWORD:-}" \
       PGDATABASE="${SQL_DATABASE:-postgres}"

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
name="${1:-coreomics_$(date +%Y-%m-%d_%H%M%S)}"
[[ "$name" == *.* ]] || name="$name.dump"
if [[ "$name" == */* ]]; then
  out="$name"
else
  out="${DUMP_DIR:-$repo_dir/dumps}/$name"
fi

if [[ -e "$out" ]]; then
  echo "Refusing to overwrite existing file: $out" >&2
  exit 1
fi
mkdir -p "$(dirname "$out")"

echo "Dumping $PGDATABASE@$PGHOST:$PGPORT -> $out"
if ! pg_dump --format=custom --file="$out" "$PGDATABASE"; then
  rm -f "$out"
  echo "pg_dump failed. Client: $(pg_dump --version);" \
       "server: $(psql -XtAc 'show server_version' 2>/dev/null || echo unknown)." \
       "pg_dump must be the same major version as the server or newer." >&2
  exit 1
fi
echo "Done: $out ($(du -h "$out" | cut -f1))"
