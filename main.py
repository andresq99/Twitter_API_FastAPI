# Python
from uuid import UUID
from datetime import date
from datetime import datetime
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
    email: EmailStr = Field(..., example="andres@gmail.com")
    pass

class UserLogin(UserBase):
    password: str = Field( # Nunca es bueno responder al cliente de la API con la contraseña
        ..., 
        min_length=8,
        max_length=64
    )

class User(UserBase): 
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Andres"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Quelal"
    )
    birth_date: Optional[date] = Field(default=None)
    

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)  
    content : str = Field(
        ...,
        min_length=1,
        max_length=256,
        example="Hello World"
    )
    created_at: datetime = Field(default=datetime.now())  
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...) # Relacion de uno a muchos



# Path operations

@app.get(path="/")
def home():
    return {"Twitter API": "Working"}

