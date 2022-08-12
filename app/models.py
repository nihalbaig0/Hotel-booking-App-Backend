from enum import unique
from sqlalchemy import Column , Integer , String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP , DATE , Date
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    owner = relationship("User")

    

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"), primary_key=True)



# select count(*) = 0 as allow_booking
# from "users"
# where (indate, outdate) overlaps (date '2021-11-05', date '2022-06-02');

# select count(*) = 0 as allow_booking
# from "schedule"
# where (indate, outdate) overlaps (date '2021-02-05', date '2021-06-06') and room_no=1;

class Guest(Base):
    __tablename__ = "guest"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)




class Room_Type(Base):
    __tablename__ = "room_type"

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String, nullable=False)
    max_capacity = Column(Integer, nullable=False)

class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, nullable=False)
    number = Column(String, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_type.id",ondelete="CASCADE"))
    room_type = relationship("Room_Type")

class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, nullable=False)
    date_in = Column(Date, nullable=False)
    date_out = Column(Date, nullable=False)
    room_no = Column(Integer,ForeignKey("room.id",ondelete="CASCADE"),nullable=False)
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    
class Reserved_Rooms(Base):
    __tablename__ = "reserved_rooms"

    id = Column(Integer, primary_key=True, nullable=False) 
    room_type_id = Column(Integer, ForeignKey("room_type.id",ondelete="CASCADE"))
    reservation_id = Column(Integer, ForeignKey("reservation.id",ondelete="CASCADE"))
    status = Column(String, nullable=False)


class Occupied_Room(Base):
    __tablename__ = "occupied_room"

    id = Column(Integer, primary_key=True, nullable=False)
    check_in = Column(DATE, nullable=False, server_default=text('now()'))
    check_out = Column(DATE, nullable=False, server_default=text('now()'))
    room_id = Column(Integer, ForeignKey("room.id",ondelete="CASCADE"))
    reservation_id = Column(Integer, ForeignKey("reservation.id",ondelete="CASCADE"))

class Hosted_At(Base):
    __tablename__ = "hosted_at"

    id = Column(Integer, primary_key=True, nullable=False)  
    guest_id = Column(Integer, ForeignKey("guest.id",ondelete="CASCADE"))
    occupied_room_id = Column(Integer, ForeignKey("occupied_room.id",ondelete="CASCADE"))



class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, nullable=False)
    room_no = Column(Integer,ForeignKey("room.id",ondelete="CASCADE"),nullable=False)
    indate = Column(Date, nullable=False)
    outdate = Column(Date, nullable=False)

