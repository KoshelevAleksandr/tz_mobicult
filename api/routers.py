from fastapi import APIRouter, Depends
from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

# from tasks import get_celery_rate
from operations import get_currency_rate_today, get_currency_rate_yesterday, get_currency_rate_before_yesterday
from models import rate
from database import get_async_session

router = APIRouter(prefix='/test', tags=['Test'])


@router.get('/g')
async def get_new_currency_rate(session: AsyncSession = Depends(get_async_session)):
    old_usd = (await session.execute(select(rate).where(rate.c.currency == 'USD'))).all()[0]
    old_eur = (await session.execute(select(rate).where(rate.c.currency == 'EUR'))).all()[0]
    today_rate = get_currency_rate_today()
    stmt_usd = update(rate).values(
        currency='USD',
        today=today_rate['USD'],
        yesterday=old_usd[2],
        before_yesterday=old_usd[3]).where(rate.c.currency == 'USD')
    stmt_eur = update(rate).values(
        currency='EUR',
        today=today_rate['EUR'],
        yesterday=old_eur[2],
        before_yesterday=old_eur[3]).where(rate.c.currency == 'EUR')
    await session.execute(stmt_usd)
    await session.execute(stmt_eur)
    await session.commit()
    return {"status": "success"}


@router.get('/rate')
async def get_rate(session: AsyncSession = Depends(get_async_session)):
    today = get_currency_rate_today()
    yesterday_rate = get_currency_rate_yesterday()
    before_yesterday_rate = get_currency_rate_before_yesterday()
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
    await session.execute(stmt_usd)
    await session.execute(stmt_eur)
    await session.commit()
    return {"status": "success"}



