from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app import models, schemas, crud, database

# "Seeds" the database, migrations not handled
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# No Error handling
# No input sanitization or checks

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Create a new user. Use JSON!!! for body.
    """
    return crud.create_user(db, user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve a user by ID.
    Raises 404 if user not found.
    """
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="resource not found")
    return db_user


from fastapi import Query

@app.get("/users/", response_model=list[schemas.User])
def read_users(
    query: str | None = Query(None, description="Filter users by username substring"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(database.get_db)
):
    """
    Return a list of users with pagination.
    OPTIONALS:
    - **query**: filter users by username substring (case-insensitive)
    - **skip**: number of records to skip
    - **limit**: maximum number of records to return
    """
    return crud.get_users(db, query=query, skip=skip, limit=limit)

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Update a user by ID. Use JSON!!! for body - param for id
    Raises 404 if user not found.
    """
    updated_user = crud.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="resource not found")
    return updated_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    """
    Delete a user by ID.
    Raises 404 if user not found.
    """
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="resource not found")
    crud.delete_user(db, user_id)
    return {"ok": True}
