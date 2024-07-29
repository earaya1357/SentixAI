from pydantic import BaseModel, SecretStr, Field, EmailStr, field_validator
import datetime as dt
from pydantic_mongo import AbstractRepository, PydanticObjectId

from typing import Optional

class User(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: EmailStr
    company: str


class NewUser(BaseModel):
    username: str
    password: str
    repassword: str
    firstname: str
    lastname: str
    email: EmailStr
    age: int
    company: str

    def checkpassword(password, repassword):
        if password != repassword:
            return False
        return True
    
    def fieldscomplete(username, password, repassword, firstname, lastname, email, age, company):
        if not username and password and repassword and firstname and lastname and email and age and company:
            return False
        return True


class Part(BaseModel):
    company: str
    partname: str
    description: str


class Sentiment(BaseModel):
    timestamp: dt.datetime
    company: str
    productname: str
    comment: str
    sentiment:str
    strength: int
    vader_score: float
    explanation: str
    tasks: list[str]


