from fastapi import FastAPI
# from pydantic import BaseModel
app = FastAPI()



# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: bool = None


@app.get("/")
async def root():
    return {"message": "Hello this is temporary"}
