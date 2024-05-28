from typing import List, Optional
from pydantic import BaseModel


class Ship(BaseModel):
    length: int

class Conditions(BaseModel):
    grid_size: int
    n_ships: int
    ships: List[Ship]
    vertical_limit: List[List[int]]
    horizontal_limit: List[List[int]]


class TestDataCreate(Conditions):
    pass


class TestDataBase(BaseModel):
    id: int
    grid_size: int
    n_ships: int
    ships: List[Ship]
    vertical_limit: List[List[int]]
    horizontal_limit: List[List[int]]

    class Config:
        orm_mode = True


class TestDataResponse(TestDataBase):
    user_id: int

class SolveRequestCreate(Conditions):
    pass

class SolveRequestBase(BaseModel):
    id: int
    status: str
    grid_size: int
    n_ships: int
    ships: List[Ship]
    vertical_limit: List[List[int]]
    horizontal_limit: List[List[int]]
    result: Optional[dict] = None

    class Config:
        orm_mode = True

class SolveRequestResponse(SolveRequestBase):
    user_id: int

class UserBase(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
