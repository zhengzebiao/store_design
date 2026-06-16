from app.repositories.component_repository import ComponentRepository


class ComponentService:
    def __init__(self) -> None:
        self.repository = ComponentRepository()

    def list_components(self) -> list[dict]:
        return self.repository.list_enabled()
