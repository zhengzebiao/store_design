from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.component import StoreDesignComponentMeta
from app.models.page import StoreDesignPage
from app.models.template import StoreDesignTemplate

DEFAULT_COMPANY_ID = 3

COMPONENT_SEED = [
    {
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
                        {"key": "search_title", "label": "搜索提示文案", "type": "text", "default": "店内搜索", "required": True}
                    ],
                }
            ]
        },
        "default_data_json": {"search_title": "店内搜索"},
        "enabled": 1,
        "sort": 100,
    },
    {
        "component_key": "U_banner",
        "name": "图片轮播",
        "category_id": 2,
        "icon": "icon-banner",
        "tpl_id": 7,
        "templates": [{"id": 7, "component_key": "U_banner", "name": "模板一", "name_en": "template1"}],
        "schema_json": {"groups": []},
        "default_data_json": {"items": []},
        "enabled": 1,
        "sort": 90,
    },
]


def seed_store_design(db: Session, company_id: int = DEFAULT_COMPANY_ID) -> None:
    template = db.scalar(
        select(StoreDesignTemplate).where(
            StoreDesignTemplate.company_id == company_id,
            StoreDesignTemplate.name == "默认首页模板",
            StoreDesignTemplate.deleted_at.is_(None),
        )
    )
    if template is None:
        template = StoreDesignTemplate(
            company_id=company_id,
            name="默认首页模板",
            type="diy",
            is_sel=1,
            is_open_tabbar=1,
            other_company_show=0,
            pid=0,
            head_img="",
            price=0,
            theme_id=None,
            system_recommend_template=1,
        )
        db.add(template)
        db.flush()

    page = db.scalar(
        select(StoreDesignPage).where(
            StoreDesignPage.company_id == company_id,
            StoreDesignPage.diy_id == template.id,
            StoreDesignPage.deleted_at.is_(None),
        )
    )
    if page is None:
        db.add(
            StoreDesignPage(
                diy_id=template.id,
                company_id=company_id,
                type="home_page",
                page_name=template.name,
                datas=[],
                other_company_show=0,
                page_info={},
                member_level=[],
                level=[],
                status=1,
                page_sort=2,
                page_scene=2,
                top_id={},
                foot_type=1,
                foot_id={},
                page_type="2",
            )
        )

    for item in COMPONENT_SEED:
        component = db.scalar(
            select(StoreDesignComponentMeta).where(StoreDesignComponentMeta.component_key == item["component_key"])
        )
        if component is None:
            db.add(StoreDesignComponentMeta(**item))
        else:
            for key, value in item.items():
                setattr(component, key, value)

    db.commit()
