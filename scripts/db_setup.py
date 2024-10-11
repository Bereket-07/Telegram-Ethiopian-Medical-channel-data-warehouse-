from sqlalchemy import create_engine
import os,logging
from dotenv import load_dotenv
import pandas as pd


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




# connecting to database
load_dotenv()

# get iindividual variables 
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# constructing the database URL

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def load_data():
    logger.info("storing the data frame into the database")
    try:
        # connect to the datbase
        engine = create_engine(DATABASE_URL)
        logger.info("loading the csv file ")
        # load the data 
        df = pd.read_csv('../data/scraped_data.csv')
        logger.info("srotring the dataframes into the sql database ")
        # Store the Dataframe into the databse
        df.to_sql('medical_data' , engine , if_exists='replace',index=False)
        logger.info(f"the dataframe stored to the database sucessfully")
    except Exception as e:
        logger.error(f"Error occured while storing the Dataframe into the database")

if __name__ == "__main__":
    load_data()     


