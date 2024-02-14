from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dashcam.src.settings import Settings

app = FastAPI()
#! This entire thing should be moved from the root folder when i know how to do it lol

origins = ["*"] # This is temporary, will be changed to the actual frontend URL

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
) 
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

Settings = Settings("settings.txt")

@app.get("/")
async def root():
    return {"message": "This is temporary"}


@app.get("/camera/{camera_id}/{setting}")
async def get_camera_setting(camera_id: int, setting: str): #? maybe change camera id to a string
    read_result = Settings.read_setting(f"{camera_id}-{setting}")
    if read_result is None:
        return {"camera_setting": "not found"}
    else:
        return {"camera_setting": read_result}
    
@app.post("/camera/{camera_id}/{setting}")
async def update_camera_setting(camera_id: int, setting: str, value: str): #? maybe change camera id to a string
    write_result = Settings.write_setting(f"{camera_id}-{setting}", value)
    if write_result is None:
        return {"camera_setting": "not found"}
    else:
        return {"camera_setting": value}




# @app.get("/camera/status")
# async def get_camera_status():
#     camera_status = read_setting("camera_status")
#     if camera_status is None:
#         return {"camera_status": "offline"}
#     else:
#         return {"camera_status": camera_status}
    


# @app.post("/camera/status")
# async def update_camera_status(status: str):
#     write_setting("camera_status", status)
#     return {"camera_status": status}