from fastapi import FastAPI
from app.api.configs.configs import Config, environmentSettings
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import asyncio
import os
import motor
from beanie import init_beanie
from schemas.mongo_models.account_models import MongoCompany, MongoCompanyAccount

app = FastAPI(
    title=Config.application_name
)


origins = [
    "http://localhost",
    "https://dashboard-deploy-h3gpr.ondigitalocean.app",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.routes.account_routes import *
from app.api.routes.authentication_routes import *

# from app.api.sqlalchemy_models.models import Base

# from app.api.sqlalchemy_models.models import metadata
# import sqlalchemy
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import declarative_base, sessionmaker

# engine = create_async_engine(environmentSettings.database_url, future=True, echo=True)
# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@app.get('/')
def docs():
    '''Redirect to docs'''
    return RedirectResponse('/docs')


@app.on_event("startup")
async def app_init():
    '''App start up code'''
    client = motor.motor_asyncio.AsyncIOMotorClient(environmentSettings.mongo_database_url)
    await init_beanie(database=client['test'] if environmentSettings.ENV == 'DEV' else client['main'], document_models=[MongoCompany,MongoCompanyAccount])
