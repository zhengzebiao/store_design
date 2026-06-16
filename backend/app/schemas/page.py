from typing import Any, Literal

from pydantic import BaseModel, Field

from app.schemas.component import DesignComponent


class StoreDesignPage(BaseModel):
    id: int | str = ""
    diy_id: int | str = ""
    company_id: int | str | None = None
    type: str = "home_page"
    page_name: str
    datas: list[DesignComponent] = Field(default_factory=list)
    other_company_show: int = 0
    page_info: dict[str, Any] = Field(default_factory=dict)
    member_level: list[Any] = Field(default_factory=list)
    level: list[Any] = Field(default_factory=list)
    status: int = 1
    created_at: str | None = None
    updated_at: str | None = None
    page_sort: int | str = 2
    page_scene: int | str = 2
    top_id: dict[str, Any] = Field(default_factory=dict)
    foot_type: int | str = 1
    foot_id: dict[str, Any] = Field(default_factory=dict)
    page_type: str | list[str] = "2"


class SavePagePayload(StoreDesignPage):
    mode: Literal["create", "edit", "copy"] = "create"
    route_id: int | str | None = None
    head_img: str | None = None


class SavePageResult(BaseModel):
    id: str
    diy_id: str
    url: str
    message: str
