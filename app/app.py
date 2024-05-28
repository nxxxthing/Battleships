"""
FastAPI application for solving the battleship problem.

This module contains the FastAPI application that provides an endpoint for solving the battleship problem
based on the provided conditions. It defines the Conditions model for specifying the problem parameters
and implements the solve_battleship endpoint to return the solution grid.
"""

from typing import List
import asyncio
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import models
import schemas
from runner import Runner

models.Base.metadata.create_all(bind=engine)

security = HTTPBasic()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """Middleware to check if user is authenticated"""
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    """Method to get database"""
    return request.state.db


def get_current_username(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    """get username of authenticated user"""
    user = crud.authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user.username


@app.post("/register", response_model=schemas.UserBase)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """registers a new user"""
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Get documentation ui"""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Custom Swagger UI"
    )


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    """json for documentation"""
    return app.openapi()


@app.post("/solve", response_model=schemas.SolveRequestResponse)
async def solve_battleship(conditions: schemas.SolveRequestCreate, username: str = Depends(get_current_username),
                           db: Session = Depends(get_db)):
    """
    Create a new solve request and store the submitted data as test data.
    """
    user = crud.get_user(db, username=username)
    solve_request = crud.create_solve_request(db, conditions, user_id=user.id)
    crud.create_test_data(db, conditions, user_id=user.id)

    async def run_solver():
        try:
            crud.update_solve_request_status_and_result(db, solve_request.id, "solving")
            runner = Runner(
                grid_size=conditions.grid_size,
                n_ships=conditions.n_ships,
                ships=conditions.ships,
                vertical_limit=conditions.vertical_limit,
                horizontal_limit=conditions.horizontal_limit
            )
            runner.run()
            result_grid = runner.result()
            crud.update_solve_request_status_and_result(db, solve_request.id, "solved", result={"grid": result_grid})
        except Exception:
            crud.update_solve_request_status_and_result(db, solve_request.id, "failed")

    asyncio.create_task(run_solver())

    return solve_request


@app.get("/testdata", response_model=List[schemas.TestDataResponse])
def get_test_data(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve all test data with pagination.
    """
    test_data = crud.get_test_data(db, skip=skip, limit=limit)
    return test_data


@app.get("/testdata/{test_data_id}", response_model=schemas.TestDataResponse)
def get_test_data_by_id(test_data_id: int, db: Session = Depends(get_db)):
    """
    Retrieve specific test data by ID.
    """
    test_data = crud.get_test_data_by_id(db, test_data_id=test_data_id)
    if not test_data:
        raise HTTPException(status_code=404, detail="Test data not found")
    return test_data


@app.get("/solve_requests", response_model=List[schemas.SolveRequestResponse])
def get_solve_requests(skip: int = 0, limit: int = 10, username: str = Depends(get_current_username),
                       db: Session = Depends(get_db)):
    """View my solve requests"""
    user = crud.get_user(db, username=username)
    solve_requests = crud.get_solve_requests(db, user_id=user.id, skip=skip, limit=limit)
    return solve_requests


@app.get("/solve_requests/{solve_request_id}", response_model=schemas.SolveRequestResponse)
def get_solve_request(solve_request_id: int, username: str = Depends(get_current_username),
                      db: Session = Depends(get_db)):
    """View single solve request"""
    user = crud.get_user(db, username=username)
    solve_request = crud.get_solve_request_by_id(db, user_id=user.id, solve_request_id=solve_request_id)
    if not solve_request:
        raise HTTPException(status_code=404, detail="Solve request not found")
    return solve_request


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
