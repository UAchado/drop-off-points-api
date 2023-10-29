import uvicorn
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status

import os
if os.environ.get("IN_DOCKER_CONTAINER"):
    from db_info import crud, database, schemas, models

    models.Base.metadata.create_all(bind = database.engine)

else:
    from .db_info import crud, database, schemas

app = FastAPI(title = "Drop-off Points API", description = "This API manages the drop-off points in UAchado System", version = "1.0.0")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/v1/")
def base():
    return {"response": "Hello World!"}

@app.get("/v1/points/", response_description = "Get the list of existing points.", response_model = list[schemas.Point], tags = ["Points"], status_code = status.HTTP_200_OK)
def get_all_points(db: Session = Depends(get_db)):
    points = crud.get_points(db)
    return points

@app.get("/v1/points/name/{point_name}", response_description = "Get a specific point by its name.", response_model = schemas.Point, tags = ["Points"], status_code = status.HTTP_200_OK)
def get_point(point_name: str, db: Session = Depends(get_db)):
    point = crud.get_point_by_name(db = db, name = point_name)
    if not point:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "POINT NOT FOUND")
    return point

@app.post("/v1/points/", response_description = "Create/Insert a new point.", response_model = schemas.Point, tags = ["Points"], status_code = status.HTTP_201_CREATED)
def create_point(point: schemas.PointCreate, db: Session = Depends(get_db)):
    if crud.get_point_by_name(db, name = point.name):
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "POINT ALREADY REGISTERED")
    return crud.create_point(db = db, new_point = point)

@app.delete("/v1/points/name/{point_name}", response_description = "Delete a specific point by its name.", tags = ["Points"], status_code = status.HTTP_200_OK)
def delete_point(point_name: str, db: Session = Depends(get_db)):
    if crud.delete_point(db, point_name) == None:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "POINT NOT FOUND")
    return {"message": "POINT DELETED"}

if __name__  == '__main__':
    uvicorn.run(app, host = '0.0.0.0', port = 8000)