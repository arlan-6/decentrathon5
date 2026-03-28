from collections.abc import Iterator
import uuid

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from core.config import DATABASE_URL


engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from models.item import Item
    from models.user import User
    _ = (Item, User)
    Base.metadata.create_all(bind=engine)
    _sync_users_schema()
    from models.refresh_token import RefreshToken
    _ = RefreshToken
    Base.metadata.create_all(bind=engine)


def _sync_users_schema() -> None:
    with engine.begin() as connection:
        full_name_exists = connection.execute(
            text(
                """
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'users' AND column_name = 'full_name'
                """
            )
        ).scalar_one_or_none()
        if full_name_exists is None:
            connection.execute(
                text(
                    "ALTER TABLE users "
                    "ADD COLUMN full_name VARCHAR(255) NOT NULL DEFAULT ''"
                )
            )

        role_exists = connection.execute(
            text(
                """
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'users' AND column_name = 'role'
                """
            )
        ).scalar_one_or_none()
        if role_exists is None:
            connection.execute(
                text(
                    """
                    DO $$
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'role_enum') THEN
                            CREATE TYPE role_enum AS ENUM ('admin', 'candidate', 'reviewer');
                        END IF;
                    END
                    $$;
                    """
                )
            )
            connection.execute(
                text(
                    "ALTER TABLE users "
                    "ADD COLUMN role role_enum NOT NULL DEFAULT 'candidate'"
                )
            )

        public_id_exists = connection.execute(
            text(
                """
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'users' AND column_name = 'public_id'
                """
            )
        ).scalar_one_or_none()
        if public_id_exists is None:
            connection.execute(
                text(
                    "ALTER TABLE users "
                    "ADD COLUMN public_id VARCHAR(36)"
                )
            )
            user_ids = connection.execute(text("SELECT id FROM users")).scalars().all()
            for user_id in user_ids:
                connection.execute(
                    text("UPDATE users SET public_id = :public_id WHERE id = :user_id"),
                    {"public_id": str(uuid.uuid4()), "user_id": user_id},
                )
            connection.execute(
                text("ALTER TABLE users ALTER COLUMN public_id SET NOT NULL")
            )
            connection.execute(
                text(
                    "CREATE UNIQUE INDEX IF NOT EXISTS ix_users_public_id "
                    "ON users (public_id)"
                )
            )
        else:
            missing_public_ids = connection.execute(
                text("SELECT id FROM users WHERE public_id IS NULL OR public_id = ''")
            ).scalars().all()
            for user_id in missing_public_ids:
                connection.execute(
                    text("UPDATE users SET public_id = :public_id WHERE id = :user_id"),
                    {"public_id": str(uuid.uuid4()), "user_id": user_id},
                )
            connection.execute(
                text(
                    "CREATE UNIQUE INDEX IF NOT EXISTS ix_users_public_id "
                    "ON users (public_id)"
                )
            )
            public_id_nullable = connection.execute(
                text(
                    """
                    SELECT is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'users' AND column_name = 'public_id'
                    """
                )
            ).scalar_one_or_none()
            if public_id_nullable == "YES":
                connection.execute(
                    text("ALTER TABLE users ALTER COLUMN public_id SET NOT NULL")
                )
