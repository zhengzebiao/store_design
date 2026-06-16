from fastapi import APIRouter

from app.core.response import success
from app.services.component_service import ComponentService

router = APIRouter()
service = ComponentService()


@router.get("/components")
async def list_components():
    return success(service.list_components())
