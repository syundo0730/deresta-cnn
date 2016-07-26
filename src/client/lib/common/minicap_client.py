# -*- coding:utf-8 -*-
import signal
import cv2
import numpy as np
from PIL import Image
import io
import time
import asyncore

from tcp_client_worker import TCPClientWorker
from async_tcp_client import AsyncTCPClient


class MinicapClient:
    def __init__(self):
        self.readBannerBytes = 0
        self.bannerLength = 2
        self.readFrameBytes = 0
        self.frameBodyLength = 0
        self.frameBody = bytearray([])
        self.banner = {
            "version": 0,
            "length": 0,
            "pid": 0,
            "realWidth": 0,
            "realHeight": 0,
            "virtualWidth": 0,
            "virtualHeight": 0,
            "orientation": 0,
            "quirks": 0
        }
        self.output = []

        self.tcp_client = AsyncTCPClient("127.0.0.1", 1313)
        self.tcp_client.set_on_receive_listener(self.on_receive)
        self.tcp_client_worker = TCPClientWorker(self.tcp_client)
        self.tcp_client_worker.start()

    def __del__(self):
        self.stop()

    def stop(self):
        print ('stopped!!!')
        self.tcp_client_worker.stop()

    def on_receive(self, data):
        chunk = bytearray(data)
        cursor = 0
        length = len(chunk)
        while cursor < length:
            if self.readBannerBytes < self.bannerLength:
                if self.readBannerBytes == 0:
                    self.banner["version"] = chunk[cursor]
                elif self.readBannerBytes == 1:
                    self.banner["length"] = self.bannerLength = chunk[cursor]
                elif self.readBannerBytes in [2, 3, 4, 5]:
                    self.banner["pid"] += (chunk[cursor] << ((self.readBannerBytes - 2) * 8))
                elif self.readBannerBytes in [6, 7, 8, 9]:
                    self.banner["realWidth"] += (chunk[cursor] << ((self.readBannerBytes - 6) * 8))
                elif self.readBannerBytes in [10, 11, 12, 13]:
                    self.banner["realHeight"] += (chunk[cursor] << ((self.readBannerBytes - 10) * 8))
                elif self.readBannerBytes in [14, 15, 16, 17]:
                    self.banner["virtualWidth"] += (chunk[cursor] << ((self.readBannerBytes - 14) * 8))
                elif self.readBannerBytes in [18, 19, 20, 21]:
                    self.banner["virtualHeight"] += (chunk[cursor] << ((self.readBannerBytes - 18) * 8))
                elif self.readBannerBytes == 22:
                    self.banner["orientation"] += chunk[cursor] * 90
                elif self.readBannerBytes == 23:
                    self.banner["quirks"] = chunk[cursor]

                cursor += 1
                self.readBannerBytes += 1

            elif self.readFrameBytes < 4:
                self.frameBodyLength += (chunk[cursor] << (self.readFrameBytes * 8))
                cursor += 1
                self.readFrameBytes += 1
            else:
                if (length - cursor) >= self.frameBodyLength:
                    self.frameBody.extend(chunk[cursor : cursor + self.frameBodyLength])
                    if self.frameBody[0] != 0xFF or self.frameBody[1] != 0xD8:
                        print("Error: frame body does not start with JPG header")
                        break

                    cv_image = np.asarray(Image.open(io.BytesIO(self.frameBody)))
                    self.output = cv_image[:, :, ::-1].copy()

                    cursor += self.frameBodyLength
                    self.frameBodyLength = 0
                    self.readFrameBytes = 0
                    self.frameBody = bytearray([])

                else:
                    self.frameBody.extend(chunk[cursor : length])
                    self.frameBodyLength -= (length - cursor)
                    self.readFrameBytes += (length - cursor)
                    cursor = length


def main():
    client = MinicapClient()
    print("HUGA")

    running = True

    def on_stop(signal, handler):
        running = False

    # signal.signal(signal.SIGTERM, on_stop)
    # signal.signal(signal.SIGINT, on_stop)

    while running:
        if len(client.output) > 0:
            cv2.imshow('capture', client.output)
        k = cv2.waitKey(1)
        if k == 27:
            print("STOPPPPPPPPPPP")
            client.stop()
            break

    print("HGGG")
    # signal.pause()

if __name__ == '__main__':
    main()
