# -*- coding:utf-8 -*-
from minitouch_command import MinitouchCommand


class CommandFactory:
    def __init__(self, contact, pressure, sequence=[]):
        self.contact = contact
        self.pressure = pressure
        self.sequence = sequence

    def down_sequence(self, position):
        return [
            MinitouchCommand(self.contact, self.pressure).down(position).commit()
        ]

    def up_sequence(self):
        return [
            MinitouchCommand(self.contact, self.pressure).up().commit()
        ]

    def swipe_up_sequence(self, start, end, tick_ms, inter_num):
        inter_pos = []
        s_x, s_y = start
        e_x, e_y = end
        for i in range(inter_num):
            diff_x = (e_x - s_x) / (inter_num + 1)
            diff_y = (e_y - s_y) / (inter_num + 1)
            inter_pos = inter_pos + [(s_x + diff_x * (i+1), s_y + diff_y * (i+1))]
        return [
                   MinitouchCommand(self.contact, self.pressure).move(p).commit().wait_ms(tick_ms) for p in inter_pos
                   ] + [
            MinitouchCommand(self.contact, self.pressure).move(end).commit().wait_ms(tick_ms),
            MinitouchCommand(self.contact, self.pressure).up().commit()
        ]

    def tap_sequence(self, position):
        return [
            MinitouchCommand(self.contact, self.pressure).down(position).commit().wait_ms(100),
            MinitouchCommand(self.contact, self.pressure).up().commit()
        ]

    def swipe_sequence(self, start, end, tick_ms, inter_num):
        return [
                   MinitouchCommand(self.contact, self.pressure).down(start).commit().wait_ms(tick_ms)
               ] + self.swipe_up_sequence(start, end, tick_ms, inter_num)
