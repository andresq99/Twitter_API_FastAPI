# Python
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic.networks import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from fastapi import Form
from fastapi import HTTPException
from fastapi import Path

app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_lenght=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_lenght=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content:str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

class LoginOut(BaseModel): 
    email: EmailStr = Field(...)
    message: str = Field(default="Login Successfully!")

# Aditional functions

def read_data(file):
    with open(f"{file}.json", "r+", encoding="utf-8") as f:
        return json.loads(f.read()) # Convertirlo al simil de json

def overwrite_data(file, result):
    with open(f"{file}.json", "w", encoding="utf-8") as f:
        f.seek(0) # Moverte al inicio del archivo
        f.write(json.dumps(result)) # Convirtiendo de una list_dic a un json

def show_data(file, id, info):
    results = read_data(file)
    id = str(id)
    for data in results:
        if data[f"{info}_id"] == id:
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡This {info} doesn't exist!"
        )

def delete_data(file, id, info):
    results = read_data(file)
    id = str(id)
    for data in results:
        if data[f"{info}_id"] == id:
            results.remove(data)
            overwrite_data(file, results)
            return data
    else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"¡This {info} doesn't exist!"
            )


# Path Operations

## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path operations register a user in the app

    Parameters:
    - Request body parameter
        - user: UserRegister

    Return a json with the basic user information:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user


### Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login(
    email: EmailStr = Form(...),
    password: str = Form(...)
):
    """
    Login

    This path operations login a user in the app

    Parameters:
        - Request body parameter
            - user: UserLogin
                - email: Emailstr
                - password: str
    
    Return a json with the basic user information:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime

    """
    data = read_data("users")
    for user in data:
        if email == user["email"] and password == user["password"] :
            return LoginOut(email=email)
        else:
            LoginOut(email=email, message="Login Unsuccessfully!")

### Show all user
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    This path operation shows all users in the app

    Parameters:
    -

    Returns a json list with all users in the app, with the following keys:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="show a User",
    tags=["Users"]
)
def show_a_user(user_id: UUID = Path(
    ...,
    title="The ID of the user to get",
    description="The ID of the user to get",
)):
    """
    This path operation show a user in the app

    ### Parameters
    - Request body parameter: 
        - **user_id: UUID**
 
    ### Returns a json with the a user in the app, with the following keys:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: datetime        
    
    """
    results = read_data("users")
    for data in results:
        if data["user_id"] == str(user_id):
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This user id doesn't exist!"
        )


### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user(user_id: UUID = Path(
    ...,
    title="User ID",
    description="The ID of the user to delete",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    )):
    """
    Delete a User

    This path operation delete a user in the app

    Parameters:
        - user_id: UUID

    Returns a json with deleted user data:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    results = read_data("users")
    id = str(user_id)
    for data in results:
        if data["user_id"] == id:
            results.remove(data)
            with open("users.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return data
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="¡This user id doesn't exist!"
            )

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user(user_id: UUID = Path(
    ...,
    title="User ID",
    description="The ID of the user to update",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    ),
    user: User = Body(...)
):
    """
    Update User

    This path operation update a user information in the app and save in the database

    Parameters:
    - user_id: UUID
    - Request body parameter:
        - **user: User** -> A user model with user_id, email, first name, last name, birth date and password
    
    Returns a user model with user_id, email, first_name, last_name and birth_date
    
    """
    user_dict = user.dict()
    id = str(user_id)
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])
    results = read_data("users")
    for user in results:
        if user["user_id"] == id:
            results[results.index(user)] = user_dict
            with open("users.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="¡This user id doesn't exist!"
            )

## Tweets

### Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
def home():
    """
    This path operation shows all tweets in the app

    Parameters:
    -

    Returns a json list with all tweets in the app, with the following keys:
    - tweet_id: UUID
    - content:str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results


### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    Post a Tweet

    This path operations post a tweet in the app

    Parameters:
    - Request body parameter
        - tweet: Tweet

    Return a json with the basic tweet information:
    - tweet_id: UUID
    - content:str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        if tweet_dict["updated_at"] is not None:
            tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet


### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet(tweet_id: UUID = Path(
    ...,
    title="Tweet ID",
    description="The ID of the tweet to show",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    )
):
    """
    Show a Tweet

    This path operation show if a tweet exist in the app

    Parameters:
        - tweet_id: UUID

    Returns a json with tweet data:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    result = read_data("tweets")
    id = str(tweet_id)
    for tweet in result:
        if tweet["tweet_id"] == id:
            return tweet
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="¡This tweet id doesn't exist!"
            )

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet(tweet_id: UUID = Path(
    ...,
    title="Tweet ID",
    description="The ID of the tweet to delete",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    )
):
    """
    Delete a Tweet

    This path operation delete a tweet in the app

    Parameters:
        - tweet_id: UUID

    Returns a json with deleted tweet data:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    results = read_data("tweets")
    id = str(tweet_id)
    for data in results:
        if data["tweet_id"] == id:
            results.remove(data)
            with open("tweets.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
                return data
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="¡This tweet id doesn't exist!"
            )

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet(tweet_id: UUID = Path(
    ...,
    title="Tweet ID",
    description="The ID of the tweet to update",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    ),
    content: str = Form(
        ...,
        max_length=256,
        title="Tweet content",
        description="This is the content of the tweet",
    )
):
    """
    Update Tweet

    This path operation update a tweet information in the app and save in the database

    Parameters:
    - tweet_id: UUID
    - contet:str
    
    Returns a json with:
        - tweet_id: UUID
        - content: str 
        - created_at: datetime 
        - updated_at: datetime
        - by: user: User
    """
    tweet_id = str(tweet_id)
    results = read_data("tweets")
    for tweet in results:
        if tweet["tweet_id"] == tweet_id:
            tweet["content"] = content
            tweet["updated_at"] = str(datetime.now())
            with open("tweets.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
                return tweet
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This tweet_id doesn't exist!"
        )