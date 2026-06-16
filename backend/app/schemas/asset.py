from pydantic import BaseModel


class AssetUploadResult(BaseModel):
    id: str
    url: str
    filename: str
    mime_type: str | None = None
    size: int = 0
