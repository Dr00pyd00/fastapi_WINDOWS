from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from app.schemas import TokenData, TokenOut
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

# endpoint vers OU on doit se connecter ( se login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

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


def verify_access_token(token: str, cred_exception: HTTPException)->TokenData:
    try:
        payload = jwt.decode(token=token,
                key=SECRET_KEY,
                algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if not id:
            raise cred_exception
        
        token_data = TokenData(id=id)
        return token_data
    except JWTError:
        raise cred_exception 


def get_current_user(token:str = Depends(oauth2_scheme)):
    cred_except = HTTPException(
       status_code=status.HTTP_401_UNAUTHORIZED,
       detail=f"Could not validate credentials...",
       headers={"WWW-Authenticate":"Bearer"}
    )
    return verify_access_token(token=token, cred_exception=cred_except)
