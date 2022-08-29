from db import db
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from basemodel import BookItem, CreateUser
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi import FastAPI, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


SECRET_KEY = "BMVvvp4j8Ai7MYfGPwVn9gKazl529yNX"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")

app = FastAPI()


def get_password_hash(password: str):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    # get user from firebase
    user = db.collection("users").document(f"{username}").get()
    # get user value as dict
    user = user.to_dict()

    if not user:
        return False
    if not verify_password(password, user.get("hash_password")):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


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
    # print(items)
    return items


# ---- 會員系統 ----
@app.post("/create/user")
async def create_new_user(create_user: CreateUser, request: Request):
    # get request post content
    data = await request.json()
    # print(data)

    # create new user
    user = {
        "username": data["username"],
        "hash_password": get_password_hash(data["password"]),
        "email": data["email"],
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        # id : count db users
        "id": len(list(db.collection("users").stream())) + 1,
    }
    db.collection("users").document(data["username"]).set(user)
    return {"message": "success"}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        return {"error": "Incorrect username or password"}
    return "User authenticated"
