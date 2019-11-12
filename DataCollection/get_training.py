import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import shutil

# excel directortyx-
excel_directory = r'C:\Users\zhangzhida\Desktop\eyegaze\data.csv'

# raw photo directory
raw_photo_directory = r'C:\Users\zhangzhida\Desktop\eyegaze\raw_data'

# result photo directory
result_directory = r'C:\Users\zhangzhida\Desktop\eyegaze\preparation'

# num of cameras
num_of_cameras = 2

# read excel
df = pd.read_csv(excel_directory)

def move_to_result_directory(filename,source_directory, result_directory, sub_directory):
    print("move_to")
    # create directory if not exists
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)
    
    if not os.path.exists( os.path.join(result_directory, sub_directory)):
        os.makedirs(os.path.join(result_directory, sub_directory))
    
    destination_file_name = os.path.join(result_directory, sub_directory, filename)
    source_filename = os.path.join(source_directory, filename)
#     os.rename(destination_file_name)
    shutil.copy2(source_filename, destination_file_name)

    