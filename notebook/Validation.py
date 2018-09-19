# coding=utf-8
from datetime import datetime
import re

PATTERN_NAME = re.compile(ur'^[\s]*[а-яА-ЯёЁa-zA-Z]+[\s]*$')
PATTERN_STR_NAME = re.compile(ur'[а-яА-ЯёЁa-zA-Z]+')
PATTERN_NUMBER = r'^[\s]*[\d]{10}[\s]*$'
PATTERN_STR_NUMB = r'[\d]{10}'
DATE_FORM = "%d/%m/%Y"


def is_dob(str_dob):
    """Date format is 'dd/mm/yyyy' only"""
    try:
        date = datetime.strptime(str_dob, DATE_FORM)
        if datetime.today() < date:
            raise ValueError
        return date
    except ValueError:
        return None


def is_phone_number(str_number):
    """Phone number format is 'xxxxxxxxxx' only"""
    if len(re.findall(PATTERN_NUMBER, str_number)) is 1:
        return [str_to_pattern(PATTERN_STR_NUMB, str_number)[0]]
    return None


def pattern(string):
    return not len(re.findall(PATTERN_NAME, string)) is 0


def str_to_pattern(current_pattern, current_str):
    return re.findall(current_pattern, current_str)


def is_name(str_name):
    """Full name must contain only alphabet characters"""
    if pattern(str_name):
        return str_to_pattern(PATTERN_STR_NAME, str_name)[0].encode('utf-8')
    return None
