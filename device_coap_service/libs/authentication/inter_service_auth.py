'''Provide a dependency for authenticating interservice requests'''

from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.security.api_key import APIKeyHeader

from app.api.configs.configs import environmentSettings


api_key_header = APIKeyHeader(name=environmentSettings.API_KEY_NAME, auto_error=False)

async def validate_api_key(api_key: str = Security(api_key_header)):
    '''Validate that the API key is correct'''
    if api_key == environmentSettings.API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
