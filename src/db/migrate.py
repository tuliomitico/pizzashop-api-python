import sys
import re

from yachalk import chalk
from connection import engine
from pathlib import Path

MIGRATION_DIR = Path(__file__).parent.parent.parent.resolve() / 'sqlalchemy/scripts'

migration_files = MIGRATION_DIR.glob("000*.sql")

with engine.connect() as conn:
    for migration_file in migration_files:
        with migration_file.open(mode='r') as file:
            sql_script = file.read()
        partes_sql = re.split(r';\s*$', sql_script, flags=re.MULTILINE)

        for parte in partes_sql:
            if parte.strip():  
                conn.execute(parte)

print(chalk.green_bright("Migrations applied sucessfully!"))

sys.exit()