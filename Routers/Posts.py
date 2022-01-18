from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from starlette.status import HTTP_204_NO_CONTENT
from database import engine
from sqlalchemy.orm import session
from database import get_db
from schemas import PostCreate
import oAuth2, Model, schemas
from typing import Optional
from sqlalchemy import func
router = APIRouter(prefix="/posts", tags=['Posts'])

Model.Base.metadata.create_all(bind=engine)


# path operation
# Decorator makes it act like an API and turns into an actual path operation
# app=fastApi reference and .get is the method that sends the get method to the API
# ("/") is the root path in the url


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastAPI', user='postgres', password='Brinda104!',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesful")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("The error was: ", error)
#         time.sleep(2)
#
#
# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM POSTS""")
#     posts = cursor.fetchall()
#     return {"data": posts}
#
#
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: PostCreate, db: session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    new_post = Model.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute("""INSERT INTO POSTS (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    return new_post


@router.get("/{id1}", response_model=schemas.PostOut)
# # The id field represents a path parameter
def get_post(id1: int, db: session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    #     cursor.execute("""SELECT * FROM POSTS WHERE ID = %s """, (str(id1)))
    #     post = cursor.fetchone()
    #     if not post:
    #         raise HTTPException(status_code=HTTP_404_NOT_FOUND,
    #                             detail=f"Post with id: {id1} does not exist")
    #
    post = db.query(Model.Post).filter(Model.Post.id == id1).first()
    result = result = db.query(Model.Post, func.count(Model.Vote.post_id).label("votes")).join(Model.Vote, Model.Vote.post_id == Model.Post.id, isouter=True).group_by(
        Model.Post.id).filter(Model.Post.id == id1).first()
    return result


#
#
@router.delete("/{id1}", status_code=HTTP_204_NO_CONTENT)
def delete_post(id1: int, db: session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    #     # deleting a post
    #     cursor.execute("""DELETE FROM POSTS WHERE ID=%s RETURNING *""", (str(id1)))
    #     deleted = cursor.fetchone()
    #     if deleted is None:
    #         raise HTTPException(status_code=HTTP_404_NOT_FOUND,
    #                             detail=f"Post with id: {id1} does not exist")
    #     return {"Deleted Post: ": deleted}
    post_query = db.query(Model.Post).filter(Model.Post.id == id1)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id: {id1} doesnt exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return post


#
#
@router.put("/{id1}")
def update_post(id1: int, updated_post: PostCreate, db: session = Depends(get_db), current_user: int = Depends(
    oAuth2.get_current_user)):
    #     cursor.execute("""UPDATE posts SET
    #                     title = %s, content = %s, published =%s
    #                     WHERE id = %s RETURNING * """,
    #                    (post.title, post.content, post.published, str(id1)))
    #     updated = cursor.fetchone()
    #     conn.commit()
    #     if updated is None:
    #         raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Post with id: {id1} does not exist")
    post_query = db.query(Model.Post).filter(Model.Post.id == id1)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id: {id1} doesnt exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return updated_post


@router.get("/", response_model=List[schemas.PostOut])
def get_all_posts(db: session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user), limit: int = 10,
                  skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(Model.Post).filter(Model.Post.title.contains(search)).limit(limit).offset(skip).all()
    result = db.query(Model.Post, func.count(Model.Vote.post_id).label("votes")).join(
        Model.Vote, Model.Vote.post_id == Model.Post.id, isouter=True).group_by(Model.Post.id).filter(
        Model.Post.title.contains(search)).limit(limit).offset(skip).all()
    return result
