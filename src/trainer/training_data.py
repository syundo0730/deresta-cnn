# -*- coding: utf-8 -*-

from labeled_image_maker import LabeledImageFileMaker
import numpy as np
import os


def label_to_output(label, label_types):
    label_index = label_types.index(label)
    return np.asarray([label_index], dtype=np.int32)


class TrainingData:

    def __init__(self, image_root, note_image_root, video_root, song_list_path):
        self.labeled_image_file_maker = LabeledImageFileMaker(image_root, note_image_root, video_root, song_list_path)
        self.labeled_images = None
        self.mean_image = None

    def release(self):
        self.labeled_images = None

    def make_mean_image(self):
        labeled_images = self.get_labeled_images()
        sum_image = None
        for labeled_image_file in labeled_images:
            image = labeled_image_file.get_image()
            if sum_image is None:
                sum_image = np.ndarray(image.shape)
                sum_image[:] = image
            else:
                sum_image += image

        self.mean_image = sum_image / len(labeled_images)

    def get_mean_image(self):
        if self.mean_image is None:
            self.make_mean_image()
        return self.mean_image

    def get_labeled_images(self):
        if self.labeled_images is None:
            self._load_labeled_images()
        return self.labeled_images

    def get_train_data(self, label_types):
        labeled_images = self.get_labeled_images()
        x_train_all = np.asarray(map(
            lambda labeled_image_file: labeled_image_file.get_image(),
            labeled_images
        ))
        y_train_all = np.asarray(map(
            lambda labeled_image_file: label_to_output(labeled_image_file.get_label(), label_types),
            labeled_images
        ))
        length = len(labeled_images)

        # 元データをランダムに並べ替える
        indexes = np.random.permutation(length)
        x_train_all_rand = x_train_all[indexes]
        y_train_all_rand = y_train_all[indexes]

        # 平均画像を引く
        mean = self.get_mean_image()
        if mean is not None:
            x_train_all_rand -= mean
        # 正規化
        x_train_all /= 255

        # 1/5はテストに使う
        data_size = length * 4 / 5
        x_train, x_test = np.split(x_train_all_rand, [data_size])
        y_train, y_test = np.split(y_train_all_rand, [data_size])

        return x_train, x_test, y_train, y_test

    def _load_labeled_images(self):
        # もしファイルが存在していたら読み込む
        self.labeled_images = self.labeled_image_file_maker.load_all_songs()


