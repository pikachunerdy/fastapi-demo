import os
import asyncio
import motor

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from beanie import init_beanie
from celery import Celery
from app.api.configs.configs import Config, environmentSettings
from schemas.mongo_models.device_models import MongoDevice
from schemas.mongo_models.account_models import MongoCompany
from fastapi.responses import RedirectResponse

celery = Celery(__name__)
celery.conf.broker_url = environmentSettings.CELERY_BROKER_URL
celery.conf.result_backend = environmentSettings.CELERY_RESULT_BACKEND


app = FastAPI(
    title=Config.application_name,
)

from app.api.routes.device_routes import *
from app.api.routes.company_routes import *
from app.api.routes.device_registration_routes import *

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

@app.get('/')
def docs():
    return RedirectResponse('/docs')

@app.on_event("startup")
async def app_init():
    client = motor.motor_asyncio.AsyncIOMotorClient(environmentSettings.mongo_database_url)
    await init_beanie(database=client['test'] if environmentSettings.ENV == 'DEV' else client['main'],
    document_models=[MongoDevice,MongoCompany])
