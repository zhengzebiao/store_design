from sqlalchemy.orm import Session

from app.repositories.component_repository import ComponentRepository


class ComponentService:
    def __init__(self, db: Session) -> None:
        self.repository = ComponentRepository(db)

    def list_components(self) -> list[dict]:
        return self.repository.list_enabled()
