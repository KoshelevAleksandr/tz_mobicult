from pydantic import BaseModel, Field
from typing import List
from datetime import date


class Currency(BaseModel):
    valute: str
    value: float


class Rate(BaseModel):
    date: date
    name: str
    currency: List[Currency]


