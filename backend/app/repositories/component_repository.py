from app.repositories.memory_store import COMPONENTS, clone


class ComponentRepository:
    def list_enabled(self) -> list[dict]:
        return sorted(
            [item for item in clone(COMPONENTS) if item.get("enabled") == 1],
            key=lambda item: item.get("sort", 0),
            reverse=True,
        )
