import os
from pathlib import Path
from urllib.parse import urlparse

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    from dotenv import load_dotenv  # type: ignore
except Exception:  # dotenv is optional
    load_dotenv = None  # type: ignore


def _mask_url_password(url: str) -> str:
    """Return the URL with the password masked to avoid leaking secrets."""
    try:
        p = urlparse(url)
        # If no credentials present, return as-is
        if not p.username and not p.password:
            return url

        username = p.username or ""
        host = p.hostname or ""
        port = f":{p.port}" if p.port else ""

        # Only include password placeholder if a password actually exists
        cred = username
        if p.password:
            cred = f"{username}:****"

        at = "@" if host else ""
        netloc = f"{cred}{at}{host}{port}"
        return p._replace(netloc=netloc).geturl()
    except Exception:
        # Best-effort masking; on failure return the original
        return url


def _build_admin_dsn(app_database_url: str) -> tuple[str, str, str]:
    """
    Build the admin DSN used for creating the target database.

    - If ADMIN_DATABASE_URL is provided, use it (ensuring a database path exists).
    - Otherwise, switch the path of DATABASE_URL to POSTGRES_ADMIN_DB (default: 'postgres').

    Returns a tuple of (admin_dsn, app_db_name, admin_db_name).
    """
    parsed = urlparse(_normalize_psycopg_dsn(app_database_url))
    app_db_name = (parsed.path or "/").lstrip("/")
    if not app_db_name:
        raise ValueError("DATABASE_URL must include a database name")

    admin_override = os.getenv("ADMIN_DATABASE_URL")
    if admin_override:
        admin_parsed = urlparse(_normalize_psycopg_dsn(admin_override))
        admin_db_name = (admin_parsed.path or "/").lstrip("/") or os.getenv("POSTGRES_ADMIN_DB", "postgres")
        if not admin_parsed.path or admin_parsed.path == "/":
            admin_parsed = admin_parsed._replace(path=f"/{admin_db_name}")
        admin_dsn = admin_parsed.geturl()
        return admin_dsn, app_db_name, admin_db_name

    admin_db_name = os.getenv("POSTGRES_ADMIN_DB", "postgres")
    admin_parsed = parsed._replace(path=f"/{admin_db_name}")
    admin_dsn = admin_parsed.geturl()
    return admin_dsn, app_db_name, admin_db_name


def _normalize_psycopg_dsn(url: str) -> str:
    """
    Normalize a URL to a psycopg2-compatible DSN.

    - Accepts SQLAlchemy-style driver URLs like 'postgresql+psycopg2://...'
    - Maps 'postgres://' to 'postgresql://'
    """
    if not url:
        return url
    # Map common variants of the scheme
    if url.startswith("postgres://"):
        return "postgresql://" + url[len("postgres://") :]
    if url.startswith("postgresql+psycopg2://"):
        return "postgresql://" + url[len("postgresql+psycopg2://") :]
    return url


def ensure_database():
    # Load .env if available for convenience (independent of terminal settings)
    if load_dotenv:
        env_path = Path(__file__).resolve().parents[1] / ".env"
        # Prefer the backend/.env next to this script, else fall back to default search
        if env_path.exists():
            load_dotenv(env_path)  # type: ignore
        else:
            load_dotenv()  # type: ignore

    # Support granular PG_* vars like in the working notebook.
    pg_user = os.getenv("PG_USER", "postgres")
    pg_password = os.getenv("PG_PASSWORD", "postgres")
    pg_host = os.getenv("PG_HOST", os.getenv("PGHOST", "localhost"))
    pg_port = os.getenv("PG_PORT", os.getenv("PGPORT", "5432"))
    pg_database = os.getenv("PG_DATABASE", os.getenv("PGDATABASE", "inventory_db"))

    database_url = os.getenv(
        "DATABASE_URL",
        f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}",
    )
    database_url = _normalize_psycopg_dsn(database_url)

    admin_dsn, database_name, admin_db_name = _build_admin_dsn(database_url)

    try:
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

                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name))
                )
                print(
                    f"Database '{database_name}' created successfully using admin DB '{admin_db_name}'"
                )
    except psycopg2.OperationalError as e:
        masked = _mask_url_password(admin_dsn)
        raise SystemExit(
            "Failed to connect to admin database using DSN: "
            f"{masked}\n"
            "Tip: set ADMIN_DATABASE_URL or POSTGRES_ADMIN_DB, and verify credentials.\n"
            f"Original error: {e}"
        )


if __name__ == "__main__":
    ensure_database()
