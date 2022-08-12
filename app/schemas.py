
from pydoc import describe
from sqlite3 import Date
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlalchemy.sql.sqltypes import TIMESTAMP , Date
from pydantic.types import conint
from datetime import date
class PostBase(BaseModel):
    title:  str
    content: str 
    published: bool = True 
    #rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
        
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class Room(BaseModel):
    id: int
    number: int
    name: str
    status: str
    room_type_id: int
class RoomType(BaseModel):
    id: int
    description: str
    max_capacity: int
    class Config:
            orm_mode = True

class RoomOut(Room):
    room_type: RoomType
    class Config:
            orm_mode = True

class Reservation(BaseModel):
    date_in: str
    date_out: str
    room_no: int

class ReservationOut(BaseModel):
    date_in: date
    date_out:date
    room_no:int
    class Config:
        orm_mode = True

class Schedule(BaseModel):
    indate: str
    outdate: str
    room_no: int

class ScheduleOut(Schedule):
    class Config:
        orm_mode = True