from decimal import Decimal
from typing import Any

from app.models.component import StoreDesignComponentMeta
from app.models.page import StoreDesignPage
from app.models.template import StoreDesignTemplate


def to_text(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def decimal_to_text(value: Decimal | int | float | None) -> str:
    if value is None:
        return "0.00"
    return f"{Decimal(value):.2f}"


def template_to_dict(template: StoreDesignTemplate) -> dict[str, Any]:
    return {
        "id": template.id,
        "name": template.name,
        "type": template.type,
        "is_sel": template.is_sel,
        "created_at": to_text(template.created_at),
        "updated_at": to_text(template.updated_at),
        "is_open_tabbar": template.is_open_tabbar,
        "other_company_show": template.other_company_show,
        "pid": template.pid,
        "head_img": template.head_img or "",
        "price": decimal_to_text(template.price),
        "theme_id": template.theme_id,
        "system_recommend_template": template.system_recommend_template,
    }


def page_to_dict(page: StoreDesignPage) -> dict[str, Any]:
    return {
        "id": str(page.id),
        "diy_id": str(page.diy_id),
        "company_id": page.company_id,
        "type": page.type,
        "page_name": page.page_name,
        "datas": page.datas or [],
        "other_company_show": page.other_company_show,
        "page_info": page.page_info or {},
        "member_level": page.member_level or [],
        "level": page.level or [],
        "status": page.status,
        "created_at": to_text(page.created_at),
        "updated_at": to_text(page.updated_at),
        "page_sort": page.page_sort,
        "page_scene": page.page_scene,
        "top_id": page.top_id or {},
        "foot_type": page.foot_type,
        "foot_id": page.foot_id or {},
        "page_type": page.page_type,
    }


def component_to_dict(component: StoreDesignComponentMeta) -> dict[str, Any]:
    return {
        "id": component.id,
        "component_key": component.component_key,
        "name": component.name,
        "category_id": component.category_id,
        "icon": component.icon,
        "tpl_id": component.tpl_id,
        "templates": component.templates or [],
        "schema_json": component.schema_json or {},
        "default_data": component.default_data_json or {},
        "enabled": component.enabled,
        "sort": component.sort,
    }
