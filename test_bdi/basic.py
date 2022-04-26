import argparse
import time

from spade_bdi.bdi import BDIAgent
from spade.template import Template
from spade.behaviour import PeriodicBehaviour
from spade.behaviour import TimeoutBehaviour
from datetime import datetime
from datetime import timedelta


class MasterAgent(BDIAgent):
    async def setup(self):
        template = Template(metadata={"performative": "Modify"})
        self.add_behaviour(self.Modify(period=5, start_at=datetime.now()), template)

        template = Template(metadata={"performative": "Ending"})
        self.add_behaviour(self.Behav4(start_at=datetime.now() + timedelta(seconds=11)), template)

    class Modify(PeriodicBehaviour):
        async def run(self):
            if self.agent.bdi_enabled:
                try:
                    count_type = self.agent.bdi.get_belief_value("type")[0]
                    if count_type == 'inc':
                        self.agent.bdi.set_belief('type', 'dec')
                    else:
                        self.agent.bdi.set_belief('type', 'inc')
                except Exception as e:
                    self.kill()

    class Behav4(TimeoutBehaviour):
        async def run(self):
            self.agent.bdi.remove_belief('type', 'inc')
            self.agent.bdi.remove_belief('type', 'dec')

    

agent_jid = "adrian@desktop-ahuhkk8"
agent_passwd = "admin"
a = MasterAgent(agent_jid ,agent_passwd , "basic.asl")

future = a.start()
future.result()
import time
time.sleep(1)
print("Wait until user interrupts with ctrl+C")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")
a.stop()