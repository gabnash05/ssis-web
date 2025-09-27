from pathlib import Path
from .database import execute_sql

def bootstrap_schema_if_needed() -> None:
    """
    Load and execute db/schema.sql if core tables are missing.
    Checks for existence of key tables before bootstrapping.
    """
    # Check if any core tables exist (you can check multiple tables)
    result = execute_sql(
        """
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('students', 'colleges', 'programs')
            LIMIT 1
        ) AS tables_exist;
        """
    )

    # If tables already exist, skip bootstrap
    if result and result.scalar():
        print("[✓] Database tables already exist, skipping bootstrap")
        return

    print("[!] Bootstrapping database schema...")

    # Path to schema file (now in the same db directory)
    schema_path = Path(__file__).parent / "schema.sql"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    sql_content = schema_path.read_text(encoding="utf-8")

    try:
        # Split into individual statements
        statements = [s.strip() for s in sql_content.split(";") if s.strip()]

        for i, statement in enumerate(statements, 1):
            print(f"  Executing statement {i}/{len(statements)}...")
            execute_sql(statement)

        print("[✓] Database schema bootstrap completed successfully")

    except Exception as e:
        print(f"[!] Error bootstrapping schema: {e}")
        raise
