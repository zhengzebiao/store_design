from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.component import StoreDesignComponentMeta
from app.repositories.serializers import component_to_dict


class ComponentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_enabled(self) -> list[dict]:
        items = self.db.scalars(
            select(StoreDesignComponentMeta)
            .where(StoreDesignComponentMeta.enabled == 1)
            .order_by(StoreDesignComponentMeta.sort.desc(), StoreDesignComponentMeta.id.asc())
        ).all()
        return [component_to_dict(item) for item in items]
