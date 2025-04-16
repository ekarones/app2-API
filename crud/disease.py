from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import sqlite3
import uuid
from pathlib import Path
import shutil
from schemas.disease import Disease

router = APIRouter()

DATABASE = "database/app-db.sqlite"
IMAGES_DISEASES_DIR = Path("private/diseases")


@router.get("/diseases/")
def get_diseases(page: int = 1, limit: int = 10, search: str = None):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    offset = (page - 1) * limit

    if search:
        # Buscar por ID exacto o por nombre que contenga el término
        query = """
            SELECT * FROM diseases 
            WHERE id = ? OR name LIKE ? 
            LIMIT ? OFFSET ?
        """
        cursor.execute(query, (search, f"%{search}%", limit, offset))
        rows = cursor.fetchall()

        count_query = """
            SELECT COUNT(*) FROM diseases 
            WHERE id = ? OR name LIKE ?
        """
        cursor.execute(count_query, (search, f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM diseases LIMIT ? OFFSET ?", (limit, offset))
        rows = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM diseases")

    total_records = cursor.fetchone()[0]
    conn.close()

    total_pages = (total_records + limit - 1) // limit

    diseases = [dict(row) for row in rows]

    return {
        "message": "Adminds successfully obtained",
        "data": diseases,
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
    }


@router.post("/diseases/")
def create_disease(
    name: str = Form(...), description: str = Form(...), image: UploadFile = File(...)
):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    image_name = f"{uuid.uuid4()}.jpg"
    image_path = IMAGES_DISEASES_DIR / image_name
    with image_path.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    cursor.execute(
        "INSERT INTO diseases (name, description, image_name) VALUES (?, ?, ?)",
        (name, description, image_name),
    )
    conn.commit()
    conn.close()
    return {
        "message": "Disease created successfully",
        "data": {"name": name, "description": description, "image_name": image_name},
    }


@router.put("/diseases/{disease_id}")
def update_disease(
    disease_id: int,
    name: str = Form(...),
    description: str = Form(...),
    image: UploadFile | None = File(None),  # La imagen es opcional
):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Verificar si la enfermedad existe
    cursor.execute("SELECT image_name FROM diseases WHERE id = ?", (disease_id,))
    disease = cursor.fetchone()
    if not disease:
        conn.close()
        raise HTTPException(status_code=404, detail="Disease not found")
    old_name_image = disease[0]  # Imagen anterior
    new_name_image = old_name_image  # Mantener por defecto la imagen anterior
    if image:
        # Si se sube una nueva imagen, generar un nuevo nombre
        new_name_image = f"{uuid.uuid4()}.jpg"
        new_image_path = IMAGES_DISEASES_DIR / new_name_image
        # Guardar la nueva imagen
        with new_image_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        # Eliminar la imagen anterior si existe
        old_image_path = IMAGES_DISEASES_DIR / old_name_image
        if old_image_path.exists():
            old_image_path.unlink()
    # Actualizar la enfermedad en la base de datos
    cursor.execute(
        "UPDATE diseases SET name = ?, description = ?, image_name = ? WHERE id = ?",
        (name, description, new_name_image, disease_id),
    )
    conn.commit()
    conn.close()
    return {
        "message": "Disease updated successfully",
        "data": {
            "id": disease_id,
            "name": name,
            "description": description,
            "image_name": new_name_image,
        },
    }


@router.delete("/diseases/{disease_id}")
def delete_disease(disease_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Verificar si la enfermedad existe y obtener la imagen
    cursor.execute("SELECT image_name FROM diseases WHERE id = ?", (disease_id,))
    disease = cursor.fetchone()
    if not disease:
        conn.close()
        raise HTTPException(status_code=404, detail="Disease not found")
    image_name = disease[0]
    image_path = IMAGES_DISEASES_DIR / image_name
    # Eliminar la enfermedad de la base de datos
    cursor.execute("DELETE FROM diseases WHERE id = ?", (disease_id,))
    conn.commit()
    conn.close()
    # Eliminar la imagen del sistema de archivos si existe
    if image_path.exists():
        image_path.unlink()
    return {"message": "Disease deleted successfully", "disease_id": disease_id}
