import requests

from datetime import date

from fastapi import Depends
from sqlalchemy import update, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import GetCurrencyRate
from database import get_async_session
from models import rate


def request_currency_rate(day):
    current_date = date.today()
    day_delta = {
        'today': 0,
        'yesterday': 1,
        'before_yesterday': 2,
    }
    date_yesterday = f'{current_date.day - day_delta[day]}/{current_date.month}/{current_date.year}'
    currency_rate_for_day = requests.get(f'https://www.cbr-xml-daily.ru/daily_json.js?date_req={date_yesterday}').json()
    rate_dict = {'USD': currency_rate_for_day['Valute']['USD']['Value'],
                 'EUR': currency_rate_for_day['Valute']['EUR']['Value']}
    return rate_dict


async def get_today_rate(day: str, session: AsyncSession = Depends(get_async_session)):
    query = select(rate)
    rates = (await session.execute(query)).all()
    print(rates)
    if day == 'today':
        result = [GetCurrencyRate(currency=item[1], currency_value=item[2], day=day) for item in rates]
    elif day == 'yesterday':
        result = [GetCurrencyRate(currency=item[1], currency_value=item[2], day=day) for item in rates]
    elif day == 'before_yesterday':
        result = [GetCurrencyRate(currency=item[1], currency_value=item[2], day=day) for item in rates]
    else:
        result = 'Неверно указан день'
    return result


def init_currency_rate(session):
    today = request_currency_rate('today')
    yesterday_rate = request_currency_rate('yesterday')
    before_yesterday_rate = request_currency_rate('before_yesterday')
    query = (session.execute(select(rate))).all()
    if not query:
        stmt_usd = insert(rate).values(
            currency='USD',
            today=today['USD'],
            yesterday=yesterday_rate['USD'],
            before_yesterday=before_yesterday_rate['USD'])
        stmt_eur = insert(rate).values(
            currency='EUR',
            today=today['EUR'],
            yesterday=yesterday_rate['EUR'],
            before_yesterday=before_yesterday_rate['EUR'])
    else:
        stmt_usd = update(rate).values(
            currency='USD',
            today=today['USD'],
            yesterday=yesterday_rate['USD'],
            before_yesterday=before_yesterday_rate['USD']).where(rate.c.currency == 'USD')
        stmt_eur = update(rate).values(
            currency='EUR',
            today=today['EUR'],
            yesterday=yesterday_rate['EUR'],
            before_yesterday=before_yesterday_rate['EUR']).where(rate.c.currency == 'EUR')
    session.execute(stmt_usd)
    session.execute(stmt_eur)
    session.commit()
    return {"status": "success"}
