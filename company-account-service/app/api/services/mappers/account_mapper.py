from app.api.models.account_models import Account, AccountInfo, RegisterAccount
from app.api.sqlalchemy_models.models import SQLAccount
from app.api.services.mappers.permission_mapper import sqlpermissions_to_permissions, permissions_to_sqlpermissions

def sqlaccount_to_account_info(sqlaccount : SQLAccount) -> AccountInfo:
    account = AccountInfo.construct()
    account.email = sqlaccount.email
    account.company_id = str(sqlaccount.company_id)
    account.id = str(sqlaccount.account_id)
    account.permissions = sqlpermissions_to_permissions(sqlaccount.permissions)
    return account

def account_to_sqlaccount(account : Account) -> SQLAccount:
    sqlaccount = SQLAccount()
    sqlaccount.email = account.email
    sqlaccount.company_id = int(account.company_id)
    sqlaccount.permissions = permissions_to_sqlpermissions(account.permissions)
    return sqlaccount

def register_account_to_sqlaccount(register_account : RegisterAccount) -> SQLAccount:
    sqlaccount = SQLAccount()
    sqlaccount.email = register_account.email
    sqlaccount.permissions = permissions_to_sqlpermissions(register_account.permissions)
    return sqlaccount