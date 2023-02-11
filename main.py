# Python
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional
from typing import List

# pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status

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

## Users

### SignUp
@app.post(
    path="/signup",
    response_model = User, # Responde con la informacion del usuario
    status_code=status.HTTP_201_CREATED, # Si el usuario crea correctamente su cuenta
    summary="Register a New User",
    tags=["Users"] 
)
def signup(): # Registrar un usuario
    pass

### Login
@app.post(
    path="/login",
    response_model = User, # Responde con la informacion del usuario
    status_code=status.HTTP_200_OK, # Si el usuario crea correctamente su cuenta
    summary="Login a User",
    tags=["Users"] 
)
def login(): # Registrar un usuario
    pass

### Show all users
@app.get(
    path="/users",
    response_model = List["User"], # Responde un JSON con un formato de lista
    status_code=status.HTTP_200_OK, # Si el usuario crea correctamente su cuenta
    summary="Show all users",
    tags=["Users"] 
)
def show_all_users(): # Registrar un usuario
    pass

### Show an user
@app.get(
    path="/user/{user_id}",
    response_model = User, # Responde con la informacion del usuario
    status_code=status.HTTP_200_OK, # Si el usuario crea correctamente su cuenta
    summary="Show an user",
    tags=["Users"] 
)
def show_an_user(): # Registrar un usuario
    pass

### Delete an user
@app.delete(
    path="/users/{user_id}/delete",
    response_model = User, # Responde con la informacion del usuario
    status_code=status.HTTP_200_OK, # Si el usuario crea correctamente su cuenta
    summary="Delete an user",
    tags=["Users"] 
)
def delete_an_user(): # Registrar un usuario
    pass

### Update an user
@app.put(
    path="/users/{user_id}/update",
    response_model = User, # Responde con la informacion del usuario
    status_code=status.HTTP_200_OK, # Si el usuario crea correctamente su cuenta
    summary="Update an user",
    tags=["Users"] 
)
def update_an_user(): # Registrar un usuario
    pass


## Tweets
