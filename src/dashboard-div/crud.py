from sqlalchemy.orm import Session
from . import model , schemas
import os , logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define the path to the logs directory one level up
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')

# Create the logs directory if it doesn't exist
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Define file paths
log_file_info = os.path.join(log_dir, 'info.log')
log_file_error = os.path.join(log_dir, 'error.log')

# Set up logging handlers
info_handler = logging.FileHandler(log_file_info)
info_handler.setLevel(logging.INFO)
error_handler = logging.FileHandler(log_file_error)
error_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
logger.addHandler(info_handler)
logger.addHandler(error_handler)

def create_detection_data(db:Session, detection_data:schemas.DetectionDataCreate):
    logger.info("creating the detection data ")
    try:
        db_detection = model.DetectionData(**detection_data.dict())
        db.add(db_detection)
        db.commit()
        db.refresh(db_detection)
        return db_detection
    except Exception as e:
        logger.error(f" error occured while creating detections")
        return None
def get_detection_data(db:Session, skip: int = 0 , limit:int = 10):
    logger.info("geting all the data")
    try:
        return db.query(model.DetectionData).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"error occured while presenting the whole data")
        return None
def get_detection_data_by_id(db: Session, detection_id: int):
    logger.info("Getting the data by unique id")
    try:
        # Correct the placement of parentheses
        return db.query(model.DetectionData).filter(model.DetectionData.id == detection_id).first()
    except Exception as e:
        logger.error(f"Error occurred while getting the data by unique id: {e}")
        return None  # Return None or handle the error as necessary
# Update a detection record by ID
def update_detection_data_by_id(db: Session, detection_id: int, update_data: dict):
    logger.info("Updating the data by unique id")
    try:
        detection = db.query(model.DetectionData).filter(model.DetectionData.id == detection_id).first()
        if not detection:
            return None
        for key, value in update_data.items():
            setattr(detection, key, value)
        db.commit()
        db.refresh(detection)
        return detection
    except Exception as e:
        logger.error(f"An error occurred while updating data: {e}")
        db.rollback()
        return None

# Delete a detection record by ID
def delete_detection_data_by_id(db: Session, detection_id: int):
    logger.info("Deleting the data by unique id")
    try:
        detection = db.query(model.DetectionData).filter(model.DetectionData.id == detection_id).first()
        if detection:
            db.delete(detection)
            db.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"An error occurred while deleting data: {e}")
        db.rollback()
        return False
