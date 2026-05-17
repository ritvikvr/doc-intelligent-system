from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import hashlib
import hmac
import json
import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = "supersecretchangeme"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
USERS_FILE = DATA_DIR / "users.json"

PBKDF2_ITERATIONS = 120_000
SALT_BYTES = 16


class AuthRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str


class StoredUser(BaseModel):
    id: int
    username: str
    hashed_password: str


def _load_users() -> list[StoredUser]:
    if not USERS_FILE.exists():
        return []
    try:
        raw = json.loads(USERS_FILE.read_text())
        return [StoredUser(**item) for item in raw]
    except Exception:
        return []


def _save_users(users: list[StoredUser]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text(json.dumps([u.model_dump() for u in users], indent=2))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt_hex, digest_hex = hashed_password.split("$", 1)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
    except Exception:
        return False

    derived = hashlib.pbkdf2_hmac(
        "sha256",
        plain_password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return hmac.compare_digest(derived, expected)


def get_password_hash(password: str) -> str:
    salt = os.urandom(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return f"{salt.hex()}${digest.hex()}"


def get_user_by_username(username: str) -> Optional[StoredUser]:
    users = _load_users()
    for user in users:
        if user.username == username:
            return user
    return None


def authenticate_user(username: str, password: str) -> Optional[StoredUser]:
    user = get_user_by_username(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception

    return UserResponse(id=user.id, username=user.username)


@router.post("/auth/register", response_model=UserResponse)
def register(auth: AuthRequest):
    users = _load_users()
    existing = next((u for u in users if u.username == auth.username), None)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    next_id = max((u.id for u in users), default=0) + 1
    user = StoredUser(
        id=next_id,
        username=auth.username,
        hashed_password=get_password_hash(auth.password),
    )
    users.append(user)
    _save_users(users)
    return UserResponse(id=user.id, username=user.username)


@router.post("/auth/login", response_model=TokenResponse)
def login(auth: AuthRequest):
    user = authenticate_user(auth.username, auth.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.get("/auth/me", response_model=UserResponse)
def read_current_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user
