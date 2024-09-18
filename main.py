from fastapi import FastAPI
from fastapi.params import Body


app = FastAPI()

@app.get("/")
def root():
    return {"message":"Welcome to my api"}

@app.post("/createpost")
def createpost(payload: dict = Body(...)):
    print(payload)
    return {"new_post":f"title: {payload['title']},content:{payload['content']}"}


