import logging
import datetime
import time
import random
from deadman_state_machine import deadman_state_machine, receivers


def main():
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    logger = logging.getLogger(__name__)
    alive_state = deadman_state_machine.AliveState()
    alert_dict = {
        'status': 'firing',
        'alertname':'DeadMansSwitch',
        'message':'SOS All is explosing',
    }
    resolve_dict = {
        'status': 'resolved',
        'alertname':'DeadMansSwitch',
        'message':'PHEW All is resolving',
    }
    receiver_list = [
        #receivers.HttpPostJsonReceiver('http://localhost:8000/hello'),
        receivers.HttpPostJsonReceiver('http://localhost:8000/deadman', alert_dict=alert_dict, resolve_dict=resolve_dict)
    ]
    context = deadman_state_machine.DeadmanStateMachine(alive_state, 10, receivers=receiver_list)

    while (datetime.datetime.now() - context.get_last_ping()) < datetime.timedelta(seconds=30):
        context.request()

        # randomize last ping
        random_number = random.randint(1,10)
        if random_number < 2:

            logger.debug("Ping")

            context.set_last_ping(datetime.datetime.now())

        time.sleep(1)


if __name__ == "__main__":
    main()
