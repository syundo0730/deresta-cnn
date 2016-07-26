# -*- coding:utf-8 -*-
import sys
import threading

from dere_stage_command_factory import DereStageCommandFactory
from src.client.lib.common.tcp_client_worker import TCPClientWorker
from src.client.lib.common.tcp_client import TCPClient


class MinitouchClient:
    def __init__(self, pad_positions):
        self.tcp_client = TCPClient("127.0.0.1", 1111)
        self.tcp_client_worker = TCPClientWorker(self.tcp_client)
        self.tcp_client_worker.start()
        self.pad_count = len(pad_positions)
        self.pressure = 200
        self.command_factories = [DereStageCommandFactory(i, self.pressure, p) for (i, p) in enumerate(pad_positions)]

    def __del__(self):
        self.stop()

    def stop(self):
        self.tcp_client_worker.stop()

    def exec_command(self, pad_id, command_name):
        if pad_id < 0 or pad_id >= len(self.command_factories):
            return False
        command_factory = self.command_factories[pad_id]
        commands = {
            'tap': command_factory.tap_sequence(),
            'right': command_factory.swipe_to_sequence('right'),
            'left': command_factory.swipe_to_sequence('left'),
            'down': command_factory.down_sequence(),
            'up': command_factory.up_sequence(),
            'up_right': command_factory.swipe_up_to_sequence('right'),
            'up_left': command_factory.swipe_up_to_sequence('left')
        }
        command_sequence = commands[command_name]
        if command_sequence is not None:
            self.exec_command_sequence(command_sequence)

    def exec_command_sequence(self, command_sequence):
        base_time = 0
        for command in command_sequence:
            wait = command.get_wait()
            deferred = threading.Timer(base_time, self.exec_send, (command,))
            deferred.start()
            if wait is not None:
                base_time += command.get_wait() * 0.001

    def exec_send(self, minitouch_command):
        self.tcp_client.append_buffer(minitouch_command.get_command())
        sys.stdout.write("sent! " + minitouch_command.get_command())


def main():
    pad_positions = [
        (500, 500),
        (500, 500),
        (500, 500),
        (500, 500),
        (500, 500),
    ]
    minitouch_client = MinitouchClient(pad_positions)
    # minitouch_client.exec_command(0, 'right')
    minitouch_client.exec_command(1, 'left')
    # minitouch_client.exec_command(2, 'up')
    # minitouch_client.exec_command(3, 'down')
    # minitouch_client.exec_command(4, 'tap')

if __name__ == '__main__':
    main()
