# -*- coding: utf-8 -*-

import os
from training_data import TrainingData
from alex import Alex
import chainer
from chainer import cuda
from chainer import optimizers
from chainer import serializers
import numpy as np


IMAGE_ROOT = os.path.join(os.path.dirname(__file__), '../../data/training_data/image')
NOTE_ROOT = os.path.join(os.path.dirname(__file__), '../../data/scraped_data/note')
VIDEO_ROOT = os.path.join(os.path.dirname(__file__), '../../data/scraped_data/video/raw')
SONG_LIST_PATH = os.path.join(os.path.dirname(__file__), '../../data/scraped_data/song_list.json')

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../data/training_data/chainer_alex.model')


class Trainer:

    def __init__(self):
        self.model = None
        self.batch_size = 0
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None

    def train(self, epoch=10, batch_size=32, gpu=False):
        if gpu:
            cuda.check_cuda_available()
        xp = cuda.cupy if gpu else np

        self.batch_size = batch_size

        label_types = ['none', 'tap', 'up', 'down', 'right', 'left']

        self.model = Alex(len(label_types))
        optimizer = optimizers.MomentumSGD(lr=0.01, momentum=0.9)
        optimizer.setup(self.model)

        if gpu:
            self.model.to_gpu()

        training_data = TrainingData(IMAGE_ROOT, NOTE_ROOT, VIDEO_ROOT, SONG_LIST_PATH)
        self.x_train, self.x_test, self.y_train, self.y_test = training_data.get_train_data(label_types)
        data_size = self.x_train.shape[0]

        for ep in range(epoch):
            print('epoch {0}/{1}: (learning rate={2})'.format(ep + 1, epoch, optimizer.lr))
            indexes = np.random.permutation(data_size)
            for i in range(0, data_size, self.batch_size):
                x_batch = self.x_train[indexes[i:i + self.batch_size]]
                y_batch = self.y_train[indexes[i:i + self.batch_size]]
                x = chainer.Variable(x_batch)
                t = chainer.Variable(y_batch)
                optimizer.update(self.model, x, t)
                print("loss: {0}".format(self.model.loss.data))

            serializers.save_npz(MODEL_PATH, self.model)
            optimizer.lr *= 0.97

    def test(self):
        print('Test started')
        test_data_size = self.x_test.shape[0]
        sum_loss = 0
        for i in range(0, test_data_size, self.batch_size):
            x = chainer.Variable(self.x_test[i:i + self.batch_size])
            t = chainer.Variable(self.y_test[i:i + self.batch_size])
            loss = self.model(x, t)
            sum_loss += loss.data * self.batch_size
            print(self.model.forward(x).data)

        print('mean loss: {0}'.format(sum_loss / test_data_size))


def main():
    training_data = TrainingData(IMAGE_ROOT, NOTE_ROOT, VIDEO_ROOT, SONG_LIST_PATH)
    x_train, x_test, y_train, y_test = training_data.get_train_data(['none', 'tap', 'up', 'down', 'right', 'left'])

if __name__ == '__main__':
    main()