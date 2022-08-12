from urllib import response
from app import oauth2
from app.oauth2 import get_current_user
from .. import models, schemas , oauth2
from fastapi import Body, FastAPI, Response , status , HTTPException, Depends, APIRouter
from ..database import engine, SessionLocal , get_db , cursor
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from datetime import date
from sqlalchemy.sql.sqltypes import TIMESTAMP , DATE
router = APIRouter(
    prefix="/reservation",
    tags=["Reservation"]
)

#@router.get("/",response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.ReservationOut])
def get_posts(db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall() 
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Reservation).all()
                                         
    # print(results)
    # print(limit)
    #return {"data":posts}
    return posts

# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_posts": f"title {payLoad['title']} content: {payLoad['content']}"}

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Reservation,db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    print(post)
    cursor.execute("""select count(*) = 0 as allow_booking from "reservation" where (date_in, date_out) overlaps (date %s, date %s) and room_no = %s""",(post.date_in,post.date_out,str(post.room_no)))
    room = cursor.fetchone()
   
    print(room["allow_booking"])
    if(room["allow_booking"] == False):
        print("yo")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    # indate = post.indate.split("-")
    # post.indate = date(int(indate[0]),int(indate[1]),int(indate[2]))
    # outdate = post.outdate.split("-")
    # post.outdate = date(int(outdate[0]),int(outdate[1]),int(outdate[2]))
    # print(post)
    # new_post = models.Schedule( **post.dict())

    date_in = post.date_in.split("-")
    post.date_in = date(int(date_in[0]),int(date_in[1]),int(date_in[2]))
    date_out = post.date_out.split("-")
    post.date_out = date(int(date_out[0]),int(date_out[1]),int(date_out[2]))
    print(post)
    new_post = models.Reservation(owner_id= current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #return {"data" : new_post}
    return new_post

#@router.get("/{id}",response_model=schemas.Post)
@router.get("/{id}",response_model=schemas.ReservationOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = (%s)""", (str(id)))
    # post = cursor.fetchone()
    # post = find_post(id)
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Reservation).filter(models.Reservation.id == id).first()
    #print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    #return {"post_detail": post}

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # deleting post
    #find the index in the array that has required id
    # my_post.pop(index)
    #index = find_index_post(id)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Reservation).filter(models.Reservation.id == id)
    if post.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Reservation with id: {id} does not exists")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    #my_posts.pop(index)
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.ReservationOut)
def update_post(id: int, post: schemas.Reservation, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # index = find_index_post(id)
    # if index== None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} does not exists")

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                 (post.title, post.content, post.published,str(id)))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                            detail=f"post with id: {id} does not exist")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    date_in = post.date_in.split("-")
    post.date_in = date(int(date_in[0]),int(date_in[1]),int(date_in[2]))
    date_out = post.date_out.split("-")
    post.date_out = date(int(date_out[0]),int(date_out[1]),int(date_out[2]))
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    #return {"data": post_query.first()}
    return post_query.first()
