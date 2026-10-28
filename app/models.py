from .database import Base, SessionLocal

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key = True, nullable = False )
    title = Column(String, nullable = True)
    content = Column(String, nullable = True)
    published = Column(Boolean, server_default="True")
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))