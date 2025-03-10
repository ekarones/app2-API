from pydantic import BaseModel


class Notification(BaseModel):
    title: str
    description: str
