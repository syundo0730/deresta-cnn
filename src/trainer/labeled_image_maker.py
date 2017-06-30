# -*- coding: utf-8 -*-

import cv2
import pickle
import json
import numpy as np
from labeled_image_file import LabeledImageFile
from video_file import VideoFile
from note_file import NoteFile


class LabeledImageFileMaker:

    def __init__(self, image_root, note_image_root, video_root, song_list_path):
        self.image_root = image_root
        self.note_image_root = note_image_root
        self.video_root = video_root
        self.song_list_path = song_list_path

    def load_all_songs(self):
        file = open(self.song_list_path)
        song_list_obj = json.load(file)
        file.close()
        labeled_images = []
        for song_item in song_list_obj:
            file_name = song_item['file_name']
            video_file = VideoFile('{0}/{1}.mp4'.format(self.video_root, file_name))
            note_file = NoteFile('{0}/{1}.json'.format(self.note_image_root, file_name))
            labeled_image_list = self._save_labeled_images(file_name, video_file, note_file)
            labeled_images.extend(labeled_image_list)

        return labeled_images

    def make_labeled_image_list(self, file_path, labeled_images):
        with open(file_path, 'wb') as f:
            pickle.dump(labeled_images, f)

    def _save_labeled_images(self, file_name, video_file, note_file):
        notes = note_file.get_obj()['notes']
        frame_num = 3
        labeled_images = []
        for note in notes:
            pos = note['pos']
            label = note['label']
            time_ms = note['time']
            frame_index = video_file.get_frame_pos_in_time_ms(time_ms)
            image_file_name = "{0}/{1}_{2}.png".format(self.image_root, file_name, frame_index)
            labeled_image_file = LabeledImageFile(image_file_name, label)
            labeled_images.append(labeled_image_file)

            # 画像を保存しておく
            frame = self._get_multi_frame_image(video_file, frame_index)
            cv2.imwrite(image_file_name, frame)

        return labeled_images

    def _get_multi_frame_image(self, video_file, frame_pos):
        return video_file.get_frame_by_frame_pos(frame_pos)

        himg = None
        vimg = None
        for i in range(4):
            frame = video_file.get_frame_by_frame_pos(frame_pos-3+i)
            if frame is None:
                resized_img = np.tile(np.uint8([127]), (227, 227, 1))
            else:
                resized_img = cv2.resize(frame, (227, 227))

            if himg is None:
                himg = resized_img
            else:
                himg = cv2.hconcat([himg, resized_img])
                if vimg is None:
                    vimg = himg.copy()
                else:
                    himg_copy = himg.copy()
                    vimg = cv2.vconcat([vimg, himg_copy])
                himg = None

        return vimg
