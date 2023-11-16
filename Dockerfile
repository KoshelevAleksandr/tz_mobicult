FROM python:3.9

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /fastapi_app/docker

RUN chmod a+x ./app.sh

#RUN chmod a+x ./celery.sh


#WORKDIR /fastapi_app/api
#
#CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000