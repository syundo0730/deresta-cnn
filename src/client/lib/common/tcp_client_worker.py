# -*- coding:utf-8 -*-
import threading


class TCPClientWorker(threading.Thread):
    def __init__(self, tcp_client):
        super(TCPClientWorker, self).__init__()
        self.client = tcp_client

    def __del__(self):
        self.stop()

    def run(self):
        self.client.start()

    def stop(self):
        self.client.stop()
        self.join()
