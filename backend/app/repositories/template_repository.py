from app.core.errors import BusinessError
from app.repositories.memory_store import PAGES, TEMPLATES, clone
from app.schemas.template import TemplateListQuery


class TemplateRepository:
    def list_templates(self, query: TemplateListQuery) -> tuple[list[dict], int]:
        items = clone(TEMPLATES)
        if query.keyword:
            items = [item for item in items if query.keyword in item["name"]]
        if query.type:
            items = [item for item in items if item["type"] == query.type]
        if query.is_sel is not None:
            items = [item for item in items if item["is_sel"] == query.is_sel]

        total = len(items)
        start = (query.page - 1) * query.limit
        end = start + query.limit
        return items[start:end], total

    def get_page_by_diy_id(self, diy_id: int | str) -> dict:
        page = PAGES.get(str(diy_id))
        if not page:
            raise BusinessError("TEMPLATE_NOT_FOUND", "模板不存在", status_code=404)
        return clone(page)

    def use_template(self, template_id: int | str) -> None:
        found = False
        for item in TEMPLATES:
            if str(item["id"]) == str(template_id):
                item["is_sel"] = 1
                found = True
            else:
                item["is_sel"] = 0
        if not found:
            raise BusinessError("TEMPLATE_NOT_FOUND", "模板不存在", status_code=404)

    def delete_template(self, template_id: int | str) -> None:
        for index, item in enumerate(TEMPLATES):
            if str(item["id"]) == str(template_id):
                if item.get("system_recommend_template"):
                    raise BusinessError("INVALID_PARAMS", "系统推荐模板不能删除")
                del TEMPLATES[index]
                PAGES.pop(str(template_id), None)
                return
        raise BusinessError("TEMPLATE_NOT_FOUND", "模板不存在", status_code=404)
