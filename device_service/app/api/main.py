'''App entry point'''

import random

import motor
from celery import Celery
from paho.mqtt import client as paho_client
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from beanie import init_beanie

from schemas.mongo_models.device_models import MongoDevice

from app.api.configs.configs import Config, environmentSettings
from app.api.routes.device_routes import *


celery = Celery(__name__)
celery.conf.broker_url = environmentSettings.CELERY_BROKER_URL
celery.conf.result_backend = environmentSettings.CELERY_RESULT_BACKEND

mqtt_client = paho_client.Client(
    Config.application_name + str(random.randint(0, 1000)))
if environmentSettings.ENV != "DEV":
    mqtt_client.username_pw_set(
        environmentSettings.mqtt_username, environmentSettings.mqtt_password)
mqtt_client.connect(environmentSettings.mqtt_broker_url, port=2883)

app = FastAPI(
    title=Config.application_name,
)

origins = [
    "http://localhost",
    "https://dashboard-deploy-h3gpr.ondigitalocean.app",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def app_init():
    '''Run when application starts'''
    client = motor.motor_asyncio.AsyncIOMotorClient(
        environmentSettings.mongo_database_url)
    await init_beanie(database=client.db_name, document_models=[MongoDevice])

if environmentSettings.ENV == "DEV":
    from app.api.routes.test_routes import *
