from fastapi import APIRouter, Query

from app.core.response import success
from app.schemas.template import TemplateListQuery, UseTemplatePayload
from app.services.template_service import TemplateService

router = APIRouter()
service = TemplateService()


@router.get("/templates")
async def list_templates(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    keyword: str | None = None,
    type: str | None = "diy",
    is_sel: int | None = None,
):
    query = TemplateListQuery(page=page, limit=limit, keyword=keyword, type=type, is_sel=is_sel)
    items, total = service.list_templates(query)
    return success(items, current_page=page, limit=limit, total=total)


@router.get("/templates/{template_id}")
async def get_template_detail(template_id: str):
    return success(service.get_detail(template_id))


@router.post("/templates/{template_id}/use")
async def use_template(template_id: str, payload: UseTemplatePayload):
    service.use_template(template_id)
    return success({"id": template_id, "message": "使用成功", "company_id": payload.company_id})


@router.delete("/templates/{template_id}")
async def delete_template(template_id: str, company_id: str):
    service.delete_template(template_id)
    return success({"id": template_id, "message": "删除成功", "company_id": company_id})
