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
from spade_artifact import Artifact
from loguru import logger
class Perception:
    """
    Data provided by the sensors, processed into information that update the world model. From actual world, to world
    model.  Acquires percepts via computer vision and arm controller invocation. Percept is the sensed XYZ position of
    an object in relation to the arm's frame of reference, in centimeters.
    """

    def __init__(self, init_world_model):
        self.agent=init_world_model.agent
        print("--- Initializing perception...")
        self.perception_world_model = init_world_model.current_world_model.perception
        self.artifact_1=  self.perception_world_model["artifact_1"]
        self.detect= init_world_model.current_world_model.detect["user"]
    def comnets(self,artifact, payload):
            logger.info(f"Received: [{artifact}] -> {payload}")
            contours=json.loads(payload)
            contours=tuple(np.array(x, dtype=np.int32) for x in contours )
            for cnt in contours:
                rect = cv2.minAreaRect(cnt)
                (x,y),(w,h),angle=rect
                logger.info(f"Received: [{artifact}] -> width={w},height={h}")
                self.w=w
                self.h=h    
    def get_percept(self):
        if self.detect == False:
            self.agent.artifacts.focus(self.artifact_1, self.comnets)
            
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

