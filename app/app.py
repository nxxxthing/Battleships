"""
FastAPI application for solving the battleship problem.

This module contains the FastAPI application that provides an endpoint for solving the battleship problem
based on the provided conditions. It defines the Conditions model for specifying the problem parameters
and implements the solve_battleship endpoint to return the solution grid.
"""

from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from runner import Runner


class Ship(BaseModel):
    """
    Represents a ship with a length.

    Attributes:
        length (int): The length of the ship.
    """
    length: int


app = FastAPI()


class Conditions(BaseModel):
    """
    Conditions for the battleship problem.

    This class defines the conditions required for solving the battleship problem,
    including the grid size, number of ships, ships' lengths, and limit lists for vertical and horizontal ships.

    Attributes:
        grid_size (int): The size of the square grid.
        n_ships (int): The number of ships.
        ships (List[Ship]): List of ships, each with its length.
        vertical_limit (List[List[int]]): List of limit lists for vertical ships.
        horizontal_limit (List[List[int]]): List of limit lists for horizontal ships.
    """
    grid_size: int
    n_ships: int
    ships: List[Ship]
    vertical_limit: List[List[int]]
    horizontal_limit: List[List[int]]


@app.post("/solve")
def solve_battleship(conditions: Conditions):
    """
    Solve the battleship problem based on the provided conditions.

    This endpoint receives conditions for the battleship problem and returns the solution if found.

    Parameters:
        conditions (Conditions): The conditions for the battleship problem.

    Returns:
        JSONResponse: The solution grid if found.

    Raises:
        HTTPException: If an error occurs during the solving process.
    """
    ships = [Ship(length=ship.length) for ship in conditions.ships]

    runner = Runner(
        grid_size=conditions.grid_size,
        n_ships=conditions.n_ships,
        ships=ships,
        vertical_limit=conditions.vertical_limit,
        horizontal_limit=conditions.horizontal_limit
    )

    try:
        runner.run()
        result_grid = runner.result()
        return JSONResponse(content={"grid": result_grid})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
