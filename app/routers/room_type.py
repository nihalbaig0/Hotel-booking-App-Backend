from app import oauth2
from app.oauth2 import get_current_user
from .. import models, schemas , oauth2
from fastapi import Body, FastAPI, Response , status , HTTPException, Depends, APIRouter
from ..database import engine, SessionLocal , get_db , cursor
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/room_type",
    tags=["Room_type"]
)


@router.get("/",response_model=List[schemas.RoomType])
def get_posts(db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    posts = db.query(models.Room_Type).all()
   
    return posts



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.RoomType)
def create_room(post: schemas.RoomType,db: Session = Depends(get_db)):

    new_post = models.Room_Type(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model = schemas.RoomType)
def get_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Room_Type).filter(models.Room_Type.id == id).first()
   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"RoomType with id: {id} was not found")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    #return {"post_detail": post}

    # if post.Post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Room_Type).filter(models.Room_Type.id == id)
    if post.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"room with id: {id} does not exists")

    #my_posts.pop(index)
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.RoomType)
def update_post(id: int, post: schemas.RoomType, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    post_query = db.query(models.Room_Type).filter(models.Room_Type.id == id)
    updated_post = post_query.first()
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                            detail=f"Room Type with id: {id} does not exist")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
