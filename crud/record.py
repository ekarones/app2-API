from fastapi import APIRouter
import sqlite3

router = APIRouter()

DATABASE = "database/app-db.sqlite"


@router.get("/records/")
def get_records(page: int = 1, per_page: int = 10):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    offset = (page - 1) * per_page
    cursor.execute("SELECT * FROM records LIMIT ? OFFSET ?", (per_page, offset))
    records = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM records")
    total_records = cursor.fetchone()[0]
    conn.close()
    total_pages = (total_records + per_page - 1) // per_page
    return {
        "message": "Records successfully obtained",
        "data": records,
        "page": page,
        "per_page": per_page,
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
