from fastapi import Depends
from sqlalchemy import update, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session, Session

from models import rate
from operations import get_currency_rate_today, get_currency_rate_yesterday, get_currency_rate_before_yesterday, \
    init_currency_rate, startup_update_currency_rate


# async def init_currency_rate(session):
#     today = get_currency_rate_today()
#     yesterday_rate = get_currency_rate_yesterday()
#     before_yesterday_rate = get_currency_rate_before_yesterday()
#     stmt_usd = insert(rate).values(
#         currency='USD',
#         today=today['USD'],
#         yesterday=yesterday_rate['USD'],
#         before_yesterday=before_yesterday_rate['USD'])
#     stmt_eur = insert(rate).values(
#         currency='EUR',
#         today=today['EUR'],
#         yesterday=yesterday_rate['EUR'],
#         before_yesterday=before_yesterday_rate['EUR'])
#     await session.execute(stmt_usd)
#     await session.execute(stmt_eur)
#     await session.commit()
#     return {"status": "success"}
#
#
# async def startup_update_currency_rate(session):
#     today = get_currency_rate_today()
#     yesterday_rate = get_currency_rate_yesterday()
#     before_yesterday_rate = get_currency_rate_before_yesterday()
#     stmt_usd = update(rate).values(
#         currency='USD',
#         today=today['USD'],
#         yesterday=yesterday_rate['USD'],
#         before_yesterday=before_yesterday_rate['USD']).where(rate.c.currency == 'USD')
#     stmt_eur = update(rate).values(
#         currency='EUR',
#         today=today['EUR'],
#         yesterday=yesterday_rate['EUR'],
#         before_yesterday=before_yesterday_rate['EUR']).where(rate.c.currency == 'EUR')
#     await session.execute(stmt_usd)
#     await session.execute(stmt_eur)
#     await session.commit()
#     return {"status": "success"}


def main():
    with Session() as db:
        query = (db.execute(select(rate))).all()
        print(query)
        if not query:
            init_currency_rate(db)
        else:
            startup_update_currency_rate(db)


if __name__ == "__main__":
    main()
