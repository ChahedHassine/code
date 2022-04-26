import asyncio
import random
import getpass

from loguru import logger
from spade.agent import Agent

from spade_artifact import Artifact, ArtifactMixin


class RandomGeneratorArtifact(Artifact):
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

        while True:
            # Publish only if my friends are online
            if len(self.presence.get_contacts()) >= 1:
                random_num = random.randint(0, 100)
                await self.publish(f"{random_num}")
                logger.info(f"Publishing {random_num}")
            await asyncio.sleep(1)
if __name__ == "__main__":
    artifact_jid = "hassine@desktop-ahuhkk8"
    artifact_passwd = "admin"
    artifact = RandomGeneratorArtifact(artifact_jid, artifact_passwd)
    future = artifact.start()
    future.result()
    artifact.join()