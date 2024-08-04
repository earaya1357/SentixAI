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
    username: str = Field(..., min_length=5, pattern=r'[0-9]')
    password: str = Field(..., min_length=8, pattern=r'[!@#%&]')
    repassword: str = Field(..., min_length=8, pattern=r'[!@#%&]')
    firstname: str
    lastname: str
    email: EmailStr
    age: int = Field(..., ge=18)
    company: str


    #@field_validator('password','repassword')
    #@classmethod
    def checkpassword(password, repassword)->None|str:
        if password != repassword:
            raise ValueError('Password does not match')
    
    #@field_validator('username','firstname', 'lastname', 'email', 'age', 'company')
    #@classmethod
    def fieldscomplete(username,firstname, lastname, email, age, company)->None|str:
        if not username and firstname and lastname and email and age and company:
            raise ValueError('Not all fields are complete')


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


