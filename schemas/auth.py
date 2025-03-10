from pydantic import BaseModel, EmailStr, Field


class Credentials(BaseModel):
    email: EmailStr = Field(..., example="johndoe@example.com")
    password: str = Field(..., min_length=6, example="securepassword")
