from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import BusinessError
from app.models.component import StoreDesignComponentMeta
from app.repositories.page_repository import PageRepository
from app.schemas.component import DesignComponent
from app.schemas.page import SavePagePayload


def get_by_path(target: dict[str, Any], path: str) -> Any:
    current: Any = target
    for key in [item for item in path.split(".") if item]:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def is_empty(value: Any) -> bool:
    return value is None or value == "" or value == []


class PageService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = PageRepository(db)

    def save_page(self, payload: SavePagePayload) -> dict:
        if not payload.company_id:
            raise BusinessError("INVALID_PARAMS", "company_id 不能为空")
        if not payload.page_name:
            raise BusinessError("INVALID_PARAMS", "page_name 不能为空")
        self.validate_components(payload.datas)
        return self.repository.save(payload)

    def validate_components(self, components: list[DesignComponent]) -> None:
        if not components:
            return

        metas = self.db.scalars(select(StoreDesignComponentMeta).where(StoreDesignComponentMeta.enabled == 1)).all()
        meta_map = {meta.component_key: meta for meta in metas}
        for component in components:
            self.validate_component(component, meta_map)

    def validate_component(self, component: DesignComponent, meta_map: dict[str, StoreDesignComponentMeta]) -> None:
        if not component.id or not component.component_key or not component.component_title or not component.template_id:
            raise BusinessError("COMPONENT_SCHEMA_INVALID", "组件基础字段不完整")
        if component.remote_data is None or not isinstance(component.remote_data, dict):
            raise BusinessError("COMPONENT_SCHEMA_INVALID", f"组件 {component.component_title} 配置数据不合法")

        meta = meta_map.get(component.component_key)
        if not meta:
            raise BusinessError("COMPONENT_NOT_FOUND", f"组件 {component.component_key} 不存在", status_code=400)

        self.validate_required_fields(component, meta)
        for child in component.tasks or []:
            self.validate_component(child, meta_map)

    def validate_required_fields(self, component: DesignComponent, meta: StoreDesignComponentMeta) -> None:
        groups = (meta.schema_json or {}).get("groups") or []
        for group in groups:
            for field in group.get("fields") or []:
                if not field.get("required"):
                    continue
                key = field.get("key")
                if not key:
                    continue
                if is_empty(get_by_path(component.remote_data, key)):
                    label = field.get("label") or key
                    raise BusinessError("COMPONENT_SCHEMA_INVALID", f"组件 {component.component_title} 的 {label} 不能为空")
