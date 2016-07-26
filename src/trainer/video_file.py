# -*- coding: utf-8 -*-

import cv2
import numpy as np


class VideoFile:

    def __init__(self, file_path):
        self.file_path = file_path
        self.capture = cv2.VideoCapture(file_path)
        self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame_count = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)

    # def __del__(self):
        # self.capture.release()
        # cv2.destroyAllWindows()

    def get_video_size(self):
        return self.width, self.height
    
    def get_fps(self):
        return self.fps
    
    def get_frame(self, frame_pos):
        if not self.capture.isOpened():
            return None
        if frame_pos < 0 or frame_pos >= self.frame_count:
            return None
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        ret, frame = self.capture.read()
        if not ret:
            return None
        return frame
