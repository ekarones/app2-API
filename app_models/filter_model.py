import openai
from openai import OpenAI
import base64

client = OpenAI(
    api_key="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"
)


def analizar_imagen_con_gpt(url_imagen: str) -> str:
    """
    Envía una imagen a GPT para evaluar si contiene una hoja clara de manzano.

    Parámetros:
    - url_imagen (str): URL de la imagen a evaluar.

    Retorna:
    - str: Respuesta generada por el modelo.
    """
    with open(url_imagen, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # Recomendado para entrada con imágenes
        messages=[
            {
                "role": "system",
                "content": "Eres un sistema de clasificación binaria de imágenes. Tu tarea es identificar si hay una hoja de árbol visible en la imagen.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Observa la imagen y responde únicamente con uno de estos dos números:\n"
                            "- 1: si hay una hoja clara y visible en la imagen\n"
                            "- 0: si no hay una hoja visible en la imagen\n"
                            "No agregues ningún otro texto. Solo responde con '1' o '0'."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                    },
                ],
            },
        ],
        max_tokens=10,
    )
    return response.choices[0].message.content
