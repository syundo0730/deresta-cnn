# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np


class LabeledImageFile:

    def __init__(self, file_path, label):
        self.file_path = file_path
        self.label = label
        self.raw_image = None

    def get_image(self):
        if self.raw_image is None:
            self._load()
        return self._to_array()

    def get_label(self):
        return self.label

    def _load(self):
        self.raw_image = Image.open(self.file_path)

    def _to_array(self, color=True):
        image = np.asarray(self.raw_image, dtype=np.float32)
        if image.ndim == 2:
            # don't have color dimension
            image = image[:, :, np.newaxis]
            if color:
                image = np.tile(image, (1, 1, 3))
        elif image.shape[2] == 4:
            # RGB + A format
            image = image[:, :, :3]

        # H x W x K -> K x H x W
        image = image.transpose(2, 0, 1)

        return image
