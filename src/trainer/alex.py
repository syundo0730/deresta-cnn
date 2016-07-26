# -*- coding: utf-8 -*-

import chainer
import chainer.functions as F
import chainer.links as L


class Alex(chainer.Chain):

    """Single-GPU AlexNet without partition toward the channel axis."""

    insize = 227

    def __init__(self, output_size):
        super(Alex, self).__init__(
            conv1=L.Convolution2D(3, 96, 11, stride=4), # (227 - 11)/4 + 1 = 55
            conv2=L.Convolution2D(96, 256, 5, pad=2), # (27 + 2*2 - 5)/1 + 1 = 27
            conv3=L.Convolution2D(256, 384, 3, pad=1), # (13 + 1*2 - 3)/1 + 1 = 13
            conv4=L.Convolution2D(384, 384, 3, pad=1), # (13 + 1*2 - 3)/1 + 1 = 13
            conv5=L.Convolution2D(384, 256, 3, pad=1), # (13 + 1*2 - 3)/1 + 1 = 13
            # output of pool5: 6*6*256 = 9216
            fc6=L.Linear(9216, 4096),
            fc7=L.Linear(4096, 4096),
            fc8=L.Linear(4096, 1024),
            fc9=L.Linear(1024, output_size)
        )
        self.train = True
        self.output_size = output_size

    def __call__(self, x, t):
        y = self.forward(x)
        self.loss = F.sigmoid_cross_entropy(y, t)
        return self.loss

    def forward(self, x):
        pool1 = lambda x: F.max_pooling_2d(F.relu(F.local_response_normalization(x)), 3, stride=2) # (55 - 3)/2 + 1 = 27
        pool2 = lambda x: F.max_pooling_2d(F.relu(F.local_response_normalization(x)), 3, stride=2) # (27 - 3)/2 + 1 = 13
        pool5 = lambda x: F.max_pooling_2d(F.relu(x), 3, stride=2) # (13 - 3)

        h = pool1(self.conv1(x))
        h = pool2(self.conv2(h))
        h = F.relu(self.conv3(h))
        h = F.relu(self.conv4(h))
        h = pool5(self.conv5(h))
        h = F.dropout(F.relu(self.fc6(h)), train=self.train)
        h = F.dropout(F.relu(self.fc7(h)), train=self.train)
        h = F.dropout(F.sigmoid(self.fc8(h)), train=self.train)
        y = self.fc9(h)

        return y
