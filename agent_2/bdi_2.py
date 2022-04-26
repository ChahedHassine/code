import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
from spade.behaviour import CyclicBehaviour
#from object_detector import *
import numpy as np
import json
from world_model import WorldModel
#from hierarchical_task_network_planner import HierarchicalTaskNetworkPlanner
from collections import deque
from perception import Perception
from spade_artifact import Artifact, ArtifactMixin
from loguru import logger
import asyncio


class MyBehav(CyclicBehaviour):
        def __init__(self, consumer_agent):
                super().__init__()
                self.agent=consumer_agent
        async def on_start(self):
            print("Starting behaviour . . .")
            self.terminate = False
            self.SUCCESS = False
            self.verbose = False

            # Initialization
            self.beliefs = WorldModel(self.agent)  # B := B0; Initial Beliefs
            self.goals = self.beliefs.current_world_model.goals
            self.intentions = self.beliefs.current_world_model.goals  # I := I0; Initial Intentions
            #self.htn_planner = HierarchicalTaskNetworkPlanner(self.beliefs)
            self.perception = Perception(self.beliefs)
            self.what, self.why, self.how_well, self.what_else, self.why_failed = "", "", "", "", ""
            self.plans = []
            self.selected_plan = []
            self.percept = {}
            self.action = ""

        async def run(self):
            print('work')
            '''if not self.SUCCESS and not self.terminate :
                if len(self.selected_plan) == 0:
                     self.percept = self.perception.get_percept()  # get next percept ρ; OBSERVE the world'''




class ReceiverAgent(ArtifactMixin, Agent):             
    async def setup(self):
        logger.info("Agent ready")
        self.presence.approve_all = True
        self.presence.set_available()
        self.my_behav = MyBehav(self)
        self.add_behaviour(self.my_behav)
        



if __name__ == "__main__":
    receiveragent = ReceiverAgent("adrian@desktop-ahuhkk8", "admin")
    future = receiveragent.start()
    future.result() # wait for receiver agent to be prepared.
    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            receiveragent.stop()
            break