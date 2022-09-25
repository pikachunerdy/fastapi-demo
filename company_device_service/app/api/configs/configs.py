'''Config Settings'''

from pydantic import BaseSettings

class EnvironmentSettings(BaseSettings):
    '''Settings that use environment variables'''
    secret : str = "secret"
    jwt_secret : str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    jwt_algorithm : str = "HS256"
    token_url : str = "http:localhost:8000/token"
    local_run : bool = False
    mongo_database_url : str = 'mongodb://localhost:27017/'
    #"mongodb+srv://doadmin:sv1T8067gx2pq5Y9@company-device-service-690ea96d.mongo.ondigitalocean.com/admin?authSource=admin&replicaSet=company-device-service&tls=true&tlsCAFile=ca-certificate.crt"
    ENV : str = ""
    CELERY_BROKER_URL : str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND : str = "redis://localhost:6379"
    API_KEY : str = 'test'
    API_KEY_NAME : str = 'api_key'

environmentSettings = EnvironmentSettings()

class Config:
    '''Settings that can be hard coded'''
    application_name : str = "company-device-service"
    version : str = "0.0.1"
