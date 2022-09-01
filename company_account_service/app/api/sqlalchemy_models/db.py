from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker 
from app.api.configs.configs import environmentSettings
from app.api.sqlalchemy_models.models import Base, SQLAccount, SQLCompany, SQLPermissions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
import asyncio

import databases
import sqlalchemy
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)

# engine = create_async_engine(environmentSettings.database_url)
# async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
# print(environmentSettings.database_url)


database = databases.Database(environmentSettings.database_url)
# metadata = sqlalchemy.MetaData()
# engine = sqlalchemy.create_engine(
#     environmentSettings.database_url
# )
# metadata.create_all(engine)




# engine = create_async_engine(
#         "postgresql+asyncpg://scott:tiger@localhost/test",
#         echo=True,

# def create(klass):
#     if not (klass.__tablename__ in inspect(engine).get_table_names()): 
#         klass.__table__.create(bind = engine, checkfirst = True)

# create(SQLCompany)
# create(SQLPermissions)
# create(SQLAccount)
# session = Session()
