from os import getenv
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from uvicorn import run

ENV_FILE_PATH = getenv("ENV_FILE_PATH")
load_dotenv(ENV_FILE_PATH)

from db_info import auth, crud, database, init_db, schemas

database.Base.metadata.create_all(bind = database.engine)

app = FastAPI(title = "Drop-off Points API",
              summary = "Drop-off Points API for UAchado App",
              description = "This API manages the drop-off points in UAchado system. It helps with the logic inside the system.",
              version = "1.0.0",
              openapi_url = "/points/v1/openapi.json",
              docs_url="/points/v1/docs",
              redoc_url="/points/v1/redocs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost"],  # Allows all origins to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

## HELPER FUNCTIONS

def get_db():
    """
    Get the database session from the SessionLocal object which the API can connect to.

    Return:
        A database session.
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
    Startup Event

    This method is an event handler for the "startup" event. It initializes the database if there are no items in it.

    Return:
        None
    """
    db = database.SessionLocal()
    try:
        if crud.get_points(db) == []:
            init_db.init(db)
    finally:
        db.close()

## ENDPOINTS

@app.get("/points/v1",
         response_description = "Root endpoint of the dropoff points API.",
         response_model = dict,
         tags = ["Points"],
         status_code = status.HTTP_200_OK)
def base() -> dict:
    """
    Root endpoint of the dropoff points API. Mostly used for testing API connectivity.

    Returns:
        _type_: A dictionary containing the response message.
    """
    return {"response": "Hello World!"}

@app.get("/points/v1/points",
         response_description = "Get the list of existing points.",
         response_model = List[schemas.Point],
         tags = ["Points"],
         status_code = status.HTTP_200_OK)
def get_all_points(db: Session = Depends(get_db)) -> List[schemas.Point]:
    """
    Get the list of existing points.

    Args:
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Returns:
        List[schemas.Point]: A list of existing points.
    """    
    return crud.get_points(db)

@app.get("/points/v1/points/name/{point_name}",
         response_description = "Get a specific point by its name.",
         response_model = schemas.Point,
         tags = ["Points"],
         status_code = status.HTTP_200_OK)
def get_point(point_name: str,
              db: Session = Depends(get_db)) -> schemas.Point:
    """
    Get a specific point by its name.

    Args:
        point_name (str): The name attribute of a specify unique point.
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Raises:
        HTTPException (HTTP_204_NO_CONTENT): Error raised if there's no stored point with that name.

    Returns:
        schemas.Point: The stored point.
    """
    point = crud.get_point_by_name(db = db, name = point_name)
    if not point:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "POINT NOT FOUND")
    return point

@app.post("/points/v1/points",
          response_description = "Create a new point.",
          response_model = schemas.Point,
          tags = ["Points"],
          status_code = status.HTTP_201_CREATED)
def create_point(request: Request,
                 point: schemas.PointCreate,
                 db: Session = Depends(get_db)) -> schemas.Point:
    """
    Create a new point.

    Args:
        request (Request): The request object containing information about the request.
        point (schemas.PointCreate): The payload data to create a new point.
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Raises:
        HTTPException (HTTP_409_CONFLICT): Error raised if there's already a stored point with that name. 

    Returns:
        _type_: The created point.
    """
    auth.verify_access(request)
    if crud.get_point_by_name(db, name = point.name):
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "POINT ALREADY REGISTERED")
    return crud.create_point(db = db, new_point = point)

@app.get("/points/v1/access",
         response_description = "Get the access name and drop-off point ID from the access token.",
         response_model = Optional[dict],
         tags = ["Points"],
         status_code = status.HTTP_200_OK)
def get_point_id_of_access(request: Request,
                           db: Session = Depends(get_db)) -> Optional[dict]:
    """
    Get the access name and drop-off point ID from the access token.

    Args:
        request (Request): request object containing information about the request.
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Raises:
        HTTPException (HTTP_204_NO_CONTENT): Error raised if the tokens provided don't associate to any stored access.

    Returns:
        Optional[dict]: A dictionary containing the name and the drop-off point ID of the access.
    """
    auth.verify_access(request)
    (access_name, access_point_id) = crud.get_auth(db = db, request = request)
    if access_name == None or access_point_id == None:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "ACCESS NOT FOUND")
    return {
        "name": access_name,
        "point_id": access_point_id
        }

@app.delete("/points/v1/points/name/{point_name}",
            response_description = "Delete a specific point by its name.",
            response_model = dict,
            tags = ["Points"],
            status_code = status.HTTP_200_OK)
def delete_point(request: Request,
                 point_name: str,
                 db: Session = Depends(get_db)):
    """Delete a specific point by its name.

    Args:
        request (Request): The request object containing information about the request.
        point_name (str): The name attribute of a specify unique point.
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Raises:
        HTTPException (HTTP_204_NO_CONTENT): Error raised if there's no stored point with that name.

    Returns:
        _type_: A dictionary containing a success message.
    """
    auth.verify_access(request)
    if crud.delete_point(db, point_name) == None:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "POINT NOT FOUND")
    return {"message": "POINT DELETED"}

if __name__  == '__main__':
    run(app, host = '0.0.0.0', port = 8000)