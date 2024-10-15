from typing import Optional
from pydantic import BaseModel

class DetectionDataBase(BaseModel):
    filename: str
    class_id: int
    x_center: float
    y_center: float
    width: float
    height: float
    confidence: float

class DetectionDataCreate(DetectionDataBase):
    image_data: bytes

class DetectionDataResponse(DetectionDataBase):
    id: int

    class Config:
        orm_mode = True

class DetectionDataUpdate(BaseModel):
    filename: Optional[str] = None
    class_id: Optional[int] = None
    x_center: Optional[float] = None
    y_center: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    confidence: Optional[float] = None

    class Config:
        orm_mode = True
