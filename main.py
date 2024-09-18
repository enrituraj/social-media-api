from typing import Optional
from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int] = None

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
    return {"data":my_posts}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) -1]
    return {"latest post":post}


@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"post with id {id} was not found."
        )
    return {"data":post}



@app.put("/posts/:id")
def update_post():
    pass


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
    


