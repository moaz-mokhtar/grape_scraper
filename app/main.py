import json

from app.scraper import DataSet, get_scraped_data
from fastapi import Depends, FastAPI, HTTPException,Response,Request
from .db import crud, models, schemas
from .db.database import SessionLocal, engine

# Initialization
models.Base.metadata.create_all(bind=engine)
app:FastAPI = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Dependency
def get_db(request: Request):
    return request.state.db


@app.get("/")
async def read_root() -> dict:
    return {"Hello": "World"}

@app.get("/scrape/")
async def scrape()-> bool:
    data_list:list[DataSet] = get_scraped_data()
    data_schema:list[schemas.DataSet] = [obj.to_schema() for obj in data_list]
    session = Depends(get_db)
    return crud.create_bulk_data_sets(db=session, data_sets=data_schema)


@app.get("/all/") 
async def get_all()-> list[schemas.DataSet]:
    session = Depends(get_db)
    data_sets:list[models.DataSet] = crud.get_data_sets(db=session)
    return data_sets
