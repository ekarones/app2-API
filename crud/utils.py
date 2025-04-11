from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
import sqlite3

from app_models.filter_model import is_leaf
from app_models.predict_model import predict_img


router = APIRouter()

DATABASE = "database/app-db.sqlite"
IMAGES_RECORDS_DIR = Path("private/records")
IMAGES_DISEASES_DIR = Path("private/diseases")


@router.get("/diseases-names/")
def create_disease():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name FROM diseases",
    )
    diseases_names = cursor.fetchall()
    conn.close()
    return {"message": "success", "data": diseases_names}


@router.post("/upload-image/")
async def upload_image(user_id: str = Form(...), image: UploadFile = File(...)):
    user_id = int(user_id)  # Convertir a entero
    unique_filename = f"{uuid.uuid4()}{Path(image.filename).suffix}"  # Mantiene la extensión original de la imagen
    file_path = IMAGES_RECORDS_DIR / unique_filename
    try:
        with open(file_path, "wb") as f:
            content = await image.read()
            f.write(content)
            # print('{"message": "Imagen guardada exitosamente", "filename": image.filename}')
    except Exception as e:
        return {"message": "Error al guardar la imagen", "error": str(e)}

    if is_leaf(file_path) == False:
        raise HTTPException(status_code=400, detail="Bad image")

    disease_id, disease_name, description, name_image = predict_img(file_path)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO records (user_id, image_path, disease_id, disease_name, diagnosis_date) VALUES (?, ?, ?, ?, DATETIME('now', 'localtime'))",
        (user_id, unique_filename, disease_id, disease_name),
    )
    conn.commit()
    conn.close()

    return {
        "message": "Imagen procesada con éxito",
        "record_image": unique_filename,#imagen enviada por el usuario
        "disease_id": disease_id,
        "disease_name": disease_name,
        "description": description,
        "disease_image": name_image,#imagen guardada de la enfermedad
    }

@router.get("/get-diagnose-by-record/{record_id}")
def get_diagnose_by_record(record_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = """
    SELECT 
        r.image_path,
        r.disease_id,
        r.disease_name,
        d.description,
        d.image_name
    FROM 
        records r
    JOIN 
        diseases d ON r.disease_id = d.id
    WHERE 
        r.id = ?;
    """
    cursor.execute(query, (record_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return {
            "record_image": result[0],
            "disease_id": result[1],
            "disease_name": result[2],
            "description": result[3],
            "disease_image": result[4]
        }
    else:
        return None

@router.get("/get-image-assets/")
def get_image_assets(filename: str):
    folder_path = Path(IMAGES_DISEASES_DIR)
    if not folder_path.exists():
        raise HTTPException(status_code=404, detail="Folder not found")
    image_path = folder_path / filename
    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(str(image_path))


@router.get("/get-image/")
def get_image(filename: str):
    folder_path = Path(IMAGES_RECORDS_DIR)
    if not folder_path.exists():
        raise HTTPException(status_code=404, detail="Folder folder not found")
    image_path = folder_path / filename
    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(str(image_path))


@router.get("/get-advices-by-disease/")
def get_advices_by_disease(disease_name: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM advices WHERE disease_name = ?",
        (disease_name,),
    )
    advices = cursor.fetchall()
    conn.close()
    return {"message": "success", "data": advices} # Retorna [] en caso de que no haya consejos para la enfermedad


@router.get("/get-records-by-user/{user_id}")
def get_records_by_user(user_id: int = 1):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records WHERE user_id = ?", (user_id,))
    records = cursor.fetchall()
    conn.close()
    if records is None:
        return {"message": "Record not found"}

    return {"message": "Records successfully obtained", "data": records}


# DASHBOARD
@router.get("/get-top-users/")
def get_top_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
    SELECT users.id, users.username, COUNT(records.id) AS record_count
    FROM users
    LEFT JOIN records ON users.id = records.user_id
    GROUP BY users.id
    ORDER BY record_count DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return {"message": "success", "data": results}


@router.get("/get-top-diseases/")
def get_top_diseases():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
    SELECT diseases.id, diseases.name, COUNT(records.id) AS diagnosis_count
    FROM diseases
    LEFT JOIN records ON diseases.id = records.disease_id
    GROUP BY diseases.id
    ORDER BY diagnosis_count DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return {"message": "success", "data": results}


@router.get("/get-advices-count/")
def get_advices_count():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
    SELECT diseases.id, diseases.name, COALESCE(COUNT(advices.id), 0) AS advice_count
    FROM diseases
    LEFT JOIN advices ON diseases.name = advices.disease_name
    GROUP BY diseases.name
    ORDER BY advice_count DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return {"message": "success", "data": results}


@router.get("/get-global-count/")
def get_global_count():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
    SELECT 'Usuarios' AS nombre_tabla, COUNT(*) AS cantidad_registros FROM users
    UNION ALL
    SELECT 'Administradores', COUNT(*) FROM admins
    UNION ALL
    SELECT 'Registros', COUNT(*) FROM records
    UNION ALL
    SELECT 'Enfermedades', COUNT(*) FROM diseases
    UNION ALL
    SELECT 'Consejos', COUNT(*) FROM advices
    UNION ALL
    SELECT 'Notificaciones', COUNT(*) FROM notifications;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return {"message": "success", "data": results}
