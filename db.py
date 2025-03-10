import sqlite3
import os
import shutil

if not os.path.exists("private/records"):
    os.makedirs("private/records")
else:
    for filename in os.listdir("private/records"):
        file_path = os.path.join("private/recors", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

if not os.path.exists("private/diseases"):
    os.makedirs("private/diseases")
else:
    for filename in os.listdir("private/diseases"):
        file_path = os.path.join("private/diseases", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

default_diseases_path = "default_diseases"
assets_diseases_path = "private/diseases"

for filename in os.listdir(default_diseases_path):
    file_path = os.path.join(default_diseases_path, filename)
    if os.path.isfile(file_path):
        shutil.copy(file_path, assets_diseases_path)

if not os.path.exists("database"):
    os.makedirs("database")

conn = sqlite3.connect("database/app-db.sqlite")
conn.text_factory = str  # Asegurar que maneje bien las cadenas
cursor = conn.cursor()
with open("schema.sql", "r", encoding="utf-8") as file:
    schema = file.read()
cursor.executescript(schema)
conn.commit()
conn.close()
print("Database created successfully!")
