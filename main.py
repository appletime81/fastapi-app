from db import db
from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse


app = FastAPI()
from basemodel import BookItem


# include image folder, style folder
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
