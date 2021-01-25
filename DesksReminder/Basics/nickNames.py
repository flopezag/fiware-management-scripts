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
    print(tests.check_name('Radosław Adamkiewicz'))

    '''
    b'Charlotte Kotterman'
    b'Juanjo Hierro'
    b'Stefano De Panfilis'
    b'Andrea Kather'
    b'Ulrich Ahle'
    b'Francisco de la Vega'
    b'Jason Fox'
    b'Angeles Tejado'
    b'Phuong Quy Le'
    b'\xc3\x81lvaro Arranz'
    b'Poznan Node Helpdesk'
    b'Alvaro Alonso'
    b'Ferm\xc3\xadn Gal\xc3\xa1n'
    b'Roberto Castillo'
    b'Andres Mu\xc3\xb1oz'
    b'Alberto Abella'
    b'Mexico Node Support'
    b'Tarek Elsaleh'
    '''

    print(tests.check_name(b'Andrea Kather'))
    print(tests.check_name(b'Phuong Quy Le'))
    print(tests.check_name(b'Alberto Abella'))

