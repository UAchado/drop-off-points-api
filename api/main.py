from typing import Optional
import uvicorn
import os

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Request, status
from dotenv import load_dotenv, dotenv_values

ENV_FILE_PATH = os.getenv("ENV_FILE_PATH")
load_dotenv(ENV_FILE_PATH)

from db_info import crud, database, schemas, auth, init_db
database.Base.metadata.create_all(bind = database.engine)

app = FastAPI(title = "Drop-off Points API", description = "This API manages the drop-off points in UAchado System", version = "1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost"],  # Allows all origins to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def get_db():
    """
    Obtain a database session for use within a context block.

    :return: A database session.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

## INIT DB

@app.on_event("startup")
async def startup_event():
    """
    Handles the startup event of the application.

    The startup event is triggered when the application starts. This method performs a check to see if there are any points in the database. If there are no points, it initializes the database
    * with some initial data.

    :return: None
    """
    db = database.SessionLocal()
    try:
        if crud.get_points(db) == []:
            init_db.init(db)
    finally:
        db.close()

## ENDPOINTS

@app.get("/points/v1")
def base():
    """
    Returns a dictionary with the response message.

    :return: A dictionary with the response message.
    :rtype: dict
    """
    return {"response": "Hello World!"}

@app.get("/points/v1/points", response_description = "Get the list of existing points.",
         response_model = list[schemas.Point], tags = ["Points"], status_code = status.HTTP_200_OK)
def get_all_points(db: Session = Depends(get_db)):
    """
    :param db: The database session to use for retrieving points.
    :return: A list of existing points.
    """
    points = crud.get_points(db)
    return points

@app.get("/points/v1/points/name/{point_name}", response_description = "Get a specific point by its name.",
         response_model = schemas.Point, tags = ["Points"], status_code = status.HTTP_200_OK)
def get_point(point_name: str,
              db: Session = Depends(get_db)):
    """
    .. py:function:: get_point(point_name: str, db: Session)

       Get a specific point by its name.

       :param point_name: The name of the point.
       :type point_name: str
       :param db: The database session.
       :type db: Session
       :return: The details of the point.
       :rtype: schemas.Point
       :raise HTTPException: If the point is not found.

    """
    point = crud.get_point_by_name(db = db, name = point_name)
    if not point:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "POINT NOT FOUND")
    return point

@app.post("/points/v1/points", response_description = "Create/Insert a new point.",
          response_model = schemas.Point, tags = ["Points"], status_code = status.HTTP_201_CREATED)
def create_point(request: Request,
                 point: schemas.PointCreate,
                 db: Session = Depends(get_db)):
    """
    :param request: The HTTP request object.
    :param point: The payload data to create a new point.
    :param db: The database session object.
    :return: The created point object.
    """
    auth.verify_access(request)
    if crud.get_point_by_name(db, name = point.name):
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "POINT ALREADY REGISTERED")
    return crud.create_point(db = db, new_point = point)


@app.get("/points/v1/access", response_description = "Get a specific point by its name.",
         response_model = Optional[int], tags = ["Points"], status_code = status.HTTP_200_OK)
def get_point_id_of_access(request: Request,
                           db: Session = Depends(get_db)):
    """
    **get_point_id_of_access**

    Get the access point ID for a specific point by its name.

    :param request: The request object containing the access information.
    :param db: The database session.

    :return: The access point ID as an optional integer.

    :raises HTTPException: Raises an exception if the access point is not found.

    Example usage:

    ```python
    access_point_id = get_point_id_of_access(request=request, db=db)
    ```

    """
    auth.verify_access(request)
    access_point_id = crud.get_auth(db = db, request = request)
    if not access_point_id:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "ACCESS NOT FOUND")
    return access_point_id

@app.delete("/points/v1/points/name/{point_name}", response_description = "Delete a specific point by its name.",
            tags = ["Points"], status_code = status.HTTP_200_OK)
def delete_point(request: Request,
                 point_name: str,
                 db: Session = Depends(get_db)):
    """
    Deletes a specific point by its name.

    :param request: The request object.
    :param point_name: The name of the point to delete.
    :param db: The database session object.
    :return: A message indicating whether the point was successfully deleted or not.
    :rtype: dict
    """
    auth.verify_access(request)
    if crud.delete_point(db, point_name) == None:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "POINT NOT FOUND")
    return {"message": "POINT DELETED"}

if __name__  == '__main__':
    uvicorn.run(app, host = '0.0.0.0', port = 8000)