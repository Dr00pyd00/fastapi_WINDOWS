from passlib.context import CryptContext


# ATTENTION a la version de passlib sur window...
# truc password hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pw(password:str):
    return pwd_context.hash(password)

def check_pw(plain_pw:str, db_pw:str)->bool:
    return pwd_context.verify(plain_pw, db_pw)
