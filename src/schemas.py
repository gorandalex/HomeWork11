from datetime import date

from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date
    description: str


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    description: str

    class Config:
        orm_mode = True
