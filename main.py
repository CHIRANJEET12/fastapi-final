from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "title 1", "content": "content 1", "id": 1},
    {"title": "title 2", "content": "content 2", "id": 2}
]




@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.post("/createpost")
# def crate(payload: dict = Body(...)):
#     print(payload)
#     return {"message": "This is post request"}

@app.get("/getposts")
def getposts():
    return {"data": my_posts}


@app.post("/createpost")
def createposts(p: Post):
    post_dict = p.model_dump()
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)
    # print(p.title)
    # print(p.content)
    # print(p.model_dump())
    return {"new_data": post_dict}
