import uvicorn
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status

import os
if os.environ.get("IN_DOCKER_CONTAINER"):
    from db_info import crud, database, schemas
else:
    from .db_info import crud, database, schemas

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def base():
    return {"response": "Hello World!"}

@app.get("/points/", response_model = list[schemas.Point], status_code = status.HTTP_200_OK)
def get_all_points(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    points = crud.get_points(db, skip = skip, limit = limit)
    return points

@app.post("/points/", response_model = schemas.Point, status_code = status.HTTP_201_CREATED)
def create_point(point: schemas.PointCreate, db: Session = Depends(get_db)):
    db_point = crud.get_point_by_name(db, name = point.name)
    if db_point:
        raise HTTPException(status_code = 400, detail = "Point already registered")
    return crud.create_point(db = db, new_point = point)

@app.delete("/point/{point_name}", status_code = status.HTTP_200_OK)
def delete_point(point_name: str, db: Session = Depends(get_db)):
    point = crud.get_point_by_name(db, name = point_name)
    if crud.delete_point(db, point) == "OK":
        return {"message": "Point deleted"}
    return {"m  essage": "Error"}

if __name__  == '__main__':
    uvicorn.run(app, host = '0.0.0.0', port = 8000)