from passlib.context import CryptContext
# hashing and verifying of password happens here
passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(password: str):
    return passwordContext.hash(password)

def verify(plain, hashed):
    return passwordContext.verify(plain, hashed)