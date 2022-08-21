from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

app = FastAPI()

# include image folder in the project folder
img_folder = './images'
app.mount('/image', StaticFiles(directory="image"), name='image')


@app.get("/")
async def index():
    return FileResponse("static/index.html")


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
