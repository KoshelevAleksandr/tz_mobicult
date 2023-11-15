import asyncio
from typing import List, Union

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models import rate
from schemas import TodayRate, Yesterday, BeforeYesterday, Rate
from config import REDIS_HOST, REDIS_PORT
from routers import router as test_router


app = FastAPI(
    title="tz_mobicult"
)


templates = Jinja2Templates(directory="templates")


app.include_router(test_router)


@app.get('/', response_model=Union[List[TodayRate], List[Yesterday], List[BeforeYesterday], List[Rate]])
async def get_currency_rate(day: str = 'today', session: AsyncSession = Depends(get_async_session)):
    query = select(rate)
    result = (await session.execute(query)).all()
    try:
        if isinstance(day, str) and day == 'today':
            return [TodayRate(id=el[0], currency=el[1], today=el[2]) for el in result]
        elif isinstance(day, str) and day == 'yesterday':
            return [Yesterday(id=el[0], currency=el[1], yesterday=el[3]) for el in result]
        elif isinstance(day, str) and day == 'before_yesterday':
            return [BeforeYesterday(id=el[0], currency=el[1], before_yesterday=el[4]) for el in result]
        else:
            return [Yesterday(id=el[0], currency=el[1], today=el[2], yesterday=el[3], before_yesterday=el[4]) for el in result]
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


# @app.get("/")
# def get_base_page(request: Request):
#     return templates.TemplateResponse("base.html", {"request": request})


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


