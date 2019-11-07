import numpy as np
import os
import glob
from PIL import Image
import cv2
import shutil
import argparse
from sklearn.model_selection import train_test_split

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

class DataProcess(object):
    # change the folder name to each data path and label path, and create a new folder test_path to store the data and test dataset (npy). The groundtruth should be eroded to only contain the border.
    def __init__(self,
                 out_rows,
                 out_cols,
                 data_path="./data/",
                 img_type="png"):

        """
        """
        self.out_rows = out_rows
        self.out_cols = out_cols
        self.data_path = data_path
        self.img_type = img_type

    def train_val_split(self, classname):

        imgs = glob.glob(self.data_path+classname+'/*.' + self.img_type)

        img_train, img_val = train_test_split(
            imgs, test_size=0.2, random_state=42)

        make_dir(self.data_path + 'train/' + classname)
        make_dir(self.data_path + 'val/' + classname)
        for source_path in img_train:

            imgname = source_path.split('/')[-1]
            shutil.copy2(source_path, self.data_path + 'train/'+classname + '/'+imgname)
        for source_path in img_val:
            imgname = source_path.split('/')[-1]

            shutil.copy2(source_path, self.data_path + 'val/'+classname + '/'+ imgname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--image_size', type=int, default=256)
    config = parser.parse_args()
    mydata = DataProcess(config.image_size, config.image_size)
    mydata.train_val_split('top')
    mydata.train_val_split('bottom')


