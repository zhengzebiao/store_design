from pydantic import BaseModel, ConfigDict


class StoreTemplate(BaseModel):
    id: int | str
    name: str
    type: str = "diy"
    is_sel: int = 0
    created_at: str | None = None
    updated_at: str | None = None
    is_open_tabbar: int = 0
    other_company_show: int = 0
    pid: int | str = 0
    head_img: str | None = None
    price: str = "0.00"
    theme_id: int | str | None = None
    system_recommend_template: int = 0

    model_config = ConfigDict(from_attributes=True)


class TemplateListQuery(BaseModel):
    page: int = 1
    limit: int = 20
    keyword: str | None = None
    type: str | None = "diy"
    is_sel: int | None = None


class UseTemplatePayload(BaseModel):
    company_id: int | str
    operator: str | None = None
