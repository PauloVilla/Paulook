from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime
from typing import Union
import uvicorn

paulook = FastAPI()


class Posts(BaseModel):
    n_likes: int
    description: str
    user_id: int
    creation_date: Union[datetime, None] = None
    post_id: int
    title_post: str


posts_dict = {}


class Users(BaseModel):
    user_name: str
    user_id: int
    user_age: int
    career: Union[str, None] = None
    semester: Union[str, None] = None
    rol: str
    rol_id: int
    friends_list: list[int]


users_dict = {}


@paulook.put("/posts")
def create_post(post: Posts):
    post = dict(post)
    posts_dict[post["post_id"]] = post
    return {"Description": f"Post Creado satisfactoriamente, post_id = {post['post_id']}"}


@paulook.put("/users")
def create_user(user: Users):
    user = dict(user)
    users_dict[user["user_id"]] = user
    return {"Description": f"Usuario creado satisfactoriamente, user_id = {user['user_id']}, rol = {user['rol']}"}


@paulook.post("/users/{user_id}/{friend_id}")
def update_user(user_id: int, friend_id: int):
    user_to_update = users_dict[user_id]
    list_to_update = user_to_update["friends_list"]
    list_to_update.append(friend_id)
    users_dict[user_id]["friends_list"] = list_to_update
    return {"Description": f"Usuario {friend_id} agregado a la lista de amigos de {user_id}"}


@paulook.get("/users/{user_id}/friends")
def get_friends_list(user_id: int):
    friends_list = users_dict[user_id]["friends_list"]
    return {user_id: friends_list}


if __name__ == "__main__":
    uvicorn.run("main:paulook", host="0.0.0.0", port=5000, log_level="info", reload=True)
