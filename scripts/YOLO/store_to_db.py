import os , logging
from sqlalchemy import create_engine, Column , Integer , String , Float , LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import making_data_frame_the_detected_data as mk

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Format of the log messages
)
# Create a logger object
logger = logging.getLogger(__name__)

# define the path to the Logs directory one level up
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','logs')

# create the logs directory if it doesn't exist
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
# define file paths
log_file_info = os.path.join(log_dir, 'info.log')
log_file_error = os.path.join(log_dir, 'error.log')

# Create handlers
info_handler = logging.FileHandler(log_file_info)
info_handler.setLevel(logging.INFO)

error_handler = logging.FileHandler(log_file_error)
error_handler.setLevel(logging.ERROR)

# Create a formatter and set it for the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

# Create a logger and set its level
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Capture all info and above
logger.addHandler(info_handler)
logger.addHandler(error_handler)


# Defining the connection string to connect to PostgresSQL
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the detection data table model
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
    image_data = Column(LargeBinary, nullable=True)  # Column for image data

# create the table in the database 
def create_the_db_table():
    logger.info("Create the table ")
    try:
        logger.info("cratin the database table ")
        Base.metadata.create_all(engine)
        logger.info("database table created sucessfully")
    except Exception as e:
        logger.error(f"error occured while creating table in the database")
# Define acceptable image file extensions
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')

def insert_data(df, image_folder_path):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        logger.info("Inserting data into the database...")
        for _, row in df.iterrows():
            image_path = os.path.join(image_folder_path, row['filename'])
            
            # Check if the file is an image based on its extension
            if not image_path.lower().endswith(image_extensions):
                logger.warning(f"Skipping non-image file: {image_path}")
                continue

            try:
                with open(image_path, 'rb') as img_file:
                    image_data = img_file.read()

                detection = DetectionData(
                    filename=row['filename'],
                    class_id=row['class_id'],
                    x_center=row['x_center'],
                    y_center=row['y_center'],
                    width=row['width'],
                    height=row['height'],
                    confidence=row['confidence'],
                    image_data=image_data
                )
                session.add(detection)
            except FileNotFoundError:
                logger.error(f"Image file not found: {image_path}")
                continue

        session.commit()
        logger.info("Data inserted successfully.")
    except Exception as e:
        logger.error(f"An error occurred while inserting data: {e}")
        session.rollback()
    finally:
        session.close()
    

