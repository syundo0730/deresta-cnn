# -*- coding: utf-8 -*-
import json
from os import walk
import codecs


def get_label_name(type, status, prev_note_id, next_note_id):
    if status == 1:
        return 'left'
    elif status == 2:
        return 'right'

    if type == 1:
        return 'tap'
    elif type == 2:
        if prev_note_id != 0:
            return 'up'
        elif next_note_id != 0:
            return 'down'

    return 'none'


def convert_note_item(note_item):
    type = note_item['type']
    status = note_item['status']
    prev_note_id = note_item['prevNoteId']
    next_note_id = note_item['nextNoteId']
    label = get_label_name(type, status, prev_note_id, next_note_id)

    return {
        'time': note_item['timing'] * 1000,  # sec からmsecに変換する
        'label': label,
        'pos': note_item['endPos'] - 1  # 右からindex 1始まりなので、左から0始まりにする
    }


def convert_note_obj(original_json_obj):
    metadata = original_json_obj['metadata']
    title = metadata['songName']
    file_name = metadata['songFile']
    duration = metadata['duration']
    difficulty = metadata['difficultyName']
    bpm = metadata['bpm']
    notes = original_json_obj['notes']
    notes = [convert_note_item(note) for note in notes]

    return {
        'title': title,
        'file_name': file_name + '_' + difficulty,
        'difficulty': difficulty,
        'bpm': bpm,
        'duration': duration,
        'notes': notes
    }


class NoteFileConverter:
    def __init__(self, note_src_root, note_dst_root):
        self.note_src_root = note_src_root
        self.note_dst_root = note_dst_root

    def convert_all(self):
        files = []
        src = self.note_src_root
        dst = self.note_dst_root
        for (dirpath, dirnames, filenames) in walk(src):
            filenames = [dirpath + '/' + name for name in filenames]
            files.extend(filenames)

        song_list = []
        for file_name in files:
            with codecs.open(file_name, 'r', 'utf-8') as file:
                note_obj = json.load(file)
                converted_note_obj = convert_note_obj(note_obj)
            out_file_name = dst + '/note/' + converted_note_obj['file_name'] + '.json'
            with codecs.open(out_file_name, 'w', 'utf-8') as outfile:
                json.dump(converted_note_obj, outfile, ensure_ascii=False, sort_keys=True, indent=4)
            song_list.append({
                'title': converted_note_obj['title'],
                'file_name': converted_note_obj['file_name'],
                'difficulty': converted_note_obj['difficulty']
            })
        with codecs.open(dst + '/song_list.json', 'w', 'utf-8') as outfile:
            json.dump(song_list, outfile, ensure_ascii=False, sort_keys=True, indent=4)


def main():
    converter = NoteFileConverter('../../data/note_data', '../../data/scraped_data')
    converter.convert_all()

if __name__ == '__main__':
    main()
