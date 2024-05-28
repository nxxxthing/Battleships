"""Define schemas for your application."""

from typing import List, Optional
from pydantic import BaseModel


class Ship(BaseModel):
    """Model representing a ship with a length."""
    length: int


class Conditions(BaseModel):
    """Model representing conditions for the battleship problem."""
    grid_size: int
    n_ships: int
    ships: List[Ship]
    vertical_limit: List[List[int]]
    horizontal_limit: List[List[int]]


class TestDataCreate(Conditions):
    """Model representing data for creating test data."""


class TestDataBase(BaseModel):
    """Base model representing test data."""
    id: int
    grid_size: int
    n_ships: int
    ships: List[Ship]
    vertical_limit: List[List[int]]
    horizontal_limit: List[List[int]]

    class Config:
        """Pydantic model configuration."""
        orm_mode = True


class TestDataResponse(TestDataBase):
    """Model representing response data for test data."""
    user_id: int


class SolveRequestCreate(Conditions):
    """Model representing data for creating a solve request."""


class SolveRequestBase(BaseModel):
    """Base model representing a solve request."""
    id: int
    status: str
    grid_size: int
    n_ships: int
    ships: List[Ship]
    vertical_limit: List[List[int]]
    horizontal_limit: List[List[int]]
    result: Optional[dict] = None

    class Config:
        """Pydantic model configuration."""
        orm_mode = True


class SolveRequestResponse(SolveRequestBase):
    """Model representing response data for a solve request."""
    user_id: int


class UserBase(BaseModel):
    """Base model representing a user."""
    id: int
    username: str

    class Config:
        """Pydantic model configuration."""
        orm_mode = True


class UserCreate(UserBase):
    """Model representing data for creating a user."""
    password: str


class UserInDB(UserBase):
    """Model representing a user in the database."""
    hashed_password: str
