from re import L
from fastapi import FastAPI
from app.api.configs.configs import Config, environmentSettings
from starlette.middleware.cors import CORSMiddleware
from beanie import init_beanie
from schemas.device_mongo_models.device_models import MongoDevice
import motor
import os
import asyncio

from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


app = FastAPI(
    title=Config.application_name, 
    #version=Config.version
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
        import os 
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/env.env','r') as file:
            first_load = file.read()

        if first_load != 'false' or first_load is None:
            with open(dir_path + '/env.env','w') as file:
                file.write('false')
            await asyncio.sleep(15)
            from app.api.routes.test_routes import create_device
            await create_device()


# broker = Broker(brokerConfig.url)
# broker.create_all()
# broker.run()