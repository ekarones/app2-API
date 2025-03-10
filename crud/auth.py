from fastapi import APIRouter, HTTPException
import sqlite3
from schemas.auth import Credentials
from schemas.user import User
from schemas.admin import Admin


router = APIRouter()

DATABASE = "database/app-db.sqlite"


@router.post("/login/")
def user_login(credentials: Credentials):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE email = ? AND password = ?",
        (credentials.email, credentials.password),
    )
    user_id = cursor.fetchone()
    conn.close()
    if user_id:
        return {"message": "Login successful", "user_id": user_id[0]}
    else:
        return {"message": "Invalid credentials"}


@router.post("/register/")
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


@router.post("/admin-login/")
def admin_login(credentials: Credentials):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM admins WHERE email = ? AND password = ?",
        (credentials.email, credentials.password),
    )
    admin_id = cursor.fetchone()
    conn.close()
    if admin_id:
        return {"message": "Login successful", "admin_id": admin_id[0]}
    else:
        return {"message": "Invalid credentials"}


@router.post("/admin-register/")
def create_admin(admin: Admin):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM admins WHERE email = ?", (admin.email,))
    email_exists = cursor.fetchone()[0] > 0
    if email_exists:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")
    # Insertar el nuevo usuario
    cursor.execute(
        "INSERT INTO admins (username, email, password) VALUES (?, ?, ?)",
        (admin.username, admin.email, admin.password),
    )
    conn.commit()
    conn.close()
    return {"message": "Admin created successfully", "data": admin.dict()}
