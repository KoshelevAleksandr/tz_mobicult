from sqlalchemy import select

from database import SessionLocal

from models import rate
from operations import init_currency_rate, startup_update_currency_rate


def main():
    with SessionLocal() as db:
        query = (db.execute(select(rate))).all()
        if not query:
            init_currency_rate(db)
        else:
            startup_update_currency_rate(db)


if __name__ == "__main__":
    main()
