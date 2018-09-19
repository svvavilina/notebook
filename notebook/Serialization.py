from Note import Note
from Validation import *


def to_json(python_object):
    if isinstance(python_object, set):
        note_list = []
        for note in python_object:
            note_list.append(note.get_json())
        return {'__class__': 'notes',
                '__value__': note_list}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object:
        if json_object['__class__'] == 'notes':
            note_list = []
            for str_note in json_object['__value__']:
                full_name = [str_note['full_name'][0].encode('utf-8'), str_note['full_name'][1].encode('utf-8'),
                             str_note['full_name'][2].encode('utf-8')]
                numbers = str_note['phone_number']
                if numbers[0] == 'none':
                    numbers = None
                note = Note(str_note['__id'], full_name, is_dob(str_note['dob']), numbers)
                note_list.append(note)
            return set(note_list)
    return json_object
