'''App entry point'''
import motor

from celery import Celery
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from beanie import init_beanie

from schemas.mongo_models.device_models import MongoDevice

from app.api.configs.configs import Config, environmentSettings


celery = Celery(__name__)
celery.conf.broker_url = environmentSettings.CELERY_BROKER_URL
celery.conf.result_backend = environmentSettings.CELERY_RESULT_BACKEND

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
    await init_beanie(
        database=client['test'] if environmentSettings.ENV == 'DEV' else client['main'],
        document_models=[MongoDevice])

from app.api.routes.device_routes import *
