from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.core.errors import BusinessError
from app.models.page import StoreDesignPage
from app.models.template import StoreDesignTemplate
from app.repositories.serializers import page_to_dict, template_to_dict
from app.schemas.template import TemplateListQuery


class TemplateRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_templates(self, query: TemplateListQuery) -> tuple[list[dict], int]:
        statement = select(StoreDesignTemplate).where(StoreDesignTemplate.deleted_at.is_(None))
        count_statement = select(func.count()).select_from(StoreDesignTemplate).where(StoreDesignTemplate.deleted_at.is_(None))

        if query.company_id is not None:
            statement = statement.where(StoreDesignTemplate.company_id == int(query.company_id))
            count_statement = count_statement.where(StoreDesignTemplate.company_id == int(query.company_id))
        if query.keyword:
            statement = statement.where(StoreDesignTemplate.name.ilike(f"%{query.keyword}%"))
            count_statement = count_statement.where(StoreDesignTemplate.name.ilike(f"%{query.keyword}%"))
        if query.type:
            statement = statement.where(StoreDesignTemplate.type == query.type)
            count_statement = count_statement.where(StoreDesignTemplate.type == query.type)
        if query.is_sel is not None:
            statement = statement.where(StoreDesignTemplate.is_sel == query.is_sel)
            count_statement = count_statement.where(StoreDesignTemplate.is_sel == query.is_sel)

        total = self.db.scalar(count_statement) or 0
        items = self.db.scalars(
            statement.order_by(StoreDesignTemplate.updated_at.desc()).offset((query.page - 1) * query.limit).limit(query.limit)
        ).all()
        return [template_to_dict(item) for item in items], total

    def get_page_by_diy_id(self, diy_id: int | str, company_id: int | str | None = None) -> dict:
        statement = select(StoreDesignPage).where(StoreDesignPage.diy_id == int(diy_id), StoreDesignPage.deleted_at.is_(None))
        if company_id is not None:
            statement = statement.where(StoreDesignPage.company_id == int(company_id))
        page = self.db.scalar(statement)
        if not page:
            raise BusinessError("TEMPLATE_NOT_FOUND", "模板不存在", status_code=404)
        return page_to_dict(page)

    def use_template(self, template_id: int | str, company_id: int | str) -> None:
        template = self.db.scalar(
            select(StoreDesignTemplate).where(
                StoreDesignTemplate.id == int(template_id),
                StoreDesignTemplate.company_id == int(company_id),
                StoreDesignTemplate.deleted_at.is_(None),
            )
        )
        if not template:
            raise BusinessError("TEMPLATE_NOT_FOUND", "模板不存在", status_code=404)

        self.db.execute(
            update(StoreDesignTemplate)
            .where(StoreDesignTemplate.company_id == int(company_id), StoreDesignTemplate.deleted_at.is_(None))
            .values(is_sel=0)
        )
        template.is_sel = 1
        self.db.commit()

    def delete_template(self, template_id: int | str, company_id: int | str) -> None:
        template = self.db.scalar(
            select(StoreDesignTemplate).where(
                StoreDesignTemplate.id == int(template_id),
                StoreDesignTemplate.company_id == int(company_id),
                StoreDesignTemplate.deleted_at.is_(None),
            )
        )
        if not template:
            raise BusinessError("TEMPLATE_NOT_FOUND", "模板不存在", status_code=404)
        if template.system_recommend_template:
            raise BusinessError("INVALID_PARAMS", "系统推荐模板不能删除")

        self.db.delete(template)
        page = self.db.scalar(
            select(StoreDesignPage).where(
                StoreDesignPage.diy_id == int(template_id),
                StoreDesignPage.company_id == int(company_id),
            )
        )
        if page:
            self.db.delete(page)
        self.db.commit()
