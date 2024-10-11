import os , logging , re
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


def load_data(path):
    logger.info("loading the data ")
    try:
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"error occured while loading the data: {e}")
def merge_the_data_frames(dataframes):
    logger.info("merging the whole data frames into one big data frame")
    try:
        return pd.concat(dataframes,ignore_index=True)
    except Exception as e:
        logger.error(f"error occured while merging the dataframes")
def check_for_missing_values(df):
    logger.info("checking for missing values")
    try:
        logger.info(f"missing values detected: \n {df.isnull().sum()}")
    except Exception as e:
        logger.error(f"error occured while checking for missing values")
def Standardixing_the_data(df):
    logger.info("standardizing the data frame")
    try:
        # Standardize text fields
        df['Channel Title'] = df['Channel Title'].str.lower().str.strip()
        df['Channel Username'] = df['Channel Username'].str.lower().str.strip()
        df['Media Path'] = df['Media Path'].apply(lambda x: x.replace('\\', '/'))  # convert to consistent path format
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Apply the function to the Message column
        logger.info("cleaining the message column ")
        df['Message'] = df['Message'].apply(clean_text)
        logger.info("the message column cleaned sucessfully")
        return df
    except Exception as e:
        logger.error(f"error occured while standardizing the data frame : {e}")
def clean_text(text):
    # Remove emojis
    text = re.sub(r'[^\w\s\u1200-\u137F]', '', text)  # Keeps English, Amharic, spaces, and removes emojis
    # Replace multiple spaces and newlines with a single space
    text = re.sub(r'\s+', ' ',text)
    # Remove leading and trailing whitespace
    text = text.strip()
    return text
