from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, query: str | None = None, skip: int = 0, limit: int = 10):
    q = db.query(models.User)
    if query:
        q = q.filter(models.User.username.ilike(f"%{query}%")) # simple filtering on username
    return q.offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email or Username in Use.")  # HTTP 409 Conflict
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db_user.username = user.username
    db_user.email = user.email
    db_user.full_name = user.full_name
    db_user.role = user.role
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email or Username in Use.")  # HTTP 409 Conflict
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
