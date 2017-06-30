# -*- coding: utf-8 -*-

import cv2


class VideoFile:

    def __init__(self, file_path):
        print(file_path)
        self.file_path = file_path
        self.capture = cv2.VideoCapture('../../data/scraped_data/video/encoded/song_3001_Master.mp4')
        self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame_count = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.video_length = self.frame_count / self.fps * 1000

    # def __del__(self):
        # self.capture.release()
        # cv2.destroyAllWindows()

    def get_video_size(self):
        return self.width, self.height
    
    def get_fps(self):
        return self.fps

    def get_frame_pos_in_time_ms(self, time_ms):
        return int(self.fps * time_ms * 0.001)

    def get_frames_by_time_ms_in_range(self, time_ms, frame_num):
        frame_index = int(self.fps * time_ms * 0.001)
        return [
            self.get_frame_by_frame_pos(frame_pos)
            for frame_pos
            in range(frame_index - frame_num/2, frame_index + frame_num/2 + 1)
            ]

    def get_frame_by_time_ms(self, time_ms):
        if not self.capture.isOpened():
            return None
        if time_ms < 0 or time_ms >= self.video_length:
            return None
        self.capture.set(cv2.CAP_PROP_POS_MSEC, time_ms)
        ret, frame = self.capture.read()
        if not ret:
            return None
        return frame

    def get_frame_by_frame_pos(self, frame_pos):
        if not self.capture.isOpened():
            print('capture is not opened!!!!!!!!!!')
            return None
        if frame_pos < 0 or frame_pos >= self.frame_count:
            print('{0} out of range!!!!!!!!'.format(frame_pos))
            return None
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        ret, frame = self.capture.read()
        if not ret:
            print('{0} no response!!!!!!!!'.format(frame_pos))
            return None
        return frame
