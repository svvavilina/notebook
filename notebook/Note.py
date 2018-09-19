class Note:
    """Describe every note in a notebook"""
    _JSON_DATE_FORM = "%d/%m/%Y"
    _DISPLAY_DATE_FORM = "%d %B %Y"

    def __init__(self, note_id, full_name, dob=None, phone_number=None):
        self.__id = note_id
        self.full_name = full_name
        self.dob = dob
        self.phone_number = phone_number

    def __hash__(self):
        return self.__id

    def __eq__(self, other):
        """Notes are equals if their full_name fields are the same"""
        if len(set(self.full_name) - set(other.full_name)) is 0 and self.dob == other.dob:
            return True
        return False

    def __str__(self):
        numbers = self.__phone_str
        str_numbers = '\n'.join(numbers).encode('utf-8')
        return 'Surname: %s\nName: %s\nPatronymic: %s\nBirthday: %s\n' \
               'Phone number: %s\n' % (self.full_name[0], self.full_name[1], self.full_name[2],
                                       self.__date_str, str_numbers)

    def get_json(self):
        try:
            date = self.dob.strftime(self._JSON_DATE_FORM)
        except (ValueError, AttributeError):
            date = 'none'
        if self.phone_number is None:
            self.phone_number = ['none']
        return dict(__id=self._Note__id, full_name=self.full_name, dob=date, phone_number=self.phone_number)

    @property
    def __date_str(self):
        """Get date in a usable format"""
        if self.dob is None:
            return 'not specified'
        return self.dob.strftime(self._DISPLAY_DATE_FORM)

    @property
    def __phone_str(self):
        """Get phone numbers in a usable format"""
        if self.phone_number is None:
            yield 'not specified'
        else:
            for number in self.phone_number:
                yield '+7 (%s) %s-%s-%s' % (number[:3], number[3:6], number[6:8], number[8:])
