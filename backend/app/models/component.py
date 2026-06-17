from datetime import datetime
from typing import Any

from sqlalchemy import BigInteger, DateTime, Integer, JSON, SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

ID_TYPE = BigInteger().with_variant(Integer, "sqlite")


class StoreDesignComponentMeta(Base):
    __tablename__ = "store_design_component_meta"

    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    component_key: Mapped[str] = mapped_column(String(64), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    category_id: Mapped[int] = mapped_column(default=0)
    icon: Mapped[str | None] = mapped_column(String(255))
    tpl_id: Mapped[int | None] = mapped_column(BigInteger)
    templates: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    schema_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    default_data_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    enabled: Mapped[int] = mapped_column(SmallInteger, default=1)
    sort: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
