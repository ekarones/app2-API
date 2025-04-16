from fastapi import APIRouter
import sqlite3
from schemas.advice import Advice

router = APIRouter()

DATABASE = "database/app-db.sqlite"


@router.get("/advices/")
def get_advices(page: int = 1, limit: int = 10, search: str = None):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    offset = (page - 1) * limit

    if search:
        # Buscar por ID exacto o por nombre que contenga el término
        query = """
            SELECT * FROM advices 
            WHERE id = ? OR disease_name LIKE ? 
            LIMIT ? OFFSET ?
        """
        cursor.execute(query, (search, f"%{search}%", limit, offset))
        rows = cursor.fetchall()

        count_query = """
            SELECT COUNT(*) FROM advices 
            WHERE id = ? OR disease_name LIKE ?
        """
        cursor.execute(count_query, (search, f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM advices LIMIT ? OFFSET ?", (limit, offset))
        rows = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM advices")

    total_records = cursor.fetchone()[0]
    conn.close()

    total_pages = (total_records + limit - 1) // limit

    advices = [dict(row) for row in rows]

    return {
        "message": "Advices successfully obtained",
        "data": advices,
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
    }


@router.post("/advices/")
def create_advice(advice: Advice):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO advices (disease_name, description) VALUES (?, ?)",
        (advice.disease_name, advice.description),
    )
    conn.commit()
    conn.close()
    return {"message": "Advice created successfully", "data": advice.dict()}


@router.put("/advices/{advice_id}")
def update_advice(advice_id: int, advice: Advice):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE advices SET disease_name = ?, description = ? WHERE id = ?",
        (advice.disease_name, advice.description, advice_id),
    )
    conn.commit()
    conn.close()
    return {"message": "Advice updated successfully", "data": advice.dict()}


@router.delete("/advices/{advice_id}")
def delete_advice(advice_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM advices WHERE id = ?", (advice_id,))
    conn.commit()
    conn.close()
    return {"message": "Advice deleted successfully"}
