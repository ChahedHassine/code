import asyncio
import random
import getpass
import cv2
import numpy as np
from loguru import logger
from spade.agent import Agent
import json

from spade_artifact import Artifact, ArtifactMixin

class RecogniseArtifact(Artifact):
    def on_available(self, jid, stanza):
        logger.success(
            "[{}] Agent {} is available.".format(self.name, jid.split("@")[0])
        )

    def on_subscribed(self, jid):
        logger.success(
            "[{}] Agent {} has accepted the subscription.".format(
                self.name, jid.split("@")[0]
            )
        )
        logger.success(
            "[{}] Contacts List: {}".format(self.name, self.presence.get_contacts())
        )

    def on_subscribe(self, jid):
        logger.success(
            "[{}] Agent {} asked for subscription. Let's aprove it.".format(
                self.name, jid.split("@")[0]
            )
        )
        self.presence.approve(jid)
        self.presence.subscribe(jid)

    async def setup(self):
        # Approve all contact requests
        self.presence.set_available()
        self.presence.on_subscribe = self.on_subscribe
        self.presence.on_subscribed = self.on_subscribed
        self.presence.on_available = self.on_available
    async def run(self):
        print("it works")
        while True:
            cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   
            _, video_frame = cap.read()  
            try:
                hsv = cv2.cvtColor(video_frame, cv2.COLOR_BGR2HSV)
                lower_red = np.array([0, 180, 134])
                upper_red = np.array([180, 255, 243]) 
                mask = cv2.inRange(hsv, lower_red, upper_red)
                kernel = np.ones((5, 5), np.uint8)
                mask = cv2.erode(mask, kernel)
                cv2.imshow('video_frame',video_frame)
                cv2.imshow('mask',mask) 
                #cv2.waitKey(0)   
            except ValueError as e:  
                print("ValueError Exception: {}".format(str(e)))
            if int(cv2.__version__[0]) > 3:
                # Opencv 4.x.x
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                #print('conversion to contours******************')
                #print("len during decoding*********************")
            else:
                # Opencv 3.x.x
                _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)        
            contours=[x.tolist() for x in contours]
            if len(contours) !=0:
                await self.publish(json.dumps(contours))
                logger.info("published")
            await asyncio.sleep(60)
class ConsumerAgent(ArtifactMixin, Agent):
    def __init__(self, *args, artifact_jid: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.artifact_jid = artifact_jid

    def artifact_callback(self, artifact, payload):
        logger.info(f"Received: [{artifact}] -> {payload}")

    async def setup(self):
        await asyncio.sleep(2)
        self.presence.approve_all = True
        self.presence.subscribe(self.artifact_jid)
        self.presence.set_available()
        await self.artifacts.focus(self.artifact_jid, self.artifact_callback)
        logger.info("Agent ready")        

if __name__ == "__main__":  
    #artifact_jid = "hassine@desktop-ahuhkk8"
    artifact_jid ="artifact@desktop-ahuhkk8"
    artifact_passwd = "admin"
    '''agent_passwd = "admin"
    agent_jid = "adrian@desktop-ahuhkk8"
    agent = ConsumerAgent(
        jid=agent_jid, password=agent_passwd, artifact_jid=artifact_jid
    )
    agent.start()'''
    artifact = RecogniseArtifact(artifact_jid, artifact_passwd)
    future = artifact.start()
    future.result()
    artifact.join()