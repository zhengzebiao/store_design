from sqlalchemy import BigInteger, JSON, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StoreDesignPage(Base):
    __tablename__ = "store_design_page"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    diy_id: Mapped[int] = mapped_column(BigInteger, index=True)
    company_id: Mapped[int] = mapped_column(BigInteger, index=True)
    type: Mapped[str] = mapped_column(String(32), default="home_page")
    page_name: Mapped[str] = mapped_column(String(255))
    datas: Mapped[dict] = mapped_column(JSON, default=list)
    page_info: Mapped[dict] = mapped_column(JSON, default=dict)
    member_level: Mapped[dict] = mapped_column(JSON, default=list)
    level: Mapped[dict] = mapped_column(JSON, default=list)
    status: Mapped[int] = mapped_column(SmallInteger, default=1)
    page_sort: Mapped[int] = mapped_column(SmallInteger, default=2)
    page_scene: Mapped[int] = mapped_column(SmallInteger, default=2)
    top_id: Mapped[dict] = mapped_column(JSON, default=dict)
    foot_type: Mapped[int] = mapped_column(SmallInteger, default=1)
    foot_id: Mapped[dict] = mapped_column(JSON, default=dict)
    page_type: Mapped[str] = mapped_column(String(32), default="2")
    schema_version: Mapped[int] = mapped_column(default=1)
