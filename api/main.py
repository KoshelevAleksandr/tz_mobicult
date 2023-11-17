from typing import List, Union

from fastapi import FastAPI, Depends, HTTPException


from fastapi_utils.tasks import repeat_every

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from operations import startup_update_currency_rate, init_currency_rate, get_today_rate, get_yesterday_rate, \
    get_before_yesterday
from database import get_async_session, SessionLocal
from models import rate
from routers import router as actions_router


app = FastAPI(
    title="tz_mobicult"
)


# app.include_router(actions_router)


@app.get('/')
async def second_rate(day: str = 'today', session: AsyncSession = Depends(get_async_session)):
    try:
        query_dict = {
            'today': get_today_rate,
            'yesterday': get_yesterday_rate,
            'before_yesterday': get_before_yesterday
        }
        result = await query_dict[day](day, session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@app.on_event("startup")
@repeat_every(seconds=10)
def startup():
    with SessionLocal() as db:
        query = (db.execute(select(rate))).all()
        if not query:
            init_currency_rate(db)
        else:
            startup_update_currency_rate(db)

