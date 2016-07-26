# -*- coding: utf-8 -*-
import json
import codecs


class Note:
    def __init__(self, label, pos, time):
        self.label = label
        self.pos = pos
        self.time = time


class NoteLoader:
    # NoteFileと同じことをやっているんじゃないか?
    # DDDふうにするといいかもしれない
    def __init__(self, note_file_name):
        with codecs.open(note_file_name, 'r', 'utf-8') as file:
            note_obj = json.load(file)
        self.title = note_obj['title']
        self.difficulty = note_obj['difficulty']
        self.bpm = note_obj['bpm']
        self.duration = note_obj['duration']
        self.notes = [Note(note['label'], note['pos'], note['time']) for note in note_obj['notes']]

    def get_note_list(self):
        return self.notes

    def get_note(self, index):
        note_len = len(self.notes)
        if 0 < index < note_len:
            return self.notes[index]
        else:
            return None


class NoteEvaluator:
    def __init__(self, notes):
        self.notes = notes
        self.notes_len = len(notes)
        self.base_index = 0

    def update(self, time):
        while True:
            if self.base_index == self.notes_len - 1:
                return False
            elif time > (self.notes[self.base_index].time + self.notes[self.base_index+1].time) * 0.5:
                self.base_index += 1
            else:
                break

    def get_note(self, index):
        if 0 < index < self.notes_len:
            return self.notes[index]
        else:
            return None

    def get_hit_note_list(self, time, margin):
        hit_note_list = []
        for note in self.notes:
            note_time = note.time
            if time - margin < note_time < time + margin:
                hit_note_list.append(note)
        return hit_note_list

    def get_hit_note_old(self, time, margin):
        hit_note_list = []
        index = self.base_index
        while True:
            note = self.get_note(index)
            if note is None:
                break
            note_time = note.time
            if note_time < time - margin:
                break
            hit_note_list.append(note.label)
            index = index - 1

        index = self.base_index
        while True:
            note = self.get_note(index)
            if note is None:
                break
            note_time = note.time
            if note_time > time + margin:
                break
            hit_note_list.append(note.label)
            index = index + 1

        return hit_note_list
