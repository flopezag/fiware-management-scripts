# -*- coding: utf-8 -*-

from DesksReminder.Basics.nicknamesBook import NickNameBook
from Common.emailer import Emailer

__author__ = 'Manuel Escriche'


class ContactBook:

    def __init__(self):
        # only for testing, the correct one is ->
        self.book = NickNameBook
        self.emailer = Emailer()

    def getNickName(self, name):
        _name = name.strip()
        if _name in self.book:
            return self.book[_name]
        elif isinstance(_name, bytes) and _name.decode("utf-8") in self.book:
            return self.book[_name.decode("utf-8")]
        else:
            message = 'Dear Reminders\' Admin,' + \
                "\n\nPlease, have a look at {} nickname because it wasn't found in the contact book."\
                .format(name.encode('utf-8')) + \
                '\n\nThanks in advance for cooperation!!' + \
                '\n\nKind Regards,' + \
                '\nFernando'
            self.emailer.send_adm_msg('Unknown Nickname for {}'.format(name.encode('utf-8')), message)
            return _name

    def check_name(self, name):
        _name = name.strip()
        if _name in self.book:
            return self.book[_name]
        elif isinstance(_name, bytes) and _name.decode("utf-8") in self.book:
            return self.book[_name.decode("utf-8")]
        else:
            print("have a look at {} nickname because it wasn't found in the contact book."
                  .format(name))


if __name__ == "__main__":
    tests = ContactBook()
    print(tests.check_name('Foo Foo'))
    print(tests.check_name(b'Foo Foo'))

