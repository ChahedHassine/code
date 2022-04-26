import argparse

from spade_bdi.bdi import BDIAgent

if __name__ == '__main__':
    agent_passwd = "admin"
    agent_jid = "adrian@desktop-ahuhkk8"

    a = BDIAgent(agent_jid , agent_passwd, "sender.asl")
    a.bdi.set_belief("receiver", "hassine@desktop-ahuhkk8")
    a.start()
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