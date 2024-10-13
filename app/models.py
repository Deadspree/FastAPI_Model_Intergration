from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, index=True)
    image_file_path = Column(String, primary_key = True, index=True)
    class_predicted = Column(Integer)  # Change to String if you prefer class labels
    timestamp = Column(DateTime, default=datetime.utcnow)
