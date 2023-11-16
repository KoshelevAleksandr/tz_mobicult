#!/bin/bash

cd api

if [[ "${1}" == "celery" ]]; then
  celery --app=tasks:celery worker -B -s /home/celery/var/run/celerybeat-schedule
elif [[ "${1}" == "flower" ]]; then
  celery --app=tasks:celery flower