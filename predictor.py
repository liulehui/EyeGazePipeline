# coding:utf-8
import torch
import torch.nn as nn
from torchvision import models, transforms
import io
import time
import os
from PIL import Image


class Predictor():
    def __init__(self,num_of_class = 2):
        self.num_of_class = num_of_class
        self.predictor = self.init_predictor()

    def init_predictor(self):
        if self.num_of_class == 2:
            return UpperDownPredictor()
        # more possible classes

    def predict(self, image):
        label = self.predictor.predict(image)
        print(label)
        return label

class UpperDownPredictor():
    def __init__(self):
        self.class_num = 2
        self.model_save_path = "./models"
        self.model = self.init_model(self.model_save_path)

    def init_model(self, model_save_path = "./models"):
        # model architecture
        model = models.mobilenet_v2()
        num_ftrs = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.2, inplace=False),
            nn.Linear(in_features=num_ftrs, out_features=self.class_num, bias=True)
        )
        if os.path.exists(os.path.join(model_save_path, 'upperdown.pth')):
            model.load_state_dict(torch.load(os.path.join(model_save_path, 'upperdown.pth')))
            print('loaded trained model!')
        else:
            print('No model in such directory.')
        # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model.eval()

        return model

    def transform_image(self,image_bytes):
        my_transforms = transforms.Compose([transforms.Resize(256),
                                            transforms.CenterCrop(224),
                                            transforms.ToTensor(),
                                            transforms.Normalize(
                                                [0.485, 0.456, 0.406],
                                                [0.229, 0.224, 0.225])])
        image = Image.open(io.BytesIO(image_bytes))
        return my_transforms(image).unsqueeze(0)

    def predict(self, image_bytes):
        image = self.transform_image(image_bytes)
        outputs = self.model.forward(image)
        _, preds = torch.max(outputs, 1)

        # print(preds)

        # post processing
        label = preds
        return label

if __name__ == "__main__":

    predictor = Predictor()
    def print_out_label(filepath):
        with open(filepath, 'rb') as f:
            image_bytes = f.read()

            print("inference:")
            start_time = time.time()
            label = predictor.predict(image_bytes)
            end_time = time.time()
            inference_latency = end_time - start_time
            print(str(inference_latency))
            # print(label)

    for filename in os.listdir("./data/val/bottom"):
        print(filename)
        if os.path.exists(os.path.join("./data/val/bottom", filename)):
            print_out_label(os.path.join("./data/val/bottom", filename))