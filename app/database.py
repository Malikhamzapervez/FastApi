from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from .config import setting


SQLALCHEMY_DATABASE_URL = URL.create(
    "postgresql",
    username=setting.DATABASE_USERNAME,
    password=setting.DATABASE_PASSWORD,
    host=setting.DATABASE_HOSTNAME,
    port=setting.DATABASE_PORT,
    database=setting.DATABASE_NAME,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
