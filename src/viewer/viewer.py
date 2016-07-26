# -*- coding: utf-8 -*-

import cv2
import numpy as np
from video_loader import VideoLoader
from note_evaluator import NoteEvaluator, NoteLoader


def get_position(width, height, pos):
    w_center = width * 0.5
    interval = width / 6.5
    pos_x_1 = int(w_center - interval * 2)
    pos_x_2 = int(w_center - interval)
    pos_x_3 = int(w_center)
    pos_x_4 = int(w_center + interval)
    pos_x_5 = int(w_center + interval * 2)
    pos_y = int(height - height / 6.0)

    positions = [
        (pos_x_1, pos_y),
        (pos_x_2, pos_y),
        (pos_x_3, pos_y),
        (pos_x_4, pos_y),
        (pos_x_5, pos_y),
    ]

    return positions[pos]


def draw_command(frame, pos, command):
    # BGR
    blue = (255, 0, 0)
    red = (0, 0, 255)
    yellow = (0, 255, 255)
    if command == 'tap':
        cv2.circle(frame, pos, 40, yellow, 3, 4)
    if command == 'up':
        cv2.circle(frame, pos, 40, red, 3, 4)
    if command == 'down':
        cv2.circle(frame, pos, 40, blue, 3, 4)
    if command == 'left':
        cv2.fillConvexPoly(
            frame,
            np.array([[pos[0]-30, pos[1]], [pos[0]+30, pos[1]+30], [pos[0]+30, pos[1]-30]]),
            yellow)
    if command == 'right':
        cv2.fillConvexPoly(
            frame,
            np.array([[pos[0]+30, pos[1]], [pos[0]-30, pos[1]-30], [pos[0]-30, pos[1]+30]]),
            yellow)


class GameViewer:
    def __init__(self, video_file_name, note_file_name):
        self.video_loader = VideoLoader(video_file_name)
        self.w, self.h = self.video_loader.get_size()
        note_loader = NoteLoader(note_file_name)
        notes = note_loader.get_note_list()
        self.note_evaluator = NoteEvaluator(notes)

    def __del__(self):
        self.frame = None

    def start(self):
        while True:
            frame, time = self.video_loader.read()
            if frame is None:
                break
            time = time + 1400
            # self.note_evaluator.update(time)
            self.show(frame, time)
            k = cv2.waitKey(100)
            if k == 27:
                break

    def show(self, frame, time):
        note_list = self.note_evaluator.get_hit_note_list(time, 100)
        for note in note_list:
            pos = get_position(self.w, self.h, note.pos)
            draw_command(frame, pos, note.label)
        cv2.imshow('capture', frame)
