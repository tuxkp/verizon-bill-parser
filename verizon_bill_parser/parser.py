import os
from .mypdfutils import MyPDFUtils
import logging

logger = logging.getLogger(__name__)
def parse():
    return "Hello, world!"

def set_logger_level(level: str):
    logger.setLevel(level=level)

def parse_file(file_path: str):
    if not os.path.exists(file_path):
        raise Exception(f"File {file_path} does not exist")
    
    pdfUtils = MyPDFUtils(file_path)
    return pdfUtils.parsedData

def parse_directory(directory: str):
    resp_list = []
    #Check if the directory exists
    if not os.path.exists(directory):
        raise Exception(f"Directory {directory} does not exist")
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        logger.debug(f"Processing file: {file_path}")
        if os.path.isfile(file_path):
            resp_list.append(parse_file(file_path))
    return resp_list