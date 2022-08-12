from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .routers import post, user , auth, vote, rooms , room_type, reservation
from .config import settings
from app import database


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


origins = [
    "http://localhost:3000",
]

# what is a middleware? 
# software that acts as a bridge between an operating system or database and applications, especially on a network.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






# my_posts = [{"title":"title of post 1","content": "content of post 1","id":1},
#             {"title":"I like pizza","content": "content of post 2","id":2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
    
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(rooms.router)
app.include_router(room_type.router)
app.include_router(reservation.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    post = db.query(models.Post)
    print(post)
    return {"data": "successful"}




