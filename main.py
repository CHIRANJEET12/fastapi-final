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


class getItems(BaseModel):
    item_name: str = None
    price: float

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None



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


@app.get("/items/{item_id}")
def getSpecificItem(item_id: int, item: getItems):
    return {"item_name": item.item_name, "item_id": item_id, "item_price": item.price}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}