from pydantic import BaseModel


class Advice(BaseModel):
    disease_name: str
    description: str
