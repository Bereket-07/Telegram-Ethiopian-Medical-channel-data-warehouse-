import os
import logging
import pandas as pd

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

output_data = []

def process_the_YOLO_object(path):
    logger.info("Processing the data collected from the YOLO object detection model...")
    try:
        for filename in os.listdir(path):
            if filename.endswith('.txt'):
                filepath = os.path.join(path, filename)
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        data = line.strip().split()
                        class_id = int(data[0])
                        x_center = float(data[1])
                        y_center = float(data[2])
                        width = float(data[3])
                        height = float(data[4])
                        confidence = float(data[5])
                        output_data.append([filename, class_id, x_center, y_center, width, height, confidence])
        df = pd.DataFrame(output_data, columns=['filename', 'class_id', 'x_center', 'y_center', 'width', 'height', 'confidence'])
        return df
    except Exception as e:
        logger.error(f"An error occurred while processing the data: {e}")
