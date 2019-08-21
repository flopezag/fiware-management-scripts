#!/usr/bin/env <PATH_DESKSREMINDER>/env/bin/python
from os.path import join, exists
from os import mkdir
from logging import _nameToLevel as nameToLevel
from logging import basicConfig, DEBUG, info
from argparse import ArgumentParser
from Common.emailer import Emailer
from DesksReminder.Desks.delivery_board import DeliveryBoard
from DesksReminder.Basics.itemsReport import getTextMessagesReport
from Config.settings import LOGHOME

__author__ = 'Manuel Escriche'

parser = ArgumentParser(prog='Delivery Board Reminders', description='')

parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')

args = parser.parse_args()

try:
    loglevel = nameToLevel[args.log.upper()]
except Exception as e:
    print('Invalid log level: {}'.format(args.log))
    print('Please use one of the following values:')
    print('   * CRITICAL')
    print('   * ERROR')
    print('   * WARNING')
    print('   * INFO')
    print('   * DEBUG')
    print('   * NOTSET')
    exit()

if exists(LOGHOME) is False:
    mkdir(LOGHOME)

filename = join(LOGHOME, 'delivery-board.log')
basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=loglevel)

deliver = True

desk = DeliveryBoard()
emailer = Emailer(loglevel=DEBUG)


messages = desk.upcoming()
emailer.send(messages, deliver=deliver)
info('Delivery Board: Upcoming {} reminders sent'.format(len(messages)))
items = getTextMessagesReport(messages)


message = """
Dear Reminders Admin,

Please, have a summary of reminders sent for Upcoming Deliverables:
    Impeded issues
        """ + items + """

Kind regards,
    Fernando
"""

emailer.send_adm_msg(subject='Report for Delivery Board', intext=message, deliver=deliver)
