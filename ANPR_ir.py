import os
import statistics
import torch
import cv2 as cv
import numpy as np
from PIL import ImageOps
from copy import deepcopy

default_save_path = os.path.join(".", "resutls")
default_plate_model = os.path.join(".", "models", "plateYolo.pt")
default_char_model = os.path.join(".", "models", "CharsYolo.pt")

class ANRPIR(object):
    def __init__(self, 
                save_path: str=default_save_path, 
                plate_model:str=default_plate_model, 
                char_model:str=default_char_model,
                device:str="cpu",
        ):
        self.char_dict = {
            "0": "0",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "A": "10",
            "B": "11",
            "P": "12",
            "Taxi": "13",
            "ث": "14",
            "J": "15",
            "چ": "16",
            "ح": "17",
            "خ": "18",
            "D": "19",
            "ذ": "20",
            "ر": "21",
            "ز": "22",
            "ژ": "23",
            "Sin": "24",
            "ش": "25",
            "Sad": "26",
            "ض": "27",
            "T": "28",
            "ظ": "29",
            "PuV": "30",
            "غ": "31",
            "ف": "32",
            "Gh": "33",
            "ک": "34",
            "گ": "35",
            "L": "36",
            "M": "37",
            "N": "38",
            "H": "39",
            "V": "40",
            "Y": "41",
            "PwD": "42",
        }
        self.char_id_dict = {v: k for k, v in self.char_dict.items()}
        self.save_path = save_path
        self.plate_model_path = plate_model
        self.char_model_path = char_model
        self.device_id = device
        self.image_size = 640
        self.trace = False
        # loading the models
        self._load_models()
    
    def _load_models(self):
        self.plate_model = torch.hub.load(
            "yolov5", "custom", self.plate_model_path, source="local", force_reload=True
        )
        self.char_model = torch.hub.load(
            "yolov5", "custom", self.char_model_path, source="local", force_reload=True
        )
    
    def read_image(self, image_path):
        self.img = cv.imread(image_path)
    
    def read_frame(self, frame):
        self.img = frame

    def detectPlateChars(self, croppedPlate):
        chars, confidences, char_detected = [], [], []
        results = self.char_model(croppedPlate)
        detections = results.pred[0]
        detections = sorted(detections, key=lambda x: x[0])  # sort by x coordinate
        for det in detections:
            conf = det[4]
            if conf > 0.5:
                cls = det[5].item()
                char = self.char_id_dict.get(str(int(cls)), "")
                chars.append(char)
                confidences.append(conf.item())
                char_detected.append(det.tolist())
        charConfAvg = round(statistics.mean(confidences) * 100) if confidences else 0
        return "".join(chars), char_detected, charConfAvg


    def process_img(self):
        resize = self.prepareImage(self.img)
        platesTexts = []
        platesResult = self.plate_model(resize).pandas().xyxy[0]
        for _, plate in platesResult.iterrows():
            plateConf = int(plate['confidence'] * 100)
            if plateConf >= 60:
                self.highlightPlate(resize, plate)
                croppedPlate = self.cropPlate(resize, plate)
                plateText, char_detected, charConfAvg = self.detectPlateChars(croppedPlate)
                platesTexts.append(plateText)
                text_position = int(plate['xmin']), int(plate['ymin']) - 10  # Position the text above the rectangle
                font = cv.FONT_HERSHEY_SIMPLEX
                font_scale = 0.7
                text_color = (255, 255, 255)  # Green color in BGR
                text_thickness = 2

                # Put the text on the image
                cv.putText(resize, plateText, text_position, font, font_scale, text_color, text_thickness, cv.LINE_AA)
        
        return platesTexts, resize

    def prepareImage(self, img):
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        return img

    def highlightPlate(self, resize, plate):
        cv.rectangle(resize, (int(plate['xmin']) - 3, int(plate['ymin']) - 3),
                    (int(plate['xmax']) + 3, int(plate['ymax']) + 3),
                    color=(0, 0, 255), thickness=3)

    def cropPlate(self, resize, plate):
        return resize[int(plate['ymin']): int(plate['ymax']), int(plate['xmin']): int(plate['xmax'])]








