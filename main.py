from db import db
from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# import basemodel
from basemodel import BookItem


# include image folder in the project folder
app.mount("/image", StaticFiles(directory="image"), name="image")
app.mount("/style", StaticFiles(directory="style"), name="style")


@app.get("/")
async def index():
    return FileResponse("static/index.html")


@app.get("/books/{book_id}", response_model=BookItem)
async def read_item(book_id: int):
    items = {}
    for item in db.collection("book_items").stream():
        items[item.id] = item.to_dict()
    return items[book_id]


@app.get("/allbooks")
async def read_items():
    items = []
    for item in db.collection("book_items").stream():
        items_dict = {
            "id": item.id,
            "title": item.to_dict()["title"],
            "price": item.to_dict()["price"],
        }
        items.append(
            items_dict
        )
    print(items)
    return items
