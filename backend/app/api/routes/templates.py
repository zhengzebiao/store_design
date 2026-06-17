from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import success
from app.schemas.template import TemplateListQuery, UseTemplatePayload
from app.services.template_service import TemplateService

router = APIRouter()


@router.get("/templates")
async def list_templates(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    company_id: str | None = None,
    keyword: str | None = None,
    type: str | None = "diy",
    is_sel: int | None = None,
    db: Session = Depends(get_db),
):
    query = TemplateListQuery(page=page, limit=limit, company_id=company_id, keyword=keyword, type=type, is_sel=is_sel)
    items, total = TemplateService(db).list_templates(query)
    return success(items, current_page=page, limit=limit, total=total)


@router.get("/templates/{template_id}")
async def get_template_detail(template_id: str, company_id: str | None = None, db: Session = Depends(get_db)):
    return success(TemplateService(db).get_detail(template_id, company_id))


@router.post("/templates/{template_id}/use")
async def use_template(template_id: str, payload: UseTemplatePayload, db: Session = Depends(get_db)):
    TemplateService(db).use_template(template_id, payload.company_id)
    return success({"id": template_id, "message": "使用成功", "company_id": payload.company_id})


@router.delete("/templates/{template_id}")
async def delete_template(template_id: str, company_id: str, db: Session = Depends(get_db)):
    TemplateService(db).delete_template(template_id, company_id)
    return success({"id": template_id, "message": "删除成功", "company_id": company_id})
