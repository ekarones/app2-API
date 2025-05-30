import os
from dotenv import load_dotenv
from openai import OpenAI
import base64

# Cargar variables del archivo .env
load_dotenv()

# Obtener la clave desde las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def analizar_imagen_con_gpt(url_imagen: str) -> str:
    """
    Envía una imagen a GPT para evaluar si contiene una hoja de manzano clara y sin elementos distractores.

    Parámetros:
    - url_imagen (str): Ruta local de la imagen a evaluar.

    Retorna:
    - str: '1' si la imagen contiene una hoja clara, o '0' si no cumple con los criterios.
    """
    with open(url_imagen, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un sistema de filtrado de imágenes especializado. "
                    "Tu tarea es determinar si la imagen contiene alguna hoja que se vea claramente"
                    "La hoja debe estar bien enfocada"
                    "Ignora imágenes borrosas, demasiado oscuras o donde la hoja no esté claramente distinguible."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analiza la imagen cuidadosamente y responde SOLO con uno de estos dos números:\n"
                            "- 1: si la imagen muestra alguna hoja clara, bien enfocada.\n"
                            "- 0: si la imagen no cumple con los criterios anteriores.\n"
                            "NO agregues ninguna explicación, texto adicional o símbolo. Solo responde con '1' o '0'."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                    },
                ],
            },
        ],
        max_tokens=5,
    )

    return response.choices[0].message.content.strip()
