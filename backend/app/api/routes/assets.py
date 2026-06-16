from fastapi import APIRouter, File, Form, UploadFile

from app.core.response import success
from app.schemas.asset import AssetUploadResult

router = APIRouter()


@router.post("/assets/upload")
async def upload_asset(company_id: str = Form(...), file: UploadFile = File(...)):
    content = await file.read()
    result = AssetUploadResult(
        id=f"asset-{company_id}-{file.filename}",
        url=f"/uploads/{company_id}/{file.filename}",
        filename=file.filename or "upload.bin",
        mime_type=file.content_type,
        size=len(content),
    )
    return success(result.model_dump())
