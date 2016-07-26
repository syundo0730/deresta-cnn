# -*- coding:utf-8 -*-


class MinitouchCommand:
    def __init__(self, contact, pressure, command='', wait=None):
        self.contact = contact
        self.pressure = pressure
        self.command = command
        self.wait = wait

    def _create_command(self, command, wait=None):
        return MinitouchCommand(
            self.contact,
            self.pressure,
            command,
            wait
        )

    def down(self, position):
        x, y = position
        return self._create_command(
            self.command + 'd {0} {1} {2} {3}\n'.format(self.contact, x, y, self.pressure)
        )

    def up(self):
        return self._create_command(
            self.command + 'u {0}\n'.format(self.contact)
        )

    def move(self, dest):
        x, y = dest
        return self._create_command(
            self.command + 'm {0} {1} {2} {3}\n'.format(self.contact, x, y, self.pressure)
        )

    def commit(self):
        return self._create_command(
            self.command + 'c\n'
        )

    def wait_ms(self, mills):
        return self._create_command(
            self.command,
            mills
        )

    def get_command(self):
        return self.command

    def get_wait(self):
        return self.wait

