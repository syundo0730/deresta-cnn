# -*- coding:utf-8 -*-
from command_factory import CommandFactory


class DereStageCommandFactory(CommandFactory):
    def __init__(self, contact, pressure, base_position):
        self.contact = contact
        self.pressure = pressure
        self.base_position = base_position
        CommandFactory.__init__(self, contact, pressure)

    def swipe_diff(self, direction):
        if direction == 'right':
            return 100
        elif direction == 'left':
            return -100
        else:
            return 0

    def swipe_to_sequence(self, direction):
        s_x, s_y = self.base_position
        end = (s_x + self.swipe_diff(direction), s_y)
        return self.swipe_sequence(self.base_position, end, 10, 2)

    def swipe_up_to_sequence(self, direction):
        s_x, s_y = self.base_position
        end = (s_x + self.swipe_diff(direction), s_y)
        return self.swipe_up_sequence(self.base_position, end, 10, 2)

    def down_sequence(self):
        return CommandFactory.down_sequence(self, self.base_position)

    def tap_sequence(self):
        return CommandFactory.tap_sequence(self, self.base_position)
