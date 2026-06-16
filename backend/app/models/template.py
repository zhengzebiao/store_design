from sqlalchemy import BigInteger, Numeric, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StoreDesignTemplate(Base):
    __tablename__ = "store_design_template"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(BigInteger, index=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(32), default="diy")
    is_sel: Mapped[int] = mapped_column(SmallInteger, default=0)
    is_open_tabbar: Mapped[int] = mapped_column(SmallInteger, default=0)
    other_company_show: Mapped[int] = mapped_column(SmallInteger, default=0)
    pid: Mapped[int] = mapped_column(BigInteger, default=0)
    head_img: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    theme_id: Mapped[int | None] = mapped_column(BigInteger)
    system_recommend_template: Mapped[int] = mapped_column(SmallInteger, default=0)
