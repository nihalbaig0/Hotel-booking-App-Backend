from app import oauth2
from app.oauth2 import get_current_user
from .. import models, schemas , oauth2
from fastapi import Body, FastAPI, Response , status , HTTPException, Depends, APIRouter
from ..database import engine, SessionLocal , get_db , cursor
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.get("/",response_model=List[schemas.RoomOut])
def get_posts(db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    posts = db.query(models.Room).all()
   
    return posts



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.RoomOut)
def create_room(post: schemas.Room,db: Session = Depends(get_db)):

    new_post = models.Room(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = (%s)""", (str(id)))
    # post = cursor.fetchone()
    # post = find_post(id)
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    # post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
    #                                      models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    cursor.execute("""select count(*) = 0 as allow_booking from "schedule"
                where (indate, outdate) overlaps (date '2021-02-05', date '2021-06-06') and room_no=1""")
    room = cursor.fetchone()
    print(room)
    #print(post)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} was not found")

    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {'message': f"post with id: {id} was not found"}
    # #return {"post_detail": post}

    # if post.Post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return {"room_available": room}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Room).filter(models.Room.id == id)
    if post.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"room with id: {id} does not exists")

    #my_posts.pop(index)
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.RoomOut)
def update_post(id: int, post: schemas.Room, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    post_query = db.query(models.Room).filter(models.Room.id == id)
    updated_post = post_query.first()
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                            detail=f"post with id: {id} does not exist")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
