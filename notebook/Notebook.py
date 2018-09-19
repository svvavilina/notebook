from datetime import datetime
from Note import Note


class Notebook:
    """Describes the functional of a notebook"""

    def __init__(self, init_notes=None):
        self.notes = init_notes

    def __len__(self):
        """Count of notes in the notebook"""
        if self.notes is None:
            return 0
        return len(self.notes)

    @staticmethod
    def get_full_name_fields():
        return {'Surname': 0, 'Name': 1, 'Patronymic': 2}

    def _get_the_same(self, new_note):
        if self.notes is None or len(self.notes) is 0:
            return None
        for note in self.notes:
            if new_note == note:
                return note
        return None

    def add_note(self, new_note):
        # type: (Note) -> int
        """Add the note to the notebook
        Result:
        0 - added
        1 - the notebook has already contained this phone number of such person
        2 - the phone number has added
        3 - phone number hasn't specified
        4 - no information"""
        if new_note is None:
            return 4
        note = self._get_the_same(new_note)
        if note is None:
            try:
                self.notes.add(new_note)
            except AttributeError:
                self.notes = {new_note}
            return 0
        try:
            note.phone_number.index(new_note.phone_number[0])
            return 1
        except ValueError:
            note.phone_number.append(new_note.phone_number[0])
            return 2
        except TypeError:
            return 3
        except AttributeError:
            if new_note.phone_number is not None:
                note.phone_number = [new_note.phone_number[0]]
            else:
                return 3
            return 2

    def find_note(self, field, value):
        # type: (str, str) -> list
        """Return lists of notes which full_name field contains a field with such value
        or
        an empty list if full_name does not contain a field or a field with such value"""
        notes_list = []
        if self.notes is None or len(self.notes) is 0:
            return notes_list
        try:
            field_numb = Notebook.get_full_name_fields()[field]
        except KeyError:
            return notes_list
        for note in self.notes:
            if note.full_name[field_numb] == value:
                notes_list.append(note)
        return notes_list

    def delete_note(self, delete_note):
        # type: (Note) -> int
        """Delete the note from the notebook
        Result:
        0 - deleted
        1 - not found
        2 - the Notebook is empty"""
        if self.notes is None or len(self.notes) is 0:
            return 2
        try:
            note = self._get_the_same(delete_note)
            self.notes.remove(note)
            return 0
        except KeyError:
            return 1

    def clean(self):
        # type: () -> int
        """Delete all notes from the Notebook.
        Result:
        0 - Cleaned
        1 - the Notebook has already cleaned"""
        self.notes.clear()
        return 0

    def print_notebook(self):
        if self.notes is None or len(self.notes) is 0:
            print '\n\t\tThe Notebook is empty\n'
            return
        for note in self.notes:
            print note

    @property
    def remind(self):
        # type: () -> list
        """Checks if someone has a b-day today"""
        notes_list = []
        if self.notes is None or len(self.notes) is 0:
            return notes_list
        for note in self.notes:
            if note.dob is not None and datetime.today().strftime('%d%m') == note.dob.strftime('%d%m'):
                notes_list.append(note)
        return notes_list
