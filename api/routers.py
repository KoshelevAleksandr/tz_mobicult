from fastapi import APIRouter, Depends
from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from operations import init_currency_rate
from models import rate
from database import get_async_session

router = APIRouter(prefix='/actions', tags=['Test'])


@router.get('/rates')
async def get_rates(session: AsyncSession = Depends(get_async_session)):
    query = select(rate)
    rates = await session.execute(query)
    return rates.all()


@router.post('/rates')
async def init_or_update_rates(session: AsyncSession = Depends(get_async_session)):
    init_currency_rate(session)
    return {"status": "error"}

#
# @router.put('/rates')
# async def update_rates(session: AsyncSession = Depends(get_async_session)):
#     old_usd = (await session.execute(select(rate).where(rate.c.currency == 'USD'))).all()[0]
#     old_eur = (await session.execute(select(rate).where(rate.c.currency == 'EUR'))).all()[0]
#     today_rate = request_currency_rate_today()
#     stmt_usd = update(rate).values(
#         currency='USD',
#         today=today_rate['USD'],
#         yesterday=old_usd[2],
#         before_yesterday=old_usd[3]).where(rate.c.currency == 'USD')
#     stmt_eur = update(rate).values(
#         currency='EUR',
#         today=today_rate['EUR'],
#         yesterday=old_eur[2],
#         before_yesterday=old_eur[3]).where(rate.c.currency == 'EUR')
#     await session.execute(stmt_usd)
#     await session.execute(stmt_eur)
#     await session.commit()
#     return {"status": "success"}


@router.delete('/rates')
async def delete_all_rates(session: AsyncSession = Depends(get_async_session)):
    stmt = delete(rate)
    await session.execute(stmt)
    await session.commit()
    return {"status": "delete"}
