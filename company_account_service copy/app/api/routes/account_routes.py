'''Account Routes'''
import time

from fastapi.params import Depends
from fastapi import Body
from pydantic import BaseModel
from pydantic.fields import Field
import jwt

from app.api.configs import environmentSettings
from app.api.exceptions.authentication_exception import InvalidPermissionException
from app.api.main import app
from app.api.models.account_models import AccountInfo, Accounts, RegisterAccount, ModifyAccount
from app.api.services.account_handler import AccountHandler
from app.api.services.company_handler import CompanyHandler

from libs.authentication.user_token_auth import TokenData, token_authentication


@app.get('/accounts/accounts', response_model=Accounts, tags=["Account"])
async def get_accounts(token_data: TokenData = Depends(token_authentication)) -> Accounts:
    '''Get the list of accounts associated with a company, requires manage_accounts permission'''
    if not token_data.permission.manage_accounts:
        raise InvalidPermissionException(token_data, "")
    company_handler = await CompanyHandler.create(token_data.company_id)
    return await company_handler.get_company_accounts_list()


@app.get('/accounts/account/{account_id}', response_model=AccountInfo, tags=["Account"])
async def get_account(account_id: str,
                      token_data: TokenData = Depends(token_authentication)) -> AccountInfo:
    '''Get a specific account given the account id'''
    if not token_data.permission.manage_accounts:
        raise InvalidPermissionException(token_data, "")
    account_handler = await AccountHandler.create(account_id, token_data.company_id)
    account_info = account_handler.get_account_info()
    return account_info


@app.post('/accounts/account', response_model=AccountInfo, tags=["Account"])
async def post_account(new_account: RegisterAccount = Body(...),
                       token_data: TokenData = Depends(token_authentication)) -> AccountInfo:
    '''Create a new account'''
    if not token_data.permission.manage_accounts:
        raise InvalidPermissionException(token_data, "")
    account_info = await AccountHandler.create_account(new_account, token_data.company_id)
    return account_info


@app.put('/accounts/account', response_model=AccountInfo, tags=["Account"])
async def put_account(account: ModifyAccount = Body(...),
                      token_data: TokenData = Depends(token_authentication)) -> AccountInfo:
    '''Modify an account'''
    if not token_data.permission.manage_accounts:
        raise InvalidPermissionException(
            token_data, "Not able to modify accounts")
    account_handler = await AccountHandler.create(account.id, token_data.company_id)
    account_info = await account_handler.modify(account)
    return account_info


@app.delete('/accounts/account/{account_id}', tags=["Account"])
async def delete_account(account_id: str, token_data: TokenData = Depends(token_authentication)):
    '''Delete an account, requires manage_accounts permission'''
    if not token_data.permission.manage_accounts:
        raise InvalidPermissionException(token_data, "")
    account_handler = await AccountHandler.create(account_id, token_data.company_id)
    await account_handler.delete()
    return


class PasswordRequestToken(BaseModel):
    '''Token that validates a password reset for an email, sent to the email'''
    email: str
    expiry: int

@app.get('/accounts/password_link')
async def password_link(email: str):
    '''Sends a link to the email with a request to change the password'''
    email_link = ('http:/localhost:8001/' if environmentSettings.ENV ==
                  'DEV' else 'tbd') + '/password/'
    token = PasswordRequestToken(
        email=email,
        expiry=time.time() + 60*60*24
    )
    jwt.encode(token.dict(), environmentSettings.jwt_secret,
               algorithm=environmentSettings.jwt_algorithm)
    # TODO send email with link


class PasswordReset(BaseModel):
    '''Request to reset a password'''
    password: str = Field(max_length=50)
    email: str = Field(max_length=50)


@app.post('/account/password/{token')
async def post_password(token: str, reset_request: PasswordReset):
    '''Reset a password using the token sent in an email'''
    payload = PasswordRequestToken(**(jwt.decode(token, environmentSettings.jwt_secret,
                                                 algorithms=[environmentSettings.jwt_algorithm]))
                                   )
    if payload.email != reset_request.email:
        raise Exception
    if time.time() > payload.expiry:
        raise Exception
    handler = await AccountHandler.create_from_email(payload.email)
    await handler.change_password(reset_request.password)
