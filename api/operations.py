import requests

from datetime import date

from fastapi import Depends
from sqlalchemy import update, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import GetCurrencyRate
from database import get_async_session
from models import rate


def request_currency_rate_today():
    today_rate = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    rate_dict = {'USD': today_rate['Valute']['USD']['Value'],
                 'EUR': today_rate['Valute']['EUR']['Value']}
    return rate_dict


def request_currency_rate_yesterday():
    current_date = date.today()
    date_yesterday = f'{current_date.day - 1}/{current_date.month}/{current_date.year}'
    yesterday_rate = requests.get(f'https://www.cbr-xml-daily.ru/daily_json.js?date_req={date_yesterday}').json()
    rate_dict = {'USD': yesterday_rate['Valute']['USD']['Value'],
                 'EUR': yesterday_rate['Valute']['EUR']['Value']}
    return rate_dict


def request_currency_rate_before_yesterday():
    current_date = date.today()
    date_before_yesterday = f'{current_date.day - 2}/{current_date.month}/{current_date.year}'
    yesterday_rate = requests.get(f'https://www.cbr-xml-daily.ru/daily_json.js?date_req={date_before_yesterday}').json()
    rate_dict = {'USD': yesterday_rate['Valute']['USD']['Value'],
                 'EUR': yesterday_rate['Valute']['EUR']['Value']}
    return rate_dict


async def get_today_rate(day: str, session: AsyncSession = Depends(get_async_session)):
    query = select(rate.c.currency, rate.c.today)
    rates = (await session.execute(query)).all()
    result = [GetCurrencyRate(currency=item[1], currency_value=item[2], day=day) for item in rates]
    return result


async def get_yesterday_rate(day: str, session: AsyncSession = Depends(get_async_session)):
    query = select(rate.c.currency, rate.c.yesterday)
    rates = (await session.execute(query)).all()
    result = [GetCurrencyRate(currency=item[1], currency_value=item[2], day=day) for item in rates]
    return result


async def get_before_yesterday(day: str, session: AsyncSession = Depends(get_async_session)):
    query = select(rate.c.currency, rate.c.before_yesterday)
    rates = (await session.execute(query)).all()
    result = [GetCurrencyRate(currency=item[1], currency_value=item[2], day=day) for item in rates]
    return result


def init_currency_rate(session):
    today = request_currency_rate_today()
    yesterday_rate = request_currency_rate_yesterday()
    before_yesterday_rate = request_currency_rate_before_yesterday()
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
    session.execute(stmt_usd)
    session.execute(stmt_eur)
    session.commit()
    return {"status": "success"}


def startup_update_currency_rate(session):
    today = request_currency_rate_today()
    yesterday_rate = request_currency_rate_yesterday()
    before_yesterday_rate = request_currency_rate_before_yesterday()
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
