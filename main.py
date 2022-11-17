from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime
import model
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Union
import uvicorn


model.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


paulook = FastAPI()


class Posts(BaseModel):
    likes: int = Field(gt=-1)
    title_post: str = Field(min_length=1, max_length=100)
    user_id: int = Field(gt=-1)
    description: str = Field(min_length=1, max_length=140)
    creation_date: Union[datetime, None] = None


class Users(BaseModel):
    user_name: str = Field(min_length=1, max_length=100)
    user_age: int = Field(gt=-1)
    career: str = Field(min_length=1, max_length=100)
    rol_id: int = Field(gt=-1)
    semester: int = Field(gt=0, lt=15)
    friends_list: str = Field(min_length=1, max_length=100)


@paulook.put("/posts")
def create_post(post: Posts, db: Session = Depends(get_db)):
    post_model = model.Post()
    post_model.title_post = post.title_post
    post_model.likes = post.likes
    post_model.user_id = post.user_id
    post_model.description = post.description
    post_model.creation_date = post.creation_date

    db.add(post_model)
    db.commit()
    return {"Description": "Post Creado satisfactoriamente"}


@paulook.put("/users")
def create_user(user: Users, db: Session = Depends(get_db)):
    user_model = model.User()
    user_model.user_name = user.user_name
    user_model.user_age = user.user_age
    user_model.career = user.career
    user_model.rol_id = user.rol_id
    user_model.semester = user.semester
    user_model.friends_list = user.friends_list
    db.add(user_model)
    db.commit()
    return {"Description": "Usuario creado satisfactoriamente"}


@paulook.post("/users/{user_id}")
def update_user(user_id: int, user: Users, db: Session = Depends(get_db)):
    user_model = db.query(model.User).filter(model.User.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    user_model.user_name = user.user_name
    user_model.user_age = user.user_age
    user_model.career = user.career
    user_model.rol_id = user.rol_id
    user_model.semester = user.semester
    user_model.friends_list = user.friends_list
    db.add(user_model)
    db.commit()
    return {"Description": f"Usuario con ID {user_id} modificado correctamente"}


@paulook.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(model.User).filter(model.User.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )
    return user_model


if __name__ == "__main__":
    uvicorn.run("main:paulook", host="0.0.0.0", port=5000, log_level="info", reload=True)
