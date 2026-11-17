from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric,
    Boolean,
    DateTime,
    Text,
    func
)

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(String(100), nullable=False, index=True)
    transaction_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    account_reference = Column(String(100), nullable=False)

    source_file = Column(String(255))
    is_duplicate = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
