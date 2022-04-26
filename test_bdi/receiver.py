import argparse

from spade_bdi.bdi import BDIAgent

if __name__ == '__main__':
    artifact_jid = "hassine@desktop-ahuhkk8"
    artifact_passwd = "admin"

    a = BDIAgent(artifact_jid, artifact_passwd, "receiver.asl")
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