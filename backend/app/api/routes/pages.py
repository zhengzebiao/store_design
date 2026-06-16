from fastapi import APIRouter

from app.core.response import success
from app.schemas.page import SavePagePayload, SavePageResult
from app.services.page_service import PageService

router = APIRouter()
service = PageService()


@router.post("/pages/save")
async def save_page(payload: SavePagePayload):
    page = service.save_page(payload)
    result = SavePageResult(
        id=str(page["id"]),
        diy_id=str(page["diy_id"]),
        url=f"/store_design/edit?mode=edit&id={page['diy_id']}",
        message="保存成功",
    )
    return success(result.model_dump())
