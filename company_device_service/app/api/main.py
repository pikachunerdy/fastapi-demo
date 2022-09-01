import os
import asyncio
import motor

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from beanie import init_beanie
from celery import Celery
from app.api.configs.configs import Config, environmentSettings
from schemas.mongo_models.device_models import MongoDevice

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(environmentSettings.CELERY_BROKER_URL, "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(environmentSettings.CELERY_RESULT_BACKEND, "redis://localhost:6379")


app = FastAPI(
    title=Config.application_name,
)

from app.api.routes.device_routes import *
from app.api.routes.device_registration_routes import *
if environmentSettings.ENV == "DEV":
    from app.api.routes.test_routes import *

origins = [
    "http://localhost",
    "https://dashboard-deploy-h3gpr.ondigitalocean.app",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def app_init():
    client = motor.motor_asyncio.AsyncIOMotorClient(environmentSettings.mongo_database_url)
    await init_beanie(database=client.db_name, document_models=[MongoDevice])
    if environmentSettings.ENV == "DEV":
        with open('env.env','r') as file:
            first_load = file.read()

        if first_load != 'false' or first_load is None:
            with open('env.env','w') as file:
                file.write('false')
            await asyncio.sleep(15)
            from app.api.routes.test_routes import create_device
            await create_device()
