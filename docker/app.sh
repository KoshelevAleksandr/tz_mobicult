#!/bin/bash

cd ..

#alembic revision --autogenerate -m "comment"

alembic upgrade head

cd api

#python init_database.py

uvicorn api.main:app --host 0.0.0.0 --port 8000

#gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

#python init_database.py