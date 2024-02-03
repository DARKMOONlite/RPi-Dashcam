from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI()


origins = ["http://localhost:80"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/")
async def root():
    return {"message": "This is temporary"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q:str = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def save_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}