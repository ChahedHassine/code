from __future__ import print_function
from base64 import decode
import copy
import cv2
import numpy as np
import sys
import requests
#from sklearn.externals import joblib
import cv2
import numpy as np
import time
import json


class Perception:
    """
    Data provided by the sensors, processed into information that update the world model. From actual world, to world
    model.  Acquires percepts via computer vision and arm controller invocation. Percept is the sensed XYZ position of
    an object in relation to the arm's frame of reference, in centimeters.
    """

    def __init__(self, init_world_model):
        print("--- Initializing perception...")
        self.perception_world_model = init_world_model.current_world_model.perception
        self.capture_device = cv2.VideoCapture(self.perception_world_model["local_camera_id"],cv2.CAP_DSHOW)
        self.capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   
    def get_percept(self, text_engraving=""):
        _, video_frame = self.capture_device.read()
        try:
            hsv = cv2.cvtColor(video_frame, cv2.COLOR_BGR2HSV)
            lower_red = np.array([0, 180, 134])
            upper_red = np.array([180, 255, 243]) 
            mask = cv2.inRange(hsv, lower_red, upper_red)
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel)
        except ValueError as e:  
            print("ValueError Exception: {}".format(str(e)))
        if int(cv2.__version__[0]) > 3:
            # Opencv 4.x.x
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #print('conversion to contours******************')
            contours=[x.tolist() for x in contours]
            #print("len during decoding*********************")
        
        else:
            # Opencv 3.x.x
            _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
            contours=[x.tolist() for x in contours]
        percept = {"mask": mask,
                   "video_frame":video_frame,
                   "contours":json.dumps(contours)
                   }
        #return mask,video_frame
        return percept
               
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break
    @staticmethod
    def belief_revision(input_world_model, percept):
        """
        Updates the current world model: B = beliefRevisionFunction(B, ρ)
        :param input_world_model: World model, instance of the WorldModel class.
        :param percept: Dictionary.
        :return: The updated world model, instance of the WorldModel class.
        """
        for key in percept.keys():
            if key == "mask": 
                input_world_model.current_world_model.mask["user"] = percept["mask"]
            if key == "video_frame": 
                input_world_model.current_world_model.video_frame["user"] = percept["video_frame"]   
            if key == "contours": 
                input_world_model.current_world_model.contours["user"] = percept["contours"]     

        return input_world_model

if __name__ == '__main__':

    # Sequence for testing
    from world_model import WorldModel
    world_model = WorldModel()
    perception = Perception(world_model)
    while True:
        percept=perception.get_percept()
        input_world_model=perception.belief_revision(world_model,percept)
        #print(input_world_model.current_world_model.mask["user"])
        #print(input_world_model.current_world_model.video_frame["user"])
        contours=input_world_model.current_world_model.contours["user"]
        print(type(contours))
        #print(mask)
        #print(video_frame)
        cv2.imshow('video_frame',input_world_model.current_world_model.video_frame["user"])
        cv2.imshow('mask',input_world_model.current_world_model.mask["user"])  
        if cv2.waitKey(0) == ord('a'):
            break
    cv2.destroyAllWindows()

