# Python
from uuid import UUID
from datetime import date
from typing import Optional

# pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI

app = FastAPI()

# Models

class UserBase(BaseModel): # Tiene la informacion basica de un usuario
    user_id: UUID = Field(...) 
    email: EmailStr = Field(...)
    pass

class UserLogin(UserBase):
    password: str = Field( # Nunca es bueno responder al cliente de la API con la contraseña
        ..., 
        min_length=8
    )

class User(UserBase): 
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)
    

class Tweet(BaseModel):
    pass    



# Path operations

@app.get(path="/")
def home():
    return {"Twitter API": "Working"}

