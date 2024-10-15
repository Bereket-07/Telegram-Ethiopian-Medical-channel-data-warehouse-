from fastapi import FastAPI, Depends , HTTPException
from sqlalchemy.orm import Session
from . import crud , model ,schemas
from .databse import engine ,Base , get_db
from fastapi.middleware.cors import CORSMiddleware



# Create a database tables
Base.metadata.create_all(bind=engine)




app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific domains, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Or restrict to specific methods like ["GET", "POST"]
    allow_headers=["*"],  # Or specify allowed headers like ["Authorization", "Content-Type"]
)

@app.post("/detections/",response_model=schemas.DetectionDataBase)
def create_detection(detection:schemas.DetectionDataCreate,db:Session=Depends(get_db)):
    return crud.create_detection_data(db=db,detection_data=detection)
@app.get("/detections/",response_model=list[schemas.DetectionDataResponse])
def read_detection(skip:int = 0 , limit: int = 1000,db:Session=Depends(get_db)):
    deection = crud.get_detection_data(db,skip=skip,limit=limit)
    return deection
@app.get("/detections/{detection_id}" , response_model=schemas.DetectionDataResponse)
def read_detection(detection_id:int,db:Session=Depends(get_db)):
    detection = crud.get_detection_data_by_id(db,detection_id=detection_id)
    if detection is None:
        raise HTTPException(status_code=404,detail="Detection not Found")
    return detection
@app.put("/detections/{detection_id}", response_model=schemas.DetectionDataResponse)
def update_detection(detection_id: int, update_data: schemas.DetectionDataUpdate, db: Session = Depends(get_db)):
    detection = crud.get_detection_data_by_id(db, detection_id=detection_id)
    if detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")
    
    updated_detection = crud.update_detection_data_by_id(db, detection_id=detection_id, update_data=update_data.dict())
    if updated_detection is None:
        raise HTTPException(status_code=500, detail="Failed to update detection")
    
    return updated_detection
@app.delete("/detections/{detection_id}", status_code=204)
def delete_detection(detection_id: int, db: Session = Depends(get_db)):
    detection = crud.get_detection_data_by_id(db, detection_id=detection_id)
    if detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")
    
    success = crud.delete_detection_data_by_id(db, detection_id=detection_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete detection")
    return