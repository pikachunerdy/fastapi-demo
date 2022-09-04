from jose import jwt
from passlib.context import CryptContext

from app.api.configs.configs import environmentSettings
from app.api.sqlalchemy_models.models import SQLAccount

from libs.authentication.user_token_auth import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(sqlaccount : SQLAccount, password : str):
    return verify_password(password, sqlaccount.password_hash)

def create_access_token(data: TokenData):
    to_encode = data.dict()
    encoded_jwt = jwt.encode(to_encode, environmentSettings.jwt_secret, algorithm=environmentSettings.jwt_algorithm)
    return encoded_jwt
