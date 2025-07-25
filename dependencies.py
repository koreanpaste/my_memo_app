from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.orm import Session,sessionmaker,relationship
from database import SessionLocal

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)
def verify_password_hash(plain_password,hashed_password)->bool:
    return pwd_context.verify(plain_password,hashed_password)
