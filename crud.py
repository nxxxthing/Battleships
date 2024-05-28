"""Define database operations for the application."""

from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User, SolveRequest, TestData
from schemas import SolveRequestCreate, UserCreate, TestDataCreate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, username: str):
    """Retrieve a user from the database by username."""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    """Create a new user in the database."""
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_solve_request(db: Session, solve_request: SolveRequestCreate, user_id: int):
    """Create a new solve request in the database."""
    db_solve_request = SolveRequest(**solve_request.dict(), user_id=user_id, status="pending")
    db.add(db_solve_request)
    db.commit()
    db.refresh(db_solve_request)
    return db_solve_request


def get_solve_requests(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    """Retrieve solve requests for a specific user with pagination."""
    return db.query(SolveRequest).filter(SolveRequest.user_id == user_id).offset(skip).limit(limit).all()


def get_solve_request_by_id(db: Session, user_id: int, solve_request_id: int):
    """Retrieve a specific solve request for a specific user by ID."""
    return db.query(SolveRequest).filter(SolveRequest.user_id == user_id, SolveRequest.id == solve_request_id).first()


def update_solve_request_status_and_result(db: Session, solve_request_id: int, status: str,
                                           result: Optional[dict] = None):
    """Update the status and result of a solve request."""
    db_solve_request = db.query(SolveRequest).filter(SolveRequest.id == solve_request_id).first()
    db_solve_request.status = status
    if result:
        db_solve_request.result = result
    db.commit()
    db.refresh(db_solve_request)
    return db_solve_request


def update_solve_request_status(db: Session, solve_request_id: int, status: str):
    """Update the status of a solve request."""
    db_solve_request = db.query(SolveRequest).filter(SolveRequest.id == solve_request_id).first()
    db_solve_request.status = status
    db.commit()
    db.refresh(db_solve_request)
    return db_solve_request


def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user by username and password."""
    user = get_user(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_test_data(db: Session, test_data: TestDataCreate, user_id: int):
    """Create test data in the database."""
    db_test_data = TestData(**test_data.dict(), user_id=user_id)
    db.add(db_test_data)
    db.commit()
    db.refresh(db_test_data)
    return db_test_data


def get_test_data(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve test data with pagination."""
    return db.query(TestData).offset(skip).limit(limit).all()


def get_test_data_by_id(db: Session, test_data_id: int):
    """Retrieve specific test data by ID."""
    return db.query(TestData).filter(TestData.id == test_data_id).first()
