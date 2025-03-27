from fastapi import APIRouter
import sqlite3
from schemas.notification import Notification

router = APIRouter()

DATABASE = "database/app-db.sqlite"

@router.get('/get-all-notifications/')
def get_all_notifications():
    conn=sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications")
    notifications = cursor.fetchall()
    conn.close() 
    return {"success": True, "data": notifications}

@router.get("/notifications/")
def get_notifications(page: int = 1, per_page: int = 10):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    offset = (page - 1) * per_page
    cursor.execute("SELECT * FROM notifications LIMIT ? OFFSET ?", (per_page, offset))
    notifications = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM notifications")
    total_records = cursor.fetchone()[0]
    conn.close()
    total_pages = (total_records + per_page - 1) // per_page
    return {
        "message": "Notifications successfully obtained",
        "data": notifications,
        "page": page,
        "per_page": per_page,
        "total_records": total_records,
        "total_pages": total_pages,
    }


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
