from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

# Ensure the tables exist when the service starts.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", summary="Service health check")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/items", response_model=List[schemas.Item], summary="List all items")
def list_items(db: Session = Depends(get_db)):
    return crud.list_items(db)


@app.post(
    "/items",
    response_model=schemas.Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)


@app.get("/items/{item_id}", response_model=schemas.Item, summary="Retrieve an item by id")
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db_item


@app.put("/items/{item_id}", response_model=schemas.Item, summary="Update an existing item")
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return crud.update_item(db, db_item, item)


@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    crud.delete_item(db, db_item)
