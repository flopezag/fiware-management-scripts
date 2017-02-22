# -*- coding: utf-8 -*-

__author__ = 'Manuel Escriche'

from nicknamesBook import NickNameBook
from Basics.emailer import Emailer


class ContactBook:

    def __init__(self):
        # only for testing, the correct one is ->
        self.book = NickNameBook

    def getNickName(self, name):
        _name = name.strip()
        if _name in self.book:
            return self.book[_name]
        else:
            emailer = Emailer()
            message = 'Dear Reminders Admin,' + \
                "\n\nPlease, have a look at {} nickname because it wasn't found in the contact book."\
                    .format(name.encode('utf-8')) + \
                '\n\nThanks in advance for cooperation!!' + \
                '\n\nKind Regards,' + \
                '\nFernando'
            emailer.send_adm_msg('Unknown Nickname for {}'.format(name.encode('utf-8')), message)
            return _name

if __name__ == "__main__":
    pass
