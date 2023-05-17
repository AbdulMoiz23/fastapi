#path operations dealing with Posts

from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from app import oauth2
from .. import models, schemas 
from .. database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
#all posts
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int =Depends
(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # print(limit)
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

    

    #Regular SQL queries
    # cursor.execute("""SELECT * FROM posts """ )
    # posts = cursor.fetchall()
    # return {"data": posts}

#creating posts 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =Depends
(oauth2.get_current_user)):
    ##Regular SQL queries

    # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s)
    # RETURNING * """,
    #                 (post.title, post.content))

    # new_post = cursor.fetchone() 

    # #make a connection to the database
    # conn.commit()

    ##SQL queries thru alchemy ORM
    # print(**post.dict())
    # print(current_user)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
        # title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#getting individual post
#fetch individual post by if

@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int =Depends
(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(
            models.Post.id == id).first()
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} not found")


    # this helps you with getting the post from the database that you logged in from
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                         detail="Not authorized to perform this requested action")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} not found"}
    return post




#Deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int =Depends
(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    #find the index in the array that has the requested ID
    # my_posts.pop(index)

    # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform this requested action")


    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#Update a post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: 
int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING * """,
    #                 (post.title, post.content, str(id)))
    # updated_post = cursor.fetchone() 
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform this requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f"post with id: {id} not found")

    # return {'data': updated_post}