from datetime import datetime, UTC

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        jti: str,
        token_hash: str,
        user_public_id: str,
        expires_at: datetime,
    ) -> RefreshToken:
        refresh_token = RefreshToken(
            jti=jti,
            token_hash=token_hash,
            user_public_id=user_public_id,
            expires_at=expires_at,
        )
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def consume(self, *, jti: str, token_hash: str) -> RefreshToken | None:
        now = datetime.now(UTC)
        token = self.db.scalars(
            select(RefreshToken)
            .where(
                RefreshToken.jti == jti,
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked_at.is_(None),
                RefreshToken.expires_at > now,
            )
            .with_for_update()
        ).first()
        if token is None:
            return None
        token.revoked_at = now
        self.db.commit()
        self.db.refresh(token)
        return token

    def revoke_by_jti(self, jti: str) -> bool:
        token = self.db.scalars(
            select(RefreshToken).where(
                RefreshToken.jti == jti,
                RefreshToken.revoked_at.is_(None),
            )
        ).first()
        if token is None:
            return False
        token.revoked_at = datetime.now(UTC)
        self.db.commit()
        return True
