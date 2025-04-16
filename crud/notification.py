from fastapi import APIRouter
import sqlite3
from schemas.notification import Notification

router = APIRouter()

DATABASE = "database/app-db.sqlite"


@router.get("/notifications/")
def get_notifications(page: int = 1, limit: int = 10, search: str = None):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    offset = (page - 1) * limit

    if search:
        # Buscar por ID exacto o por nombre que contenga el término
        query = """
            SELECT * FROM notifications 
            WHERE id = ? OR title LIKE ? 
            LIMIT ? OFFSET ?
        """
        cursor.execute(query, (search, f"%{search}%", limit, offset))
        rows = cursor.fetchall()

        count_query = """
            SELECT COUNT(*) FROM notifications 
            WHERE id = ? OR title LIKE ?
        """
        cursor.execute(count_query, (search, f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM notifications LIMIT ? OFFSET ?", (limit, offset))
        rows = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM notifications")

    total_records = cursor.fetchone()[0]
    conn.close()

    total_pages = (total_records + limit - 1) // limit

    notifications = [dict(row) for row in rows]

    return {
        "message": "Notifications successfully obtained",
        "data": notifications,
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
    }

@router.get('/get-all-notifications/')
def get_all_notifications():
    conn=sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications")
    notifications = cursor.fetchall()
    conn.close() 
    return {"success": True, "data": notifications}


@router.post("/notifications/")
def create_notification(notification: Notification):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notifications (title, description, creation_date) VALUES (?, ?, DATETIME('now', 'localtime'))",
        (notification.title, notification.description),
    )
    conn.commit()
    conn.close()
    return {"message": "Notification created successfully", "data": notification.dict()}

@router.put("/notifications/{notification_id}")
def update_notification(notification_id: int, notification: Notification):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE notifications SET title = ?, description = ? WHERE id = ?",
        (notification.title, notification.description, notification_id),
    )
    conn.commit()
    conn.close()
    return {"message": "Notification updated successfully", "data": notification.dict()}

@router.delete("/notifications/{notificacion_id}")
def delete_notification(notificacion_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notifications WHERE id = ?", (notificacion_id,))
    conn.commit()
    conn.close()
    return {"message": "Notification deleted successfully"}
