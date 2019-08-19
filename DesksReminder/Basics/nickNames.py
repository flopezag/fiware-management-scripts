# -*- coding: utf-8 -*-

from DesksReminder.Basics.nicknamesBook import NickNameBook
from Common.emailer import Emailer

__author__ = 'Manuel Escriche'


class ContactBook:

    def __init__(self):
        # only for testing, the correct one is ->
        self.book = NickNameBook

    def getNickName(self, name):
        _name = name.strip()
        if _name.encode('utf-8') in self.book:
            return self.book[_name.encode('utf-8')]
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

    def check_name(self, name):
        _name = name.strip()
        if _name in self.book:
            return self.book[_name]
        else:
            print("have a look at {} nickname because it wasn't found in the contact book."
                  .format(name))


if __name__ == "__main__":
    tests = ContactBook()
    tests.check_name('Radosław Adamkiewicz')
    tests.check_name('Santiago Martinez García')
    tests.check_name('Miguel Jiménez')

    tests.check_name('MARTEL')
    tests.check_name('José Ignacio Carretero Guarde')
    tests.check_name('Joaquín Iranzo')
    tests.check_name('Atos Spain Tenerife Node Support Team')
    tests.check_name('Britanny Node Support')
    tests.check_name('Álvaro Arranz')
