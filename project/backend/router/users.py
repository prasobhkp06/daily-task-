from fastapi import APIRouter
from database import cursor, row_to_dict

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users():
    cursor.execute("SELECT id, username, email FROM users ORDER BY id DESC")
    return [row_to_dict(row) for row in cursor.fetchall()]
