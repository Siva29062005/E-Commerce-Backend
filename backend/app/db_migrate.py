"""Lightweight schema patches for dev (create_all does not alter existing tables)."""

from sqlalchemy import inspect, text

from app.database import engine


def run_migrations() -> None:
    insp = inspect(engine)
    if "users" in insp.get_table_names():
        cols = {c["name"] for c in insp.get_columns("users")}
        if "role" not in cols:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(32) NOT NULL DEFAULT 'user'"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_users_role ON users (role)"))

    if "refresh_tokens" not in insp.get_table_names():
        from app.database import Base
        from app.models import RefreshToken  # noqa: F401

        RefreshToken.__table__.create(bind=engine, checkfirst=True)
