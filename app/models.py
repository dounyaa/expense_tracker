from sqlalchemy import Integer, Float, String, Date, Boolean
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import date as DateType

class ExpenseDB(Base):
    __tablename__ = "expenses"
    id : Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    date : Mapped[DateType] = mapped_column(Date, nullable=False)
    is_recurring : Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sa.false())
