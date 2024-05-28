# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class TestData(Base):
    __tablename__ = "test_data"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    grid_size = Column(Integer)
    n_ships = Column(Integer)
    ships = Column(JSON)
    vertical_limit = Column(JSON)
    horizontal_limit = Column(JSON)
    user = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class SolveRequest(Base):
    __tablename__ = "solve_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    grid_size = Column(Integer)
    n_ships = Column(Integer)
    ships = Column(JSON)
    vertical_limit = Column(JSON)
    horizontal_limit = Column(JSON)
    status = Column(String, default="pending")
    user = relationship("User")
    result = Column(JSON, nullable=True)