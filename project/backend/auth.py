from fastapi import APIRouter, HTTPException, status
from database import conn, cursor, row_to_dict
from schemas import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=409, detail="Username already exists")

    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (user.username, user.email, user.password),
    )
    conn.commit()
    return {"message": "User registered successfully", "username": user.username}


@router.post("/login")
def login(data: UserLogin):
    cursor.execute(
        "SELECT id, username, email FROM users WHERE username = ? AND password = ?",
        (data.username, data.password),
    )
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "message": "Login successful",
        "user": row_to_dict(user),
    }
