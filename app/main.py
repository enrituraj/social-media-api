from typing import Optional
from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',
                                user='postgres',password='1234',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection Successfully.")
        break
    except Exception as error:
        print("Database connection failed.")
        print("Error : ",error)
        time.sleep(3)

my_posts = [
    {
        "id":1,
        "title":"title of post 1",
        "content":"content of post 1",
    },
    {
        "id":2,
        "title":"title of post 2",
        "content":"favouritre food pizza",
    },
]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message":"Welcome to my api"}


@app.post("/posts",status_code = status.HTTP_201_CREATED)
def create_posts(new_post:Post):
    post_dict = new_post.dict()
    post_dict['id']= randrange(0,100000)
    my_posts.append(post_dict)
    return {"new_post":post_dict}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data":posts}


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute(""" SELECT * FROM posts ORDER BY DESC LIMIT 1 """)
    posts = cursor.fetchall()
    return {"data":posts}


@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"post with id {id} was not found."
        )
    return {"data":post}



@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    print(post)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exit"
        )
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data":post_dict}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exit"
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


