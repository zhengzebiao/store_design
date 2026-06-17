from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import success
from app.schemas.page import SavePagePayload, SavePageResult
from app.services.page_service import PageService

router = APIRouter()


@router.post("/pages/save")
async def save_page(payload: SavePagePayload, db: Session = Depends(get_db)):
    page = PageService(db).save_page(payload)
    result = SavePageResult(
        id=str(page["id"]),
        diy_id=str(page["diy_id"]),
        url=f"/store_design/edit?mode=edit&id={page['diy_id']}",
        message="保存成功",
    )
    return success(result.model_dump())
