from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    return db.get(models.Item, item_id)


def list_items(db: Session) -> List[models.Item]:
    statement = select(models.Item).order_by(models.Item.created_at.desc())
    return db.execute(statement).scalars().all()


def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, db_item: models.Item, item_update: schemas.ItemUpdate) -> models.Item:
    update_data = item_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, db_item: models.Item) -> None:
    db.delete(db_item)
    db.commit()
