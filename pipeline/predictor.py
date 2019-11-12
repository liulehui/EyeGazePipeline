# coding:utf-8
import pandas as pd
import torch
import torch.nn as nn
from torchvision import models, transforms
import io
import time
import os
from PIL import Image
import platform


class Predictor():
    def __init__(self, num_of_class = 2):
        self.num_of_class = num_of_class
        self.predictor = self.init_predictor()

    def init_predictor(self):
        if self.num_of_class == 2:
            return UpperDownPredictor()
        # more possible classes

    def predict(self, image, img_name):
        label = self.predictor.predict(image, img_name)
        print(label)
        return label

class UpperDownPredictor():
    def __init__(self):
        self.class_num = 2

        self.model_save_path = os.path.join(os.getcwd(), "models") # "./models"
        self.model = self.init_model()

    def init_model(self):
        # model architecture
        model = models.mobilenet_v2()
        num_ftrs = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.2, inplace=False),
            nn.Linear(in_features=num_ftrs, out_features=self.class_num, bias=True)
        )
        if os.path.exists(os.path.join(self.model_save_path, 'upperdown.pth')):
            model.load_state_dict(torch.load(os.path.join(self.model_save_path, 'upperdown.pth')))
            print('loaded trained model!')
        else:
            print('No model in such directory.')
        # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model.eval()
        return model

    def transform_image(self, image_bytes):
        my_transforms = transforms.Compose([transforms.Resize(256),
                                            transforms.CenterCrop(224),
                                            transforms.ToTensor(),
                                            transforms.Normalize(
                                                [0.485, 0.456, 0.406],
                                                [0.229, 0.224, 0.225])])
        image = Image.open(io.BytesIO(image_bytes))
        return my_transforms(image).unsqueeze(0)

    def predict(self, image_bytes, img_name):
        image = self.transform_image(image_bytes)
        outputs = self.model.forward(image)
        _, preds = torch.max(outputs, 1)
        # print(preds)
        # post processing
        label = preds.item()
        csv_filename = os.path.join(os.getcwd(), 'prediction.csv')
        if not os.path.exists(csv_filename):
            df = pd.DataFrame(columns=['img_name', 'predict_label'])
            df.to_csv(csv_filename, index=False)

        new_row = img_name[:-1] + ',' + str(label) + '\n'
        with open(csv_filename, 'a') as fd:
            fd.write(new_row)

        return label

        # write the predicted labels to results.csv



        # display on the screen in real time

# if __name__ == "__main__":
#
#     predictor = Predictor()
#
#     # def print_out_label(filepath):
#     #     with open(filepath, 'rb') as f:
#     #         image_bytes = f.read()
#     #
#     #         print("inference:")
#     #         start_time = time.time()
#     #         label = predictor.predict(image_bytes)
#     #         end_time = time.time()
#     #         inference_latency = end_time - start_time
#     #         print(str(inference_latency))
#     #         print(label)



    # if platform.system() == 'Windows':
    #     data_dir = os.getcwd() + "\\data\\val\\bottom"
    # else:
    #     data_dir = os.getcwd() + "/data/val/bottom"
    # for filename in os.listdir(data_dir):
    #     print(filename)
    #     if os.path.exists(os.path.join(data_dir, filename)):
    #         print_out_label(os.path.join(data_dir, filename))