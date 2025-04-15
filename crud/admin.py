from fastapi import APIRouter, HTTPException
import sqlite3
from schemas.admin import Admin

router = APIRouter()

DATABASE = "database/app-db.sqlite"


@router.get("/admins/")
def get_admins(page: int = 1, limit: int = 10, search: str = None):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    offset = (page - 1) * limit

    if search:
        # Buscar por ID exacto o por nombre que contenga el término
        query = """
            SELECT * FROM admins 
            WHERE id = ? OR username LIKE ? 
            LIMIT ? OFFSET ?
        """
        cursor.execute(query, (search, f"%{search}%", limit, offset))
        rows = cursor.fetchall()

        count_query = """
            SELECT COUNT(*) FROM admins 
            WHERE id = ? OR username LIKE ?
        """
        cursor.execute(count_query, (search, f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM admins LIMIT ? OFFSET ?", (limit, offset))
        rows = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM admins")

    total_records = cursor.fetchone()[0]
    conn.close()

    total_pages = (total_records + limit - 1) // limit

    admins = [dict(row) for row in rows]

    return {
        "message": "Adminds successfully obtained",
        "data": admins,
        "page": page,
        "limit": limit,
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
