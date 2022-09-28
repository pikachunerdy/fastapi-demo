from pydantic import BaseSettings

class EnvironmentSettings(BaseSettings):
    DEVICE_SERVICE_URL : str = 'http://localhost:8002'
    ENV : str = ""
    API_KEY : str = 'test'
    API_KEY_NAME : str = 'api_key'


environmentSettings = EnvironmentSettings()

class Config:
    application_name : str = "company-account-service"
    version = "0.0.1"
    measurements_api : str = "/measurements"
    aes_api : str = '/aes_key'
