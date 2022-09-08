from app.api.models.account_models import AccountInfo, Account, Permissions, RegisterAccount, ModifyAccount
# from app.api.sqlalchemy_models.models import SQLAccount
from app.api.authentication.authentication import get_password_hash
# from app.api.services.mappers.account_mapper import sqlaccount_to_account_info, account_to_sqlaccount, register_account_to_sqlaccount
# from app.api.services.mappers.permission_mapper import permissions_to_sqlpermissions
# from app.api.sqlalchemy_models.manager import SQLAccountManger, SQLCompanyManager
from schemas.mongo_models.account_models import MongoCompanyAccount, MongoPermissions


def mongo_account_to_account_info(mongo_account: MongoCompanyAccount) -> AccountInfo:
    account_info = AccountInfo.construct()
    account_info.company_id = mongo_account.company_id
    account_info.email = mongo_account.email
    account_info.id = mongo_account.id
    account_info.permissions = mongo_account.permissions
    return account_info
#     raise NotImplementedError()

def permissions_to_mongo_permissions(permissions: Permissions) -> MongoPermissions:
    mongo_permissions = MongoPermissions.construct()
    return mongo_permissions.permissions
    # raise NotImplementedError()

class AccountHandler:

    # _sql_account : SQLAccount
    _mongo_account: MongoCompanyAccount

    @classmethod
    async def create(klass, account_id: str, company_id: str):
        # _sql_account = await SQLAccountManger.get_SQLAccount(account_id, company_id)
        mongo_account = await MongoCompanyAccount.find(
            MongoCompanyAccount.id == account_id,
            MongoCompanyAccount.company_id == company_id
        ).first_or_none()
        if mongo_account is None:
            raise Exception
        handler = klass()
        handler._mongo_account = mongo_account
        return handler

    @classmethod
    async def create_from_email(klass, email: str):
        # _sql_account = await SQLAccountManger.get_SQLAccount_with_email(email)
        mongo_account = await MongoCompanyAccount.find(
            MongoCompanyAccount.email == email,
        ).first_or_none()
        handler = klass()
        # handler._sql_account = _sql_account
        handler._mongo_account = mongo_account
        return handler

    @staticmethod
    async def create_account(register_account: RegisterAccount, company_id: str) -> AccountInfo:
        # sqlaccount = await SQLAccountManger.get_SQLAccount_with_email(new_account.email)
        mongo_account = await MongoCompanyAccount.find(
            MongoCompanyAccount.email == register_account.email,
        ).first_or_none()
        if mongo_account is not None:
            raise Exception()
        # sqlaccount = register_account_to_sqlaccount(new_account)
        # sqlaccount.password_hash = get_password_hash(new_account.password)
        # sqlaccount.company_id = int(company_id)
        # await SQLAccountManger.save_SQLAccount(sqlaccount)
        # return sqlaccount_to_account_info(sqlaccount)
        # mongo_account = register_account_to_mongo_account(register_account)
        mongo_account = MongoCompanyAccount.construct()
        mongo_account.email = register_account.email
        mongo_account.permissions = register_account.permissions
        mongo_account.password_hash = get_password_hash(register_account.password)
        mongo_account.company_id = company_id
        await mongo_account.save()
        return mongo_account_to_account_info(mongo_account)


    def get_account_info(self) -> AccountInfo:
        return mongo_account_to_account_info(self._mongo_account)
        # return sqlaccount_to_account_info(self._sql_account)

    async def delete(self):
        # sql_company = await SQLCompanyManager.get_SQLCompany(self._sql_account.company_id)
        # if sql_company.master_account_id == self._sql_account.account_id:
        #     raise Exception
        # await SQLAccountManger.delete_SQLAccount(self._sql_account)
        if self._mongo_account.master_account:
            raise Exception
        await self._mongo_account.delete()

    async def modify(self, account: ModifyAccount) -> AccountInfo:
        # self._sql_account. = account.email
        # self._sql_account.permissions = permissions_to_sqlpermissions(
        #     account.permissions)
        # await SQLAccountManger.save_SQLAccount(self._sql_account)
        # return sqlaccount_to_account_info(self._sql_account)
        self._mongo_account.permissions = permissions_to_mongo_permissions(account.permissions)
        await self._mongo_account.save()
        return mongo_account_to_account_info(self._mongo_account)

    async def change_password(self, new_password: str):
        # self._sql_account.password_hash = get_password_hash(new_password)
        # await SQLAccountManger.save_SQLAccount(self._sql_account)
        self._mongo_account.password_hash = get_password_hash(new_password)
        await self._mongo_account.save()
