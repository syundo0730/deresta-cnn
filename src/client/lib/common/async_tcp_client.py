# -*- coding:utf-8 -*-
import socket
import asyncore


class AsyncTCPClient(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

        self.write_buffer = ''
        self.receive_buf_size = 1024 * 1000 * 100
        self.on_receive_listener = None

    def set_on_receive_listener(self, listener):
        self.on_receive_listener = listener

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(self.receive_buf_size)
        if self.on_receive_listener is not None:
            self.on_receive_listener(data)

    def writeable(self):
        return len(self.send_buffer) > 0

    def handle_write(self):
        sent = self.send(self.write_buffer)
        self.write_buffer = self.write_buffer[sent:]

    def append_buffer(self, data):
        self.write_buffer += data

    def start(self):
        asyncore.loop()

    def stop(self):
        self.handle_close()
