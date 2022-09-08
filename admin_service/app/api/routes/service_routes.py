# import time

# from fastapi.params import Depends
# from jose import jwt
# from pydantic import BaseModel
# from pydantic.fields import Field
# from fastapi import Body


# from app.api.configs.configs import environmentSettings
# from company_account_service.app.api.authentication.authentication import get_password_hash
# from company_account_service.app.api.sqlalchemy_models.manager import SQLServiceManager
# from company_account_service.app.api.sqlalchemy_models.models import SQLService, SQLServiceAuthKey
# from libs.authentication.admin_token_auth import TokenData, token_authentication
# from app.api.exceptions.authentication_exception import InvalidPermissionException
# from app.api.main import app
# from app.api.models.account_models import AccountInfo, Accounts, RegisterAccount, ModifyAccount
# from app.api.services.account_handler import AccountHandler
# from app.api.services.company_handler import CompanyHandler


# class AuthKey(BaseModel):
#     name: str
#     key: str

#     @staticmethod
#     def from_sql_auth_key(klass, sql_auth_key : SQLServiceAuthKey) -> 'AuthKey':
#         '''Convert to mnon'''
#         return klass(name=sql_auth_key.name, key=sql_auth_key.key)

# class Service(BaseModel):
#     name: str
#     auth_keys: list[AuthKey]

#     @staticmethod
#     def from_sql_service(klass, sql_service : SQLService) -> 'Service':
#         return klass(
#             name=sql_service.service_name,
#             auth_keys=[
#                 AuthKey.from_sql_auth_key(sql_auth_key)
#                 for sql_auth_key in sql_service.keys
#             ]
#         )

# @app.get('/admin/services/services', tags=['admin', 'services'], response_model=list[Service])
# async def get_services(token_data: TokenData = Depends(token_authentication)) -> list[Service]:
#     sql_services = await SQLServiceManager.get_SQLServices()
#     response = [
#         Service.from_sql_service(sql_service)
#         for sql_service in sql_services
#     ]
#     return response

# @app.post('/admin/services/service', tags=['admin', 'services'], response_model=Service)
# async def post_service(service_name : str, token_data: TokenData = Depends(token_authentication)) -> Service:
#     sql_service = await  SQLServiceManager.create_SQLService(service_name)
#     return Service.from_sql_service(sql_service)

# @app.delete('/admin/services/service', tags=['admin', 'services'])
# async def delete_service(service_name : str, token_data: TokenData = Depends(token_authentication)):
#     await SQLServiceManager.delete_SQLService(service_name)
#     return

# @app.post('/admin/services/auth_key', response_model=Service)
# async def post_service(service_name : str, key_name : str, token_data: TokenData = Depends(token_authentication)) -> Service:
#     sql_service = await  SQLServiceManager.create_SQLServiceAuthKey(service_name, key_name)
#     return Service.from_sql_service(sql_service)
