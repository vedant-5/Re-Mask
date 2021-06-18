import time
from typing import Optional, List

from pydantic import BaseModel, EmailStr

class SignUpModel(BaseModel):
    name: str
    referenceId : str
    address: str
    contactNo: str
    telPhone: Optional[str] = None
    emailAddress: str
    password: str
    type: str

class LoginModel(BaseModel):
    emailAddress: str
    password: str

class DonateModel(BaseModel):
    item: str
    timeStart : str
    timeEnd: str
    date: str
    mass: int

class EmailSchema(BaseModel):
    email: List[EmailStr]

class EmailContent(BaseModel):
    message: str
    subject: str