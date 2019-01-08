"""
Allow an object to alter its behavior when its internal state changes.
The object will appear to change its class.
"""

import abc
import logging
import datetime
import time
import random


class DeadmanStateMachine:
    """
    Define the interface of interest to clients.
    Maintain an instance of a ConcreteState subclass that defines the
    current state.
    """

    def __init__(self, state, timeout=120, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self._state = state
        self.timeout = timeout
        self.last_state = None
        self.last_ping = datetime.datetime.now()
        self.alert_sent = False
        self.resolve_sent = False

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_last_state(self):
        return self.last_state

    def set_last_state(self, last_state):
        self.last_state = last_state

    def get_last_ping(self):
        return self.last_ping

    def set_last_ping(self, ping_datetime):
        self.last_ping = ping_datetime

    def get_alert_sent(self):
        return self.alert_sent

    def set_alert_sent(self, alert_sent):
        self.alert_sent = alert_sent

    def get_resolve_sent(self):
        return self.resolve_sent

    def set_resolve_sent(self, resolve_sent):
        self.resolve_sent = resolve_sent

    def request(self):
        self.logger.debug("State is {}".format(self.get_state()))
        self._state.handle(self)

    def send_alert(self):
        self.logger.debug("Send alert")
        self.set_alert_sent(True)

    def send_resolve(self):
        self.logger.debug("Send resolve")
        self.set_resolve_sent(True)


class State(metaclass=abc.ABCMeta):
    """
    Define an interface for encapsulating the behavior associated with a
    particular state of the DeadmanStateMachine.
    """

    @abc.abstractmethod
    def handle(self, context):
        pass

    @abc.abstractmethod
    def go_next(self):
        pass


class AliveState(State):
    """
    Implement a behavior associated with AliveState

    Transitions:
    * next state is AliveState or DeadState
    """

    def handle(self, context):
        context.set_last_state(context.get_state())
        # reset notifications
        context.set_alert_sent(False)
        context.set_resolve_sent(False)
        self.go_next(context)

    def go_next(self, context):
        # last_ping > 15s => DeadState
        if (datetime.datetime.now() - context.get_last_ping()) > datetime.timedelta(seconds=context.get_timeout()):
            dead_state = DeadState()
            context.set_state(dead_state)
        else:
            context.set_state(self)


class DeadState(State):
    """
    Implement a behavior associated with DeadState

    Transitions:
    * next state is DeadState or RessurrectionState
    """

    def handle(self, context):
        context.set_last_state(context.get_state())
        if context.get_alert_sent() is False:
            context.send_alert()
        self.go_next(context)

    def go_next(self, context):
        # last_ping > 15s => DeadState (still)
        if (datetime.datetime.now() - context.get_last_ping()) > datetime.timedelta(seconds=context.get_timeout()):
            context.set_state(self)
        else:
            # last_ping < 15s => RessurrectionState
            ressurection_state = RessurrectionState()
            context.set_state(ressurection_state)


class RessurrectionState(State):
    """
    Implement a behavior associated with RessurrectionState

    Transitions:
    * next state is always AliveState
    """

    def handle(self, context):
        context.set_last_state(context.get_state())
        if context.get_resolve_sent() is False:
            context.send_resolve()
        self.go_next(context)

    def go_next(self, context):
        alive_state = AliveState()
        context.set_state(alive_state)


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    alive_state = AliveState()
    context = DeadmanStateMachine(alive_state, 10)

    while (datetime.datetime.now() - context.get_last_ping()) < datetime.timedelta(seconds=30):
        context.request()

        # randomize last ping
        random_number = random.randint(1,10)
        if random_number < 3:

            logger.debug("Ping")

            context.set_last_ping(datetime.datetime.now())

        time.sleep(1)


if __name__ == "__main__":
    main()
