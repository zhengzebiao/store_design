from datetime import datetime
from typing import Any

from sqlalchemy import BigInteger, DateTime, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StoreDesignOperationLog(Base):
    __tablename__ = "store_design_operation_log"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(BigInteger, index=True)
    diy_id: Mapped[int | None] = mapped_column(BigInteger, index=True)
    page_id: Mapped[int | None] = mapped_column(BigInteger)
    operator_id: Mapped[int | None] = mapped_column(BigInteger)
    operation: Mapped[str] = mapped_column(String(64))
    before_snapshot: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    after_snapshot: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    ip: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
