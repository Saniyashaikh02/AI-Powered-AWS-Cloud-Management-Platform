from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.database import users_collection
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


class User(BaseModel):
    username: str
    password: str


# 🔐 REGISTER
@router.post("/register")
def register(user: User):
    existing = users_collection.find_one({"username": user.username})

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = pwd_context.hash(user.password)

    users_collection.insert_one({
        "username": user.username,
        "password": hashed
    })

    return {"message": "User created"}


# 🔐 LOGIN
@router.post("/login")
def login(user: User):
    db_user = users_collection.find_one({"username": user.username})

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid user")

    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Wrong password")

    payload = {
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token}


# 🔒 VERIFY TOKEN (IMPORTANT)
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")