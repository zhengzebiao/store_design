from sqlalchemy import BigInteger, JSON, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StoreDesignComponentMeta(Base):
    __tablename__ = "store_design_component_meta"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    component_key: Mapped[str] = mapped_column(String(64), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    category_id: Mapped[int] = mapped_column(default=0)
    icon: Mapped[str | None] = mapped_column(String(255))
    tpl_id: Mapped[int | None] = mapped_column(BigInteger)
    templates: Mapped[dict] = mapped_column(JSON, default=list)
    schema_json: Mapped[dict] = mapped_column(JSON, default=dict)
    default_data_json: Mapped[dict] = mapped_column(JSON, default=dict)
    enabled: Mapped[int] = mapped_column(SmallInteger, default=1)
    sort: Mapped[int] = mapped_column(default=0)
