from app.api.sqlalchemy_models.models import SQLCompany, SQLAccount, SQLPermissions, SQLService, SQLServiceAuthKey
from sqlalchemy.orm import sessionmaker, selectinload , subqueryload, joinedload
from sqlalchemy.future import select
from app.api.main import async_session
import secrets
import string

class SQLAccountManger:


    @staticmethod
    async def get_SQLAccount(account_id : int, company_id : int) -> SQLAccount:
        async with async_session() as session:
            account_id = int(account_id)
            company_id = int(company_id)
            account = (await session.execute(select(SQLAccount).options(selectinload(SQLAccount.permissions)).where(SQLAccount.account_id == account_id, SQLAccount.company_id == company_id).limit(1)))
            if account is not None:
                account = account.scalars().first()
        return account

    @staticmethod
    async def get_SQLAccount_with_email(email : str) -> SQLAccount:
        async with async_session() as session:
            # company = await session.query(SQLAccount).filter_by(email = email).first()
            account = (await session.execute(select(SQLAccount).options(selectinload(SQLAccount.permissions)).where(SQLAccount.email == email).limit(1)))
            if account is not None:
                account = account.scalars().first()
            print(account)
        return account

    @staticmethod
    async def save_SQLAccount(account : SQLAccount):
        async with async_session() as session:
            session.add(account)
            await session.commit()

    @staticmethod
    async def delete_SQLAccount(account : SQLAccount):
        async with async_session() as session:
            await session.delete(account)
            await session.commit()

class SQLCompanyManager:

    @staticmethod
    async def get_SQLCompany(company_id : int) -> SQLCompany:
        async with async_session() as session:
            company_id = int(company_id)
            company = (await session.execute(select(SQLCompany).options(joinedload(SQLCompany.accounts).subqueryload(SQLAccount.permissions)).where(SQLCompany.company_id == company_id).limit(1)))
            if company is not None:
                company = company.scalars().first()
        return company

    @staticmethod
    async def save_SQLCompany(company : SQLCompany):
        async with async_session() as session:
            session.add(company)
            await session.commit()

class SQLServiceManager:

    @staticmethod
    async def get_SQLServices() -> list[SQLService]:
        ...

    @staticmethod
    async def create_SQLService(service_name : str) -> SQLService:
        sql_service = SQLService(service_name = service_name)
        async with async_session() as session:
            session.add(sql_service)
            await session.commit()
        return sql_service

    @staticmethod
    async def delete_SQLService(service_name : str):
        async with async_session() as session:
            sql_service = (await session.execute(select(SQLService).where(SQLService.service_name == service_name).limit(1)))
            if sql_service is None:
                raise Exception
            await session.delete(sql_service)
            await session.commit()

    @staticmethod
    async def create_SQLServiceAuthKey(service_name : str, key_name : str) -> SQLService:
        async with async_session() as session:
            sql_service = (await session.execute(select(SQLService).where(SQLService.service_name == service_name).limit(1)))
            if sql_service is None:
                raise Exception
            # secure random string
            secure_str = ''.join((secrets.choice(string.ascii_letters) for i in range(64)))
            sql_auth_key = SQLServiceAuthKey(name = key_name, key = secure_str)
            session.add(sql_auth_key)
            sql_service.keys.append(sql_auth_key)
            session.add(sql_service)
            await session.commit()

    @staticmethod
    async def delete_SQLServiceAuthKey(service_name : str, key_name : str) -> SQLService:
        ...
