# -*- coding:utf-8 -*-
import socket


class TCPClient:
    def __init__(self, host, port):
        self.stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stream.connect((host, port))

        self.running = False
        self.write_buffer = ''
        self.receive_buf_size = 1024 * 1000 * 100
        self.on_receive_listener = None

    def set_on_receive_listener(self, listener):
        self.on_receive_listener = listener

    def writeable(self):
        return len(self.write_buffer) > 0

    def start(self):
        self.running = True
        while self.running:
            if self.writeable():
                self._write()
            self._receive()

    def stop(self):
        self.running = False

    def append_buffer(self, data):
        self.write_buffer += data

    def _write(self):
        sent = self.stream.send(self.write_buffer)
        self.write_buffer = self.write_buffer[sent:]

    def _receive(self):
        data = self.stream.recv(self.receive_buf_size)
        if len(data) == 0:
            return
        if self.on_receive_listener is None:
            return
        self.on_receive_listener(data)

