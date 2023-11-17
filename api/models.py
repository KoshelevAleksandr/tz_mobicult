from sqlalchemy import Column, Integer, Table, String, MetaData, Float

metadata = MetaData()

rate = Table(
    "rate",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("currency", String, nullable=False),
    Column("today", Float, nullable=False),
    Column("yesterday", Float, nullable=False),
    Column("before_yesterday", Float, nullable=False),
)
