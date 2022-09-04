from libs.authentication.user_token_auth import Permissions
from app.api.main import app
from app.api.models.account_models import Account
from app.api.services.account_handler import AccountHandler
from app.api.sqlalchemy_models.models import SQLCompany


@app.get('/create_user', tags=["Test"])
async def get_create_user():
    '''Create a fake user and company, the user name and password are test'''
    from app.api.main import async_session
    # async with async_session_maker() as session:
    async with async_session() as session:
        sqlCompany : SQLCompany = SQLCompany()
        sqlCompany.company_id = 0
        session.add(sqlCompany)
        await session.commit()
        account = Account.construct()
        account.email = "test"
        account.password = "test"
        account.company_id = sqlCompany.company_id
        permission : Permissions = Permissions.construct()
        permission.view_devices = True
        permission.register_devices = True
        permission.manage_devices  = True
        permission.manage_accounts  = True
        permission.view_device_data = True
        account.permissions = permission
        await AccountHandler.create_account(account, 0)
        print('created')
        return
