import os
import subprocess
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

db_user = os.getenv("DB_USERNAME", "postgres")
db_password = os.getenv("DB_PASSWORD", "")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "ssis_web")

env = os.environ.copy()
env["PGPASSWORD"] = db_password

base_dir = Path(__file__).parent
setup_sql = base_dir / "setup.sql"
schema_sql = base_dir / "app" / "db" / "schema.sql"

# 1. System setup (run on default 'postgres' db)
subprocess.run([
    "psql",
    "-U", db_user,
    "-h", db_host,
    "-p", db_port,
    "-d", "postgres",
    "-f", str(setup_sql)
], env=env, check=True)

# 2. Schema setup (run on new database)
subprocess.run([
    "psql",
    "-U", db_user,
    "-h", db_host,
    "-p", db_port,
    "-d", db_name,
    "-f", str(schema_sql)
], env=env, check=True)

print("[✓] Database, user, and schema setup completed")
