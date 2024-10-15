from sqlalchemy import Column, Integer, String, Float, LargeBinary
from.databse import Base

class DetectionData(Base):
    __tablename__ = 'detected_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    class_id = Column(Integer, nullable=False)
    x_center = Column(Float, nullable=False)
    y_center= Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    
