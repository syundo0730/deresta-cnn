# -*- coding: utf-8 -*-

import cv2
import pickle
import json
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
            for resource in song_item['resources']:
                file_name = resource['file_name']
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
            labels = note['labels']
            for f in range(pos - frame_num/2, pos + frame_num/2 + 1):
                frame = video_file.get_frame(f)
                image_file_name = "{0}/{1}_{2}.png".format(self.image_root, file_name, f)
                labeled_image_file = LabeledImageFile(image_file_name, labels)
                # 画像を保存しておく
                resized_img = cv2.resize(frame, (227, 227))
                cv2.imwrite(image_file_name, resized_img)
                labeled_images.append(labeled_image_file)

        return labeled_images

