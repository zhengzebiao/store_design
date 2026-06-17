from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import success
from app.services.component_service import ComponentService

router = APIRouter()


@router.get("/components")
async def list_components(db: Session = Depends(get_db)):
    return success(ComponentService(db).list_components())
