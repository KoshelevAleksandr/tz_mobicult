from typing import List, Union

from fastapi import FastAPI, Depends, HTTPException


from fastapi_utils.tasks import repeat_every

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from operations import init_currency_rate, get_today_rate
from database import get_async_session, SessionLocal
from models import rate
from routers import router as actions_router


app = FastAPI(
    title="tz_mobicult"
)


app.include_router(actions_router)


@app.get('/')
async def second_rate(day: str = 'today', session: AsyncSession = Depends(get_async_session)):
    try:
        result = await get_today_rate(day, session)
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
        init_currency_rate(db)
