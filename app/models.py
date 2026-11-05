from .database import Base, SessionLocal
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, text

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key = True, nullable = False )
    title = Column(String, nullable = False)
    content = Column(String, nullable = True)
    published = Column(Boolean, nullable=False, server_default=text("true"))
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key= True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key= True)