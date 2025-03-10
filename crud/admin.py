from fastapi import APIRouter, HTTPException
import sqlite3
from schemas.admin import Admin

router = APIRouter()

DATABASE = "database/app-db.sqlite"


@router.get("/admins/")
def get_admins(page: int = 1, per_page: int = 10):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    offset = (page - 1) * per_page
    cursor.execute("SELECT * FROM admins LIMIT ? OFFSET ?", (per_page, offset))
    admins = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM admins")
    total_records = cursor.fetchone()[0]
    conn.close()
    total_pages = (total_records + per_page - 1) // per_page
    return {
        "message": "Admins successfully obtained",
        "data": admins,
        "page": page,
        "per_page": per_page,
        "total_records": total_records,
        "total_pages": total_pages,
    }


@router.get("/admins/{admin_id}")
def get_admin_by_id(admin_id: int = 1):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE id = ?", (admin_id,))
    admin = cursor.fetchone()
    conn.close()
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"message": "Admin successfully obtained", "data": admin}


@router.post("/admins/")
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


@router.put("/admins/{admin_id}")
def update_admin(admin_id: int, admin: Admin):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Verificar si el nuevo email ya existe en otro usuario
    cursor.execute(
        "SELECT COUNT(*) FROM admins WHERE email = ? AND id != ?",
        (admin.email, admin_id),
    )
    email_exists = cursor.fetchone()[0] > 0
    if email_exists:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")
    # Actualizar los datos del usuario
    cursor.execute(
        "UPDATE admins SET username = ?, email = ?, password = ? WHERE id = ?",
        (admin.username, admin.email, admin.password, admin_id),
    )
    # Verificar si se realizó alguna actualización
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Admin not found")
    conn.commit()
    conn.close()
    return {"message": "Admin updated successfully", "data": admin.dict()}


@router.delete("/admins/{admin_id}")
def delete_admin(admin_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admins WHERE id = ?", (admin_id,))
    conn.commit()
    conn.close()
    return {"message": "Admin deleted successfully"}
