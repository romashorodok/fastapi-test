from fastapi import Depends, FastAPI, HTTPException
from .container import Container
from . import crud, models, schemas
from .database import engine


models.Base.metadata.create_all(bind=engine)


async def get_container():
    with Container() as di:
        yield di


app = FastAPI()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, di: Container = Depends(get_container)):
    db_user = crud.get_user_by_email(di.db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=di.db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, di: Container = Depends(get_container)):
    users = crud.get_users(di.db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, di: Container = Depends(get_container)):
    db_user = crud.get_user(di.db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, di: Container = Depends(get_container)
):
    return crud.create_user_item(db=di.db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, di: Container = Depends(get_container)):
    items = crud.get_items(di.db, skip=skip, limit=limit)
    return items
