from typing import Union, Annotated
import json
from PIL import Image
import numpy as np
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from image_process import seperateBoxesAndSaveIt, takeBoxOneByOneAndSaveCharactersSeperatelyAndSaveItInATextFile, delete_files_in_root_folder
from calculation import calculations
import cv2
import os

app = FastAPI()
#End point which recieves main image and return the set of strings for the veryfication purposes
@app.post("/api/main_image/")
async def processImg (image:UploadFile) :
    ##print(await image.read())
    contents = await image.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('MainImage.png', img)
    isWriteSuccess = cv2.imwrite('./MainImage.png', img)
    print("image written to disk")

    if(isWriteSuccess == False)  :
        return
        ## send error erorr  
    
    delete_files_in_root_folder(["bending_moment_graph2.jpeg"])
    return takeBoxOneByOneAndSaveCharactersSeperatelyAndSaveItInATextFile(seperateBoxesAndSaveIt("./MainImage.png"))

#Recieving the verified input as an list and return the answer as two image files

@app.post("/api/verified_data/")
async def calculation (req : Request) :
    print("calculation starting")
    verifiedValues = await req.json()
    processedValues = []
    for value in verifiedValues['data'] :
        processedValues.append(value[0])
    print(processedValues)
    ##return verifiedValues
    print("before calculation")    
    calculations(processedValues)
    for file_name in os.listdir():
          if (file_name == "bending_moment_graph.jpeg"):   
            return  FileResponse("./bending_moment_graph.jpeg")
    return  FileResponse("./Inputs are wrong or Structure is imbalanced.jpeg")