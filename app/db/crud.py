from sqlalchemy.orm import Session
from . import models, schemas


def get_data_sets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DataSet).offset(skip).limit(limit).all()


def create_data_set(db: Session, data_set: schemas.DataSetBase) -> models.DataSet:
    db_data_set = models.DataSet(name=data_set.name, organization=data_set.organization, description=data_set.description, link=data_set.link)
    db.add(db_data_set)
    db.commit()
    db.refresh(db_data_set)
    return db_data_set

def create_bulk_data_sets(db: Session, data_sets: list[schemas.DataSetBase]) -> bool:
    
    db.bulk_save_objects(data_sets)
    db.commit()
    
    return True




