from pydantic import BaseSettings

class EnvironmentSettings(BaseSettings):
    measurements_api : str = "http://localhost:8002/measurements"
    ENV : str = ""


environmentSettings = EnvironmentSettings()

class Config:
    application_name : str = "company-account-service"
    version = "0.0.1"
