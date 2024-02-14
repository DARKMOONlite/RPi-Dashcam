from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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


def write_setting(setting, value):
    try:
        with open("settings.txt", 'w') as file:
            for line in file:
                if line.startswith(setting):
                    file.write(f"{setting}={value}\n")
                    return value # find the first instance of the setting and replace it with the new value
                else:
                    file.write(line)
        return None # if the setting is not found, return None
    
    except OSError: # if the file is locked or something 
        print(f"Error writing to file {setting}")
        return None
        
def read_setting(setting):
    try:
        with open("settings.txt", 'r') as file:
            for line in file:
                if line.startswith(setting):
                    return line.split("=")[1]
        return None
    
    except OSError: # if the file is locked or something
        print(f"Error reading from file {setting}")
        return None


@app.get("/")
async def root():
    return {"message": "This is temporary"}





@app.get("/camera/{camera_id}/{setting}")
async def get_camera_setting(camera_id: int, setting: str):
    read_result = read_setting(f"{camera_id}_{setting}")
    if read_result is None:
        return {"camera_setting": "not found"}
    else:
        return {"camera_setting": read_result}
    
@app.post("/camera/{camera_id}/{setting}")
async def update_camera_setting(camera_id: int, setting: str, value: str):
    write_result = write_setting(f"{camera_id}_{setting}", value)
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