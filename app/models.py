from .database import Base, SessionLocal

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key = True, nullable = True )
    title = Column(String, nullable = True, index = True)
    content = Column(String, nullable = True, index = True)
    published = Column(Boolean, server_default="True")
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))


