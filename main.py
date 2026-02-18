from fastapi import Body, FastAPI, Query, Path
from pydantic import BaseModel, AfterValidator, Field
from typing import Optional, Annotated, Literal
from random import random, randrange

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


@app.get("/itemss/")
async def read_items(q: Annotated[str | None, Query(alias="item-query", min_length=10, max_length=50, pattern="^fixedquery$")]=None):
    results = {
        "items" : [{"item_id": "Foo"}, {"item_name": "Bar"}]
    }
    if q:
        results.update({"q":q})
    return results


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError("Invalid Id")
    return id

@app.get("/itemsssss/")
async def read_itemss(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None
    ):
    if id: 
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}
    

@app.get("/items/{items_id}")
def read_items(item_id: Annotated[int, Path(title="The ID of the item to get", ge=100, le=1000)],
               size: Annotated[float, Query(gt=0, lt=10.5)],
               q: Annotated[str | None, Query(alias="Item-query")] = None):
    results = {"item_id": item_id}
    if q:
        results.update({"q":q})
    if size:
        results.update({"size": size})
    return results

@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results



class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items/")
def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
# /items/?limit=10&offset=5&order_by=updated_at&tags=ai&tags=ml
# def read_items(limit: int, offset: int, order_by: str, tags: list[str])
# item: Item = Body(embed=True)


