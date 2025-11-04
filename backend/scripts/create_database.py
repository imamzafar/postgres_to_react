import os
from urllib.parse import urlparse

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def ensure_database():
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/inventory_db",
    )
    parsed = urlparse(database_url)
    database_name = parsed.path.lstrip("/")

    if not database_name:
        raise ValueError("DATABASE_URL must include a database name")

    admin_db = os.getenv("POSTGRES_ADMIN_DB", "postgres")
    admin_url = parsed._replace(path=f"/{admin_db}")
    # psycopg2 does not understand the params attribute directly, so rebuild URL.
    admin_dsn = admin_url.geturl()

    with psycopg2.connect(admin_dsn) as connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (database_name,),
            )
            exists = cursor.fetchone()
            if exists:
                print(f"Database '{database_name}' already exists")
                return

            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))
            print(f"Database '{database_name}' created successfully")


if __name__ == "__main__":
    ensure_database()
