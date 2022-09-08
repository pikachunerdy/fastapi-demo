# from cgitb import handler
# from app.api.sqlalchemy_models.models import SQLCompany
from app.api.models.account_models import Accounts
# from app.api.services.mappers.account_mapper import sqlaccount_to_account_info
# import app.api.sqlalchemy_models.manager as db_manager
from schemas.mongo_models.account_models import MongoCompany, MongoCompanyAccount
from app.api.services.account_handler import mongo_account_to_account_info

class CompanyHandler:

    # sql_company : SQLCompany
    _mongo_company : MongoCompany

    @classmethod
    async def create(klass, company_id : int):
        # sql_company = await db_manager.SQLCompanyManager.get_SQLCompany(company_id)
        # handler =  klass()
        # handler.sql_company = sql_company
        # return handler
        mongo_account = await MongoCompany.get(company_id)
        handler = klass()
        handler._mongo_company = mongo_account
        return handler

    async def get_company_accounts_list(self) -> Accounts:
        print('sbv skjbj')
        # accounts = Accounts.construct()
        # accounts.accounts = [sqlaccount_to_account_info(account) for account in self.sql_company.accounts]
        # return accounts
        print('lgjjbsdv')
        accounts = Accounts.construct()
        print('s;kdnsllbgnslkkbn')

        accounts.accounts = [mongo_account_to_account_info(mongo_account) async for mongo_account in MongoCompanyAccount.find_many(MongoCompanyAccount.company_id == self._mongo_company.id)]
        print(accounts.accounts)
        return accounts
