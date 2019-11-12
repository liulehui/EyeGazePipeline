import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import shutil

csv_filename = os.path.join(os.getcwd(), 'eval_prediction.csv')
if not os.path.exists(csv_filename):
    df = pd.DataFrame(columns=['img_name', 'img_time', 'gaze_time', 'real_label', 'predict_label'])
    df.to_csv(csv_filename, mode='a', index=False)

img_dir = r'C:\Users\zhangzhida\Desktop\EyeGazePipeline\data\screenshot'
gaze_data_dir = r'C:\Users\zhangzhida\Desktop\EyeGazePipeline\observer'


