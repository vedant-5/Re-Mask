import time
from typing import Optional, List

from pydantic import BaseModel

class SignUpModel(BaseModel):
    name: str
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

class StatusModel(BaseModel) :
    referenceId: str
    status: str


