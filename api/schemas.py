from pydantic import BaseModel


class GetCurrencyRate(BaseModel):
    currency: str
    currency_value: float
    day: str
