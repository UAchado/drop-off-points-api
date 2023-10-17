from fastapi import FastAPI, Depends
import uvicorn

from sqlalchemy.orm import Session

from database import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/points/", response_model=list[schemas.Point])
def get_all_points(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    points = crud.get_points(db, skip=skip, limit=limit)
    return points

if __name__  == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)