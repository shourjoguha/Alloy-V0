#!/bin/bash

set -e

load_env() {
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    if [ -f "$script_dir/../.env" ]; then
        export $(cat "$script_dir/../.env" | grep -v '^#' | xargs)
    fi
    DATABASE_HOST="${DATABASE_HOST:-localhost}"
    DATABASE_PORT="${DATABASE_PORT:-5432}"
    DATABASE_NAME="${DATABASE_NAME:-Jacked-DB}"
    DATABASE_USER="${DATABASE_USER:-jacked}"
    DATABASE_PASSWORD="${DATABASE_PASSWORD:-jackedpass}"
    POSTGRES_CONTAINER_ID="${POSTGRES_CONTAINER_ID}"
}

show_migration_status() {
    docker exec "${POSTGRES_CONTAINER_ID}" psql -U "${DATABASE_USER}" -d "${DATABASE_NAME}" \
        -c "SELECT version, description, applied_at FROM migration_version ORDER BY applied_at DESC;"
}

get_file_checksum() {
    local file="$1"
    md5sum "$file" | awk '{print $1}'
}

is_migration_applied() {
    local checksum="$1"
    local result
    result=$(docker exec "${POSTGRES_CONTAINER_ID}" psql -U "${DATABASE_USER}" -d "${DATABASE_NAME}" \
        -t -c "SELECT EXISTS(SELECT 1 FROM migration_version WHERE checksum = '${checksum}');")
    echo "$result" | tr -d ' ' | grep -q '^t$'
}

apply_migration() {
    local migration_file="$1"
    local checksum
    checksum=$(get_file_checksum "$migration_file")
    
    echo "Applying migration: $migration_file"
    echo "Checksum: $checksum"
    
    if is_migration_applied "$checksum"; then
        echo "Migration already applied (matching checksum)"
        show_migration_status
        return 0
    fi
    
    docker exec -i "${POSTGRES_CONTAINER_ID}" psql -U "${DATABASE_USER}" -d "${DATABASE_NAME}" < "$migration_file"
    
    local version
    version=$(basename "$migration_file" .sql)-$(date +%Y%m%d%H%M%S)
    
    docker exec "${POSTGRES_CONTAINER_ID}" psql -U "${DATABASE_USER}" -d "${DATABASE_NAME}" \
        -c "INSERT INTO migration_version (version, description, checksum) VALUES ('$version', '$migration_file', '$checksum');"
    
    echo "Migration applied successfully!"
    show_migration_status
}

main() {
    load_env
    
    if [ -z "$POSTGRES_CONTAINER_ID" ]; then
        echo "ERROR: POSTGRES_CONTAINER_ID not set in .env"
        exit 1
    fi
    
    case "${1:-}" in
        status)
            echo "Current migration status:"
            show_migration_status
            ;;
        apply)
            local script_dir
            script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
            local migration_file="$script_dir/migrations.sql"
            
            if [ ! -f "$migration_file" ]; then
                echo "ERROR: migrations.sql not found at $migration_file"
                exit 1
            fi
            apply_migration "$migration_file"
            ;;
        *)
            echo "Usage: $0 [status|apply]"
            echo ""
            echo "Commands:"
            echo "  status  - Show current migration status"
            echo "  apply   - Apply migrations.sql file"
            exit 0
            ;;
    esac
}

main "$@"
