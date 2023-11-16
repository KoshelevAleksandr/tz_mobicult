from sqlalchemy import Column, Integer, Table, String, Float

from database import metadata

rate = Table(
    "rate",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("currency", String, nullable=False),
    Column("today", Float, nullable=False),
    Column("yesterday", Float, nullable=False),
    Column("before_yesterday", Float, nullable=False),
)

#
#
#
# class CurrencyRate(Base):
#     __tablename__ = "currency_rate"
#
#     id = Column(Integer, primary_key=True)
#     currency = Column(String, nullable=False)
#     today = Column(Float, nullable=False)
#     yesterday = Column(Float, nullable=False)
#     before_yesterday = Column(Float, nullable=False)
