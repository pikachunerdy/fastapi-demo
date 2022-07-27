from fastapi import FastAPI
from app.api.configs.configs import Config, environmentSettings
from starlette.middleware.cors import CORSMiddleware
import asyncio
import os

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
if environmentSettings.ENV == "DEV": 
    from app.api.routes.test_routes import *


# from app.api.sqlalchemy_models.db import engine
from app.api.sqlalchemy_models.models import Base

from app.api.sqlalchemy_models.models import metadata
import sqlalchemy
# metadata = sqlalchemy.MetaData()
# engine = sqlalchemy.create_engine(
#     environmentSettings.database_url
# )
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_async_engine(environmentSettings.database_url, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@app.on_event("startup")
async def startup():
    if environmentSettings.ENV == "DEV":
        import os 
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path)
        with open(dir_path + '/env.env','r') as file:
            first_load = file.read()

        if first_load != 'false' or first_load is None:
            with open(dir_path + '/env.env','w') as file:
                file.write('false')
            import pipes
            print("export FIRST_START=%s" % (pipes.quote('false')))
            await asyncio.sleep(15)
            async with engine.begin() as conn:
                await conn.run_sync(metadata.drop_all)
                await conn.run_sync(metadata.create_all)
            from app.api.routes.test_routes import get_create_user
            await get_create_user()

        
