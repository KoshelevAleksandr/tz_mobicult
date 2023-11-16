from pydantic import BaseModel


class Rate(BaseModel):
    id: int
    currency: str
    today: float
    yesterday: float
    before_yesterday: float


class TodayRate(BaseModel):
    id: int
    currency: str
    today: float


class Yesterday(BaseModel):
    id: int
    currency: str
    yesterday: float


class BeforeYesterday(BaseModel):
    id: int
    currency: str
    before_yesterday: float

# class GetCurrencyRate(BaseModel):
#     id: int
#     currency: str
#     currency_value: float
#     day: str
