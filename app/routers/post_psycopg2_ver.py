# ------------------------- Libraries -------------------------
import time
from typing import List

from fastapi import status, HTTPException, Response, APIRouter
import psycopg2
from psycopg2.extras import RealDictCursor

from app import schemas

# ------------------------- Implement Posts with psycopg2 -------------------------
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

db_is_connected = False
while not db_is_connected:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="110963",
            cursor_factory=psycopg2.extras.DictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        db_is_connected = True
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


@router.get('/', response_model=List[schemas.Post])
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    posts_dicts = [
        {column.name: value for column, value in zip(cursor.description, post)}
        for post in posts
    ]
    return posts_dicts


@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    post_dict = {column.name: value for column, value in zip(cursor.description, post)}
    return post_dict


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    new_post_dict = {column.name: value for column, value in zip(cursor.description, new_post)}
    return new_post_dict


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate):
    cursor.execute("""UPDATE posts SET (title, content, published) = (%s, %s, %s) WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    updated_post_dict = {column.name: value for column, value in zip(cursor.description, updated_post)}
    return updated_post_dict
