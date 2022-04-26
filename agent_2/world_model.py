import time
import json
import os
import pyhop 
import cv2 
class WorldModel:  # TODO: Move 2 gremlin world model with init
    """
    Stores and updates current & past world models, instances of a Pyhop State class.
    """

    def __init__(self,consumer_agent):
        self.agent= consumer_agent
        self.current_world_model = pyhop.State("current_world_model")
         # Planner
        if os.path.isfile('json/planner.json'):
            with open('json/planner.json') as f:
                self.current_world_model.planner = json.load(f)
        #Perception
        if os.path.isfile('json/perception.json'):
            with open('json/perception.json') as f:
                self.current_world_model.perception = json.load(f)              
        # Goals
        self.current_world_model.goals = [tuple(self.current_world_model.planner["goals"])]
        self.current_world_model.object_width = {'user':None} 
        self.current_world_model.object_height = {'user':None}
        self.current_world_model.perception = {"artifact_1":"artifact@desktop-ahuhkk8","artifact_2":"artifact@desktop-ahuhkk8"}
        self.current_world_model.detect={'user':False}


        

if __name__ == '__main__':
    # Sequence for testing
    world_model = WorldModel()
    print(world_model.current_world_model.goals)
   