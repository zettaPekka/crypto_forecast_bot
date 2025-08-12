from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import BigInteger


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

class TraderData(Base):
    __tablename__ = "trader_data"

    trader_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    balance: Mapped[float] = mapped_column(default=0.0)
