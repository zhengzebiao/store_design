from sqlalchemy.orm import Session

from app.core.errors import BusinessError
from app.repositories.page_repository import PageRepository
from app.schemas.page import SavePagePayload


class PageService:
    def __init__(self, db: Session) -> None:
        self.repository = PageRepository(db)

    def save_page(self, payload: SavePagePayload) -> dict:
        if not payload.company_id:
            raise BusinessError("INVALID_PARAMS", "company_id 不能为空")
        if not payload.page_name:
            raise BusinessError("INVALID_PARAMS", "page_name 不能为空")
        return self.repository.save(payload)
