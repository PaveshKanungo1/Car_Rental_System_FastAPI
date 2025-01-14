from datetime import datetime, timedelta, timezone
from jose import jwt
import os

SECRET_KEY = os.getenv('SECRET_KEY', default="SECRET_KEY")
ALGORITHM = os.getenv('ALGORITHM', default="ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

