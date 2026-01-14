from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta


SECRET_KEY = "patate2000"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

def create_access_token(data: dict)->str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt =jwt.encode(
        claims=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt