from pydantic import BaseModel, Field
from typing import List
from datetime import date


class Rate(BaseModel):
    id: int
    currency: str
    today: float
    yesterday: float
    before_yesterday: float

    # class Config:
    #     orm_mode = True


