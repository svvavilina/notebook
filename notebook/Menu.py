# coding=utf-8
import json
from Notebook import Notebook
from Serialization import *


class FieldFormatException(Exception):
    """For invalid field values input"""
    pass


class Menu:
    MENU_ITEMS = {0: 'Print all notes',
                  1: 'Add a new note or new phone number to an exist note',
                  2: 'Delete a note',
                  3: 'Find',
                  4: 'Clean the Notebook',
                  5: 'Exit'}

    def __init__(self):
        self.__clean_buffer()
        self.field = ''
        try:
            with open('notebook.json', 'r') as f:
                notes = json.load(f, object_hook=from_json)
                self.notebook = Notebook(notes)
            print '\tToday is b-day:'
            notes = self.notebook.remind
            self.print_notes(notes)
        except IOError:
            self.notebook = Notebook()

    def __clean_buffer(self):
        """Clean the input buffer """
        self.surname = self.name = self.patronymic = self.dob = ''

    def __str__(self):
        str_menu = 'Menu items:\n'
        for item in self.MENU_ITEMS:
            str_menu += '\t%d - %s\n' % (item, self.MENU_ITEMS[item])
        return str_menu

    def _print_notebook(self):
        self.notebook.print_notebook()

    @staticmethod
    def print_notes(notes):
        if len(notes) is not 0:
            for such_note in notes:
                print such_note
        else:
            print 'No notes'

    @staticmethod
    def _add_field(function, field_name):
        """Input and check current field value"""
        value = raw_input('%s:\t' % field_name)
        if value == '':
            value = 'none'
        formatted = function(unicode(value, 'utf-8'))
        if field_name == 'Date of birthday (dd/mm/yyyy)' and value == 'none':
            return formatted
        if formatted is None and not field_name == 'Phone number':
            raise FieldFormatException('The %s' % field_name)
        return formatted

    def _read_note(self):
        """Input and check the block of fields: surname, name, patronymic and dob"""
        print 'Please, input fields'
        if self.surname == '':
            self.surname = self._add_field(is_name, 'Surname')
        if self.name == '':
            self.name = self._add_field(is_name, 'Name')
        if self.patronymic == '':
            self.patronymic = self._add_field(is_name, 'Patronymic')
        if self.surname == 'none' and self.name == 'none':
            if self.patronymic == 'none':
                print '\n\t\tAll full name fields can not be empty\n'
            else:
                print '\n\t\tThe Note can not include only patronymic field\n'
            self.__clean_buffer()
            return False
        if self.dob == '':
            self.dob = self._add_field(is_dob, 'Date of birthday (dd/mm/yyyy)')
        return True

    def _add_note(self):
        """Add a new note"""
        try:
            if not self._read_note():
                return
            print 'Phone number format +7 (___) ___-__-__: xxxxxxxxxx (only 10 digits)'
            number = self._add_field(is_phone_number, 'Phone number')
            full_name = [self.surname, self.name, self.patronymic]
            note = Note(len(self.notebook), full_name, self.dob, number)
            result = self.notebook.add_note(note)
            if result is 0:
                print '\n\t\tThe Note has added\n'
            elif result is 1:
                print '\n\t\tThe Notebook has already contained this phone number of such person\n'
            elif result is 2:
                print '\n\t\tThe phone number has added\n'
            elif result is 3:
                print '\n\t\tThe phone number has not specified\n'
            elif result is 4:
                print '\n\t\tNo information\n'
            self.__clean_buffer()
        except FieldFormatException as e:
            print '%s field contains invalid characters' % e
            self._add_note()

    def _delete_note(self):
        """Delete a specific note """
        try:
            if not self._read_note():
                return
            full_name = [self.surname, self.name, self.patronymic]
            note = Note(len(self.notebook), full_name, self.dob)
            result = self.notebook.delete_note(note)
            if result is 0:
                print '\n\t\tThe Note has deleted\n'
            elif result is 1:
                print '\n\t\tThe Note is not found\n'
            elif result is 2:
                print '\n\t\tThe Notebook is empty\n'
            self.__clean_buffer()
        except FieldFormatException as e:
            print '%s field contains invalid characters' % e
            self._add_note()

    def _find_by_field(self):
        """Find by one of the conditions: surname, name or patronymic"""
        try:
            if self.field == '':
                self.field = raw_input('Input field name (Surname/Name/Patronymic):\t')
                field = Notebook.get_full_name_fields()[self.field]
            value = self._add_field(is_name, 'Field value')
            result = self.notebook.find_note(self.field, unicode(value, 'utf-8').encode('utf-8'))
            self.print_notes(result)
            self.field = ''
        except FieldFormatException as e:
            print '%s field contains invalid characters' % e
            self._find_by_field()
        except KeyError:
            print '\n\t\tInvalid field value\n'
            self.field = ''
            self._find_by_field()

    def _clean(self):
        """Clear out the Notebook"""
        result = self.notebook.clean()
        if result is 0:
            print '\n\t\t\The Notebook has cleaned\n'
        elif result is 1:
            print '\n\t\tThe Notebook is empty\n'

    def _quite(self):
        """Save all notes to the json-file"""
        with open('notebook.json', mode='w') as f:
            json.dump(self.notebook.notes, f, default=to_json, indent=2)
        print '\tGoodbye'

    def _read_item(self):
        """Input and check menu item"""
        try:
            mode = int(raw_input('Item number:\t'))
            if mode is 0:
                self._print_notebook()
            elif mode is 1:
                self._add_note()
            elif mode is 2:
                self._delete_note()
            elif mode is 3:
                self._find_by_field()
            elif mode is 4:
                self._clean()
            elif mode is 5:
                self._quite()
                return False
            else:
                raise ValueError
            return True
        except ValueError:
            print 'Not a menu item'
            return True

    def session(self):
        """Include all session actions"""
        print 'Welcome'
        result = True
        while result:
            print self
            result = self._read_item()

