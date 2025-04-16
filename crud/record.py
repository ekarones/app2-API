from fastapi import APIRouter
import sqlite3

router = APIRouter()

DATABASE = "database/app-db.sqlite"


@router.get("/records/")
def get_records(page: int = 1, limit: int = 10, search: str = None):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    offset = (page - 1) * limit

    if search:
        # Buscar por ID exacto o por nombre que contenga el término
        query = """
            SELECT * FROM records 
            WHERE id = ? OR user_id = ?
            LIMIT ? OFFSET ?
        """
        cursor.execute(query, (search, search, limit, offset))
        rows = cursor.fetchall()

        count_query = """
            SELECT COUNT(*) FROM records 
            WHERE id = ? OR user_id = ?
        """
        cursor.execute(count_query, (search, f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM records LIMIT ? OFFSET ?", (limit, offset))
        rows = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM records")

    total_records = cursor.fetchone()[0]
    conn.close()

    total_pages = (total_records + limit - 1) // limit

    records = [dict(row) for row in rows]

    return {
        "message": "Records successfully obtained",
        "data": records,
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
    }


@router.get("/records/{record_id}")
def get_record_by_id(record_id: int = 1):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
    record = cursor.fetchone()
    conn.close()
    if record is None:
        return {"message": "Record not found"}
    return {"message": "Record successfully obtained", "data": record}


@router.delete("/records/{record_id}")
def delete_record(record_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    return {"message": "Record deleted successfully"}
