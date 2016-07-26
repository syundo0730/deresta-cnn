# -*- coding:utf-8 -*-
import socket
import threading


class AsyncTCPClient(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.write_buffer = ''

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        pass

    def writeable(self):
        return len(self.send_buffer) > 0

    def handle_write(self):
        sent = self.send(self.write_buffer)
        self.write_buffer = self.write_buffer[sent:]

    def append_buffer(self, data):
        self.write_buffer += data


class AsyncTCPClientHandler:
    def __init__(self, host, port):
        self.stop_event = threading.Event()
        self.client = AsyncTCPClient(host, port)
        self.tcp_thread = threading.Thread(target=self._tcp_loop, name="tcp_loop")

    def start(self):
        self.tcp_thread.start()

    def stop(self):
        self.tcp_thread.join()
        raise asyncore.ExitNow('TCP Server quitting!')

    def get_client(self):
        return self.client

    def _tcp_loop(self):
        try:
            asyncore.loop()
        except asyncore.ExitNow, e:
            print(e)


def main():
    tcp_client_handler = AsyncTCPClientHandler("127.0.0.1", 1111)
    tcp_client_handler.start()
    print('started')
    client = tcp_client_handler.get_client()
    client.append_buffer('d 0 500 500 200\n')
    client.append_buffer('c\n')
    print('command appended')

    # time.sleep(3)
    tcp_client_handler.stop()

    print('exit')


if __name__ == '__main__':
    main()
