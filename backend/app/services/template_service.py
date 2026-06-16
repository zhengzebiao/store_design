from app.repositories.template_repository import TemplateRepository
from app.schemas.template import TemplateListQuery


class TemplateService:
    def __init__(self) -> None:
        self.repository = TemplateRepository()

    def list_templates(self, query: TemplateListQuery) -> tuple[list[dict], int]:
        return self.repository.list_templates(query)

    def get_detail(self, template_id: int | str) -> dict:
        return self.repository.get_page_by_diy_id(template_id)

    def use_template(self, template_id: int | str) -> None:
        self.repository.use_template(template_id)

    def delete_template(self, template_id: int | str) -> None:
        self.repository.delete_template(template_id)
