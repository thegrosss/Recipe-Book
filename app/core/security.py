from passlib.context import CryptContext

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    password_hash = crypt.hash(password)
    return password_hash

def verify_password(password: str, hashed_password: str) -> bool:
    return crypt.verify(password, hashed_password)