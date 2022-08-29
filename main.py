from db import db
from typing import Union
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from basemodel import BookItem, CreateUser
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI()


def get_password_hash(password: str):
    return bcrypt_context.hash(password)

# include image folder, style folder
app.mount("/image", StaticFiles(directory="image"), name="image")
app.mount("/style", StaticFiles(directory="style"), name="style")


@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.get("/login")
async def login_page():
    return FileResponse("static/login.html")    


@app.get("/books/{book_id}", response_model=BookItem)
async def read_item(book_id: int):
    items = {}
    for item in db.collection("book_items").stream():
        items[item.id] = item.to_dict()
    return items[book_id]


@app.get("/books")
async def read_items():
    items = []
    for item in db.collection("book_items").stream():
        items_dict = {
            "id": item.id,
            "title": item.to_dict()["title"],
            "price": item.to_dict()["price"],
        }
        items.append(items_dict)
    print(items)
    return items


# ---- 會員系統 ----
@app.post("/create/user")
async def create_new_user(create_user: CreateUser, request: Request):
    # get request post content
    data = await request.json()
    print(data)

    # create new user
    user = {
        "username": data["username"],
        "password": data["password"],
        "email": data["email"],
        "first_name": data["first_name"],
        "last_name": data["last_name"],
    }
    db.collection("users").document(data["username"]).set(user)
    return {"message": "success"}
