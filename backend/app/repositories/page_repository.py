from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import BusinessError
from app.models.page import StoreDesignPage
from app.models.template import StoreDesignTemplate
from app.repositories.serializers import page_to_dict
from app.schemas.page import SavePagePayload


def page_type_to_text(value: str | list[str]) -> str:
    if isinstance(value, list):
        return ",".join(value)
    return value


class PageRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save(self, payload: SavePagePayload) -> dict:
        if payload.mode == "copy":
            source_diy_id = int(payload.route_id or payload.diy_id or 0)
            if not source_diy_id:
                raise BusinessError("INVALID_PARAMS", "复制模式缺少来源模板 ID")
            source_page = self.db.scalar(
                select(StoreDesignPage).where(
                    StoreDesignPage.diy_id == source_diy_id,
                    StoreDesignPage.company_id == int(payload.company_id),
                    StoreDesignPage.deleted_at.is_(None),
                )
            )
            if not source_page:
                raise BusinessError("PAGE_NOT_FOUND", "复制来源页面不存在", status_code=404)

        if payload.mode in {"create", "copy"}:
            template = StoreDesignTemplate(
                company_id=int(payload.company_id),
                name=payload.page_name,
                type="diy",
                is_sel=0,
                is_open_tabbar=0,
                other_company_show=payload.other_company_show,
                pid=int(payload.route_id or payload.diy_id or 0),
                head_img=payload.head_img or "",
                price=0,
                theme_id=None,
                system_recommend_template=0,
            )
            self.db.add(template)
            self.db.flush()

            page = StoreDesignPage(
                diy_id=template.id,
                company_id=int(payload.company_id),
                type=payload.type,
                page_name=payload.page_name,
                datas=[item.model_dump() for item in payload.datas],
                other_company_show=payload.other_company_show,
                page_info=payload.page_info,
                member_level=payload.member_level,
                level=payload.level,
                status=payload.status,
                page_sort=int(payload.page_sort),
                page_scene=int(payload.page_scene),
                top_id=payload.top_id,
                foot_type=int(payload.foot_type),
                foot_id=payload.foot_id,
                page_type=page_type_to_text(payload.page_type),
            )
            self.db.add(page)
            self.db.commit()
            self.db.refresh(page)
            return page_to_dict(page)

        diy_id = int(payload.diy_id or payload.route_id or 0)
        if not diy_id:
            raise BusinessError("INVALID_PARAMS", "编辑模式缺少模板 ID")

        page = self.db.scalar(
            select(StoreDesignPage).where(
                StoreDesignPage.diy_id == diy_id,
                StoreDesignPage.company_id == int(payload.company_id),
                StoreDesignPage.deleted_at.is_(None),
            )
        )
        if not page:
            raise BusinessError("PAGE_NOT_FOUND", "装修页面不存在", status_code=404)

        template = self.db.scalar(
            select(StoreDesignTemplate).where(
                StoreDesignTemplate.id == diy_id,
                StoreDesignTemplate.company_id == int(payload.company_id),
                StoreDesignTemplate.deleted_at.is_(None),
            )
        )
        if not template:
            raise BusinessError("TEMPLATE_NOT_FOUND", "模板不存在", status_code=404)

        template.name = payload.page_name
        template.other_company_show = payload.other_company_show
        template.head_img = payload.head_img or template.head_img

        page.type = payload.type
        page.page_name = payload.page_name
        page.datas = [item.model_dump() for item in payload.datas]
        page.other_company_show = payload.other_company_show
        page.page_info = payload.page_info
        page.member_level = payload.member_level
        page.level = payload.level
        page.status = payload.status
        page.page_sort = int(payload.page_sort)
        page.page_scene = int(payload.page_scene)
        page.top_id = payload.top_id
        page.foot_type = int(payload.foot_type)
        page.foot_id = payload.foot_id
        page.page_type = page_type_to_text(payload.page_type)

        self.db.commit()
        self.db.refresh(page)
        return page_to_dict(page)
