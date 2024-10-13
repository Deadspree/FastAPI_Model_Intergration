from typing import Optional

from fastapi import FastAPI, Depends
from fastapi import File, UploadFile
from PIL import Image
from io import BytesIO

from torchvision import transforms
import torch
import torchvision.models as models
import logging
import app.config.logging_config as config
import torch.nn as nn
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .database import get_db
from .models import Prediction
from sqlalchemy.exc import IntegrityError


app = FastAPI()


config.initLog()
log = logging.getLogger("dog-cat")
def read_imagefile(data) -> Image.Image:
    image = Image.open(BytesIO(data))
    return image

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/pet/")
async def predict(file: UploadFile=File(...), db: Session = Depends(get_db)):
    

    image = read_imagefile(await file.read())
    tfms= transforms.Compose([
                                            transforms.Resize((224,224)),
                                            #transforms.RandomRotation(20),
                                            #transforms.RandomVerticalFlip(p=0.1),
                                            transforms.ToTensor(),
                                            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
                                            ])
    image = tfms(image)
    image = image[None,:]
    dcModel = models.resnet18(weights=False)
    num_classes = 2
    class_names = ['cat', 'dog']
    dcModel.fc = nn.Linear(dcModel.fc.in_features, num_classes)
    dcModel.load_state_dict(torch.load('C:/Users/Admin_PC/fastapi-dog-cat-main/model_weights.pth',map_location=torch.device('cpu')))
    dcModel.eval()
    with torch.no_grad():
        outputs = dcModel(image)
        _, predicted = torch.max(outputs, 1)
        db_prediction = Prediction(
            image_file_path = file.filename,
            class_predicted = class_names[predicted.item()]
        )
        try:
            db.add(db_prediction)
            db.commit()
        except IntegrityError:
            db.rollback()  # Rollback if there's an integrity error (e.g., duplicate entry)
            log.warning("Prediction already exists in the database.")
                
        return {"Prediction": class_names[predicted.item()]}
             

