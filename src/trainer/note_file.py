# -*- coding: utf-8 -*-

import json


class NoteFile:

    def __init__(self, file_path):
        self.file_path = file_path
        self.raw_note_obj = None

    def get_obj(self):
        if self.raw_note_obj is None:
            self._load()
        return self.raw_note_obj

    def _load(self):
        file = open(self.file_path)
        self.raw_note_obj = json.load(file)
        file.close()

