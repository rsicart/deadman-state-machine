import unittest
import datetime
import time
from deadman import deadman_state_machine

class ActiveStateTestCase(unittest.TestCase):

    def test_handle_alive_to_alive(self):
        alive_state = deadman_state_machine.AliveState()
        timeout = 30
        context = deadman_state_machine.DeadmanContext(alive_state, timeout)
        # set last_ping more recent than timeout to simulate a received ping
        context.set_last_ping(datetime.datetime.now() - datetime.timedelta(seconds=1))
        # before transition
        self.assertEqual(True, isinstance(context.get_state(), deadman_state_machine.AliveState))
        # process request & state transition
        context.request()
        self.assertEqual(True, isinstance(context.get_state(), deadman_state_machine.AliveState))
        self.assertEqual(True, isinstance(context.get_last_state(), deadman_state_machine.AliveState))

    def test_handle_alive_to_dead(self):
        alive_state = deadman_state_machine.AliveState()
        timeout = 1
        context = deadman_state_machine.DeadmanContext(alive_state, timeout)
        # force timeout without waiting
        # set last_ping older than timeout to simulate blackout
        context.set_last_ping(datetime.datetime.now() - datetime.timedelta(seconds=30))
        # before transition
        self.assertEqual(True, isinstance(context.get_state(), deadman_state_machine.AliveState))
        # process request & state transition
        context.request()
        self.assertEqual(True, isinstance(context.get_state(), deadman_state_machine.DeadState))
        self.assertEqual(True, isinstance(context.get_last_state(), deadman_state_machine.AliveState))


class DeadStateTestCase(unittest.TestCase):

    def test_handle_dead_to_dead(self):
        dead_state = deadman_state_machine.DeadState()
        timeout = 1
        context = deadman_state_machine.DeadmanContext(dead_state, timeout)
        # set last_ping older than timeout to simulate blackout
        context.set_last_ping(datetime.datetime.now() - datetime.timedelta(seconds=30))
        # before transition
        self.assertEqual(True, isinstance(context.get_state(), deadman_state_machine.DeadState))
        # process request & state transition
        context.request()
        self.assertEqual(True, isinstance(context.get_state(), deadman_state_machine.DeadState))
        self.assertEqual(True, isinstance(context.get_last_state(), deadman_state_machine.DeadState))

    def test_handle_dead_to_ressurrection(self):
        dead_state = deadman_state_machine.DeadState()
        timeout = 30
        context = deadman_state_machine.DeadmanContext(dead_state, timeout)
        # set last_ping more recent than timeout to simulate a received ping
        context.set_last_ping(datetime.datetime.now() - datetime.timedelta(seconds=1))
        # before transition
        self.assertEqual(True, isinstance(context.get_state(), deadman_state_machine.DeadState))
        # process request & state transition
        context.request()
        self.assertEqual(True, isinstance(context.get_state(), deadman_state_machine.RessurrectionState))
        self.assertEqual(True, isinstance(context.get_last_state(), deadman_state_machine.DeadState))


class RessurrectionStateTestCase(unittest.TestCase):

    def test_handle_ressurrection_to_alive(self):
        ressurrection_state = deadman_state_machine.RessurrectionState()
        timeout = 1
        context = deadman_state_machine.DeadmanContext(ressurrection_state, timeout)
        # before transition
        self.assertEqual(True, isinstance(context.get_state(), deadman_state_machine.RessurrectionState))
        # process request & state transition
        context.request()
        self.assertEqual(True, isinstance(context.get_state(), deadman_state_machine.AliveState))
        self.assertEqual(True, isinstance(context.get_last_state(), deadman_state_machine.RessurrectionState))
