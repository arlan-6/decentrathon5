from sqlalchemy import select
from sqlalchemy.orm import Session

from models.application import Application


class ApplicationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, *, candidate_id: int, essay_text: str, motivation_text: str) -> Application:
        item = Application(candidate_id=candidate_id, essay_text=essay_text, motivation_text=motivation_text)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_all(self) -> list[Application]:
        return list(self.db.scalars(select(Application).order_by(Application.id)))

    def get(self, application_id: int) -> Application | None:
        return self.db.get(Application, application_id)

    def update(
        self,
        *,
        application: Application,
        essay_text: str | None = None,
        motivation_text: str | None = None,
        status: str | None = None,
    ) -> Application:
        if essay_text is not None:
            application.essay_text = essay_text
        if motivation_text is not None:
            application.motivation_text = motivation_text
        if status is not None:
            application.status = status

        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def delete(self, *, application: Application) -> None:
        self.db.delete(application)
        self.db.commit()
