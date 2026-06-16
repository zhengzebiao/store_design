from copy import deepcopy
from datetime import datetime, timezone
from itertools import count
from typing import Any


def now_text() -> str:
    return datetime.now(timezone.utc).isoformat()


_template_id = count(1002)
_page_id = count(70)

TEMPLATES: list[dict[str, Any]] = [
    {
        "id": 1001,
        "name": "默认首页模板",
        "type": "diy",
        "is_sel": 1,
        "created_at": now_text(),
        "updated_at": now_text(),
        "is_open_tabbar": 1,
        "other_company_show": 0,
        "pid": 0,
        "head_img": "",
        "price": "0.00",
        "theme_id": None,
        "system_recommend_template": 1,
    }
]

PAGES: dict[str, dict[str, Any]] = {
    "1001": {
        "id": "69",
        "diy_id": "1001",
        "company_id": 3,
        "type": "home_page",
        "page_name": "默认首页模板",
        "datas": [],
        "other_company_show": 0,
        "page_info": {},
        "member_level": [],
        "level": [],
        "status": 1,
        "created_at": now_text(),
        "updated_at": now_text(),
        "page_sort": 2,
        "page_scene": 2,
        "top_id": {},
        "foot_type": 1,
        "foot_id": {},
        "page_type": "2",
    }
}

COMPONENTS: list[dict[str, Any]] = [
    {
        "id": 1,
        "component_key": "U_search",
        "name": "搜索框",
        "category_id": 1,
        "icon": "icon-ht_basis_searchframe",
        "tpl_id": 6,
        "templates": [{"id": 6, "component_key": "U_search", "name": "模板一", "name_en": "template1"}],
        "schema_json": {
            "groups": [
                {
                    "key": "datas",
                    "title": "数据配置",
                    "fields": [
                        {"key": "search_title", "label": "搜索提示文案", "type": "text", "default": "店内搜索"}
                    ],
                }
            ]
        },
        "default_data": {"search_title": "店内搜索"},
        "enabled": 1,
        "sort": 100,
    },
    {
        "id": 2,
        "component_key": "U_banner",
        "name": "图片轮播",
        "category_id": 2,
        "icon": "icon-banner",
        "tpl_id": 7,
        "templates": [{"id": 7, "component_key": "U_banner", "name": "模板一", "name_en": "template1"}],
        "schema_json": {"groups": []},
        "default_data": {"items": []},
        "enabled": 1,
        "sort": 90,
    },
]


def clone(value: Any) -> Any:
    return deepcopy(value)


def next_template_id() -> int:
    return next(_template_id)


def next_page_id() -> int:
    return next(_page_id)
