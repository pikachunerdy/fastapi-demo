from fastapi import FastAPI
from app.api.configs.configs import Config, environmentSettings
from starlette.middleware.cors import CORSMiddleware
import asyncio
app = FastAPI(    
    title=Config.application_name
)

# origins = [
#     "https://dashboard-deploy-h3gpr.ondigitalocean.app/"
# ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    await asyncio.sleep(5)
    # metadata.create_all(engine)
    ...
    # from app.api.sqlalchemy_models.db import database
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    # await database.connect()
    # from app.api.sqlalchemy_models.db import engine
    # if environmentSettings.ENV == 'DEV':
    #     print('setup')
    #     async with engine.begin() as conn:
    #         # await conn.run_sync(Base.metadata.drop_all)
    #         await conn.run_sync(Base.metadata.create_all)
    #         print("Created")