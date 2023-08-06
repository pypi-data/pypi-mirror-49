# -*- coding: utf-8 -*-

import re
import sys

from ..regex import IPV4, HOSTNAME

import logging
logger = logging.getLogger(__name__)


class Validator(object):
    def __init__(self, pattern):
        self.pattern = pattern
    
    def validate(self, value):
        return re.search(self.pattern, value)


class IPv4Validator(Validator):
    def __init__(self):
        pattern = IPV4
        Validator.__init__(self, pattern)
        

class HostnameValidator(Validator):
    def __init__(self):
        pattern = HOSTNAME
        Validator.__init__(self, pattern)


class DirPathValidator(Validator):
    def __init__(self):
        if sys.platform == 'win32':
            pattern = r'^[a-zA-Z]:\\[ \w\\]*$'
        elif sys.platform.startswith('linux'):
            pattern = r'^(/)?([^/\0]+(/)?)+$'
        else:
            raise ValueError
        Validator.__init__(self, pattern)


def show_table(headers, contents):
    column_sizes = []
    for index, header in enumerate(headers):
        size = len(header)
        for row in contents:
            if len(row[index]) > size:
                size = len(row[index])
        column_sizes.append(size)

    # Line 1, 3 and n: delimiters
    delim_line = "+"
    for size in column_sizes:
        delim_line += "-" * size + "+"
    print(delim_line)

    # Line 2: column names
    name_line = "|"
    for index, header in enumerate(headers):
        name_line += header + " " * (column_sizes[index] - len(header)) + "|"
    print(name_line)

    print(delim_line)

    for content in contents:
        content_line = "|"
        for i in range(len(headers)):
            content_line += content[i] + " " * (column_sizes[i] - len(content[i])) + "|"
        print(content_line)
    print(delim_line)


class InteractiveInput(object):
    @staticmethod
    def message(text, style="DESCRIPTION"):
        if style == "TITLE":
            print("=" * len(text))
            print(text.upper())
            print("=" * len(text))
        elif style == "SECTION":
            print("\n*** %s ***" % text)
        else:
            print("\n%s" % text)

    @staticmethod
    def input(question, default=None, validator=None):
        while True:
            try:
                if default:
                    value = input("\n%s[%s]:" % (question, default))
                else:
                    value = input("\n%s:" % question)
            except KeyboardInterrupt:
                print("\nQuit.")
                sys.exit(0)

            value = value or default
            if not value:
                continue

            if validator:
                if validator.validate(value):
                    pass
                else:
                    print("ERROR! Please try again.\n")
                    continue
            return value

    @staticmethod
    def select(question, choices, default=None):
        while True:
            print("\n%s" % question)
            for index in range(len(choices)):
                optkey = index + 1
                optval = choices[index]
                spacecount = len(str(len(choices))) - len(str(optkey))
                if default and default == optval:
                    line = "  %s%s) [%s]" % (" " * spacecount, " " * len(str(optkey)), optval)
                else:
                    line = "  %s%s) %s" % (" " * spacecount, optkey, optval)
                print(line)
                
            choice = input("Choice:")
            if choice:
                if filter(lambda x: str(x) == choice, range(1, len(choices) + 1)):
                    value = choices[int(choice) - 1]
                else:
                    print("That's not one of the available choices. Please try again\n")
                    continue                    
            else:
                if default and filter(lambda x: x == default, choices):
                    value = default
                else:                    
                    print("That's not one of the available choices. Please try again\n")
                    continue
            return value
