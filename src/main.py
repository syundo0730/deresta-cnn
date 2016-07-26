# -*- coding: utf-8 -*-

import os
from trainer.trainer import Trainer


trainer = Trainer()
trainer.train(10, 1, False)
trainer.test()
