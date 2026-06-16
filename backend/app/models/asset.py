from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StoreDesignAsset(Base):
    __tablename__ = "store_design_asset"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(BigInteger, index=True)
    asset_type: Mapped[str] = mapped_column(String(32))
    url: Mapped[str] = mapped_column(Text)
    filename: Mapped[str | None] = mapped_column(String(255))
    mime_type: Mapped[str | None] = mapped_column(String(100))
    size: Mapped[int] = mapped_column(BigInteger, default=0)
