from re import L
from fastapi import FastAPI
from app.api.configs.configs import Config, environmentSettings
from starlette.middleware.cors import CORSMiddleware
from beanie import init_beanie
from schemas.device_mongo_models.device_models import MongoDevice
import motor
import os
import asyncio

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
   if os.getenv('FIRST_START') == 'true' or os.getenv('FIRST_START') is None:
        import pipes
        print("export FIRST_START=%s" % (pipes.quote('false')))
        await asyncio.sleep(15)
        from app.api.routes.test_routes import create_device
        await create_device()


# broker = Broker(brokerConfig.url)
# broker.create_all()
# broker.run()