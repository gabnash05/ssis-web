from pathlib import Path
from sqlalchemy import text
from .database import get_connection, execute_sql


def bootstrap_schema_if_needed() -> None:
    """Load and execute db/db.sql if core tables are missing."""
    result = execute_sql(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'students'
        ) AS exists;
        """
    )

    if not result or result.scalar():
        return

    schema_path = Path(__file__).parent / "db.sql"
    sql = schema_path.read_text(encoding="utf-8")
    conn = get_connection()

    for statement in [s.strip() for s in sql.split(";") if s.strip()]:
        conn.execute(text(statement))

    conn.commit()
