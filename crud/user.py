from fastapi import APIRouter, HTTPException
import sqlite3
from schemas.user import User

router = APIRouter()

DATABASE = "database/app-db.sqlite"


@router.get("/users/")
def get_users(page: int = 1, per_page: int = 10):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    offset = (page - 1) * per_page
    cursor.execute("SELECT * FROM users LIMIT ? OFFSET ?", (per_page, offset))
    users = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_records = cursor.fetchone()[0]
    conn.close()
    total_pages = (total_records + per_page - 1) // per_page
    return {
        "message": "Users successfully obtained",
        "data": users,
        "page": page,
        "per_page": per_page,
        "total_records": total_records,
        "total_pages": total_pages,
    }


@router.get("/users/{user_id}")
def get_user_by_id(user_id: int = 1):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User successfully obtained", "data": user}


@router.post("/users/")
def create_user(user: User):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", (user.email,))
    email_exists = cursor.fetchone()[0] > 0
    if email_exists:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")
    # Insertar el nuevo usuario
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (user.username, user.email, user.password),
    )
    conn.commit()
    conn.close()
    return {"message": "User created successfully", "data": user.dict()}


@router.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Verificar si el nuevo email ya existe en otro usuario
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE email = ? AND id != ?", (user.email, user_id)
    )
    email_exists = cursor.fetchone()[0] > 0
    if email_exists:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")
    # Actualizar los datos del usuario
    cursor.execute(
        "UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?",
        (user.username, user.email, user.password, user_id),
    )
    # Verificar si se realizó alguna actualización
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    conn.commit()
    conn.close()
    return {"message": "User updated successfully", "data": user.dict()}


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"message": "User deleted successfully"}
