from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

from Runner import Runner

app = FastAPI()


class Ship(BaseModel):
    length: int


class Conditions(BaseModel):
    grid_size: int
    n_ships: int
    ships: List[Ship]
    vertical_limit: List[List[int]]
    horizontal_limit: List[List[int]]


class Solution(BaseModel):
    grid: List[List[int]]


@app.post("/solve", response_model=Solution)
def solve_battleship(conditions: Conditions):
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
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e).strip())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)