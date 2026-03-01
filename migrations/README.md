# Migrations

This directory contains all database migration files and tools.

## Structure

- `migrations.sql` - Single migration file containing the complete current database schema
- `migrate.sh` - Shell script for applying migrations
- `migrate.py` - Python script for applying migrations
- `archive/` - Directory for storing old migration backups (if needed)

## Usage

### From Project Root

The `migrate` wrapper script in the project root allows you to run migrations from anywhere in the project:

```bash
# Check migration status
./migrate status

# Apply migrations (only if changed)
./migrate apply
```

### From migrations/ Directory

You can also run the migration scripts directly from this directory:

```bash
# Using shell script
./migrate.sh status
./migrate.sh apply

# Using Python script
python migrate.py status
python migrate.py apply
```

## How It Works

1. **Single File Approach**: Only one `migrations.sql` file exists at any time
2. **Checksum Tracking**: The system calculates an MD5 checksum of `migrations.sql`
3. **Smart Application**: Migration is only applied if the checksum has changed
4. **Version Tracking**: Applied migrations are tracked in the `migration_version` table

## Making Schema Changes

1. Edit `migrations.sql` with your changes
2. Test locally by running `./migrate apply` (or from root: `./migrate apply`)
3. If satisfied, commit the updated `migrations.sql` file
4. Deploy - the migration will detect the new checksum and apply automatically

## Configuration

Database credentials are loaded from `../.env` file:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5434
DATABASE_NAME=Jacked-DB
DATABASE_USER=jacked
DATABASE_PASSWORD=jackedpass
POSTGRES_CONTAINER_ID=<container_id>
```
