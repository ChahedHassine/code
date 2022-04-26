import asyncio
import random
import getpass
import time
from loguru import logger
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour,OneShotBehaviour
from spade_artifact import Artifact, ArtifactMixin
import cv2
import numpy as np
import json
from spade.message import Message
from world_model import WorldModel
from collections import deque
from perception import Perception
class MyBehav(CyclicBehaviour):
        def comnets(self,artifact, payload):
            logger.info(f"Received: [{artifact}] -> {payload}")
        def __init__(self, consumer_agent):
                super().__init__()
                self.agent=consumer_agent
        async def on_start(self):
            print("Starting behaviour . . .")
            #self.counter = 0

        async def run(self):
            #print("Counter: {}".format(self.counter))
            #self.counter += 1
            await self.agent.artifacts.focus(self.agent.artifact_jid, self.comnets)
            await asyncio.sleep(1) 
            '''msg = Message(to="adrian@desktop-ahuhkk8")  # Instantiate the message  # TODO: place holder for IM
            msg.set_metadata("performative", "inform")
            msg.body = json.dumps([self.agent.w,self.agent.h]) # Set the message content
            await self.send(msg)
            print('message sent to other agent')
            self.kill(exit_code=10)'''


class ConsumerAgent(ArtifactMixin, Agent):
    def __init__(self, *args, artifact_jid: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.artifact_jid = artifact_jid
    def artifact_callback(self, artifact, payload):
            #logger.info(f"Received: [{artifact}] -> {payload}") 
            contours=json.loads(payload)
            contours=tuple(np.array(x, dtype=np.int32) for x in contours )
            for cnt in contours:
                rect = cv2.minAreaRect(cnt)
                (x,y),(w,h),angle=rect
                logger.info(f"Received: [{artifact}] -> width={w},height={h}")
                self.w=w
                self.h=h
                break
                '''msg = Message(to="adrian@desktop-ahuhkk8")  # Instantiate the message  # TODO: place holder for IM
                msg.set_metadata("performative", "inform")
                msg.body = json.dumps([w,h]) # Set the message content
                print('message sent')
                self.send(msg)'''
                #print("width=",w,"height",h)
                #print("Message received ")              
    async def setup(self):
        logger.info("Agent ready")
        self.presence.approve_all = True
        self.presence.subscribe(self.artifact_jid)
        self.presence.set_available()
        self.my_behav = MyBehav(self)
        self.add_behaviour(self.my_behav)


if __name__ == "__main__":
    artifact_jid = "hassine@desktop-ahuhkk8"
    artifact_passwd = "admin"
    agent_jid = "artifact@desktop-ahuhkk8"
    agent_passwd = "admin"
    agent = ConsumerAgent(
        jid=agent_jid, password=agent_passwd, artifact_jid=artifact_jid
    )
    future = agent.start()
    future.result()

    print("Wait until user interrupts with ctrl+C")
    while not agent.my_behav.is_killed():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    agent.stop()