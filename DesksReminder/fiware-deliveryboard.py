#!/usr/bin/env <PATH_DESKSREMINDER>/env/bin/python
import os
import logging
import argparse
from logging import DEBUG
from Util.emailer import Emailer
from DesksReminder.Desks.delivery_board import DeliveryBoard
from DesksReminder.Basics.itemsReport import getTextMessagesReport
from Config.settings import LOGHOME

__author__ = 'Manuel Escriche'

parser = argparse.ArgumentParser(prog='Delivery Board Reminders', description='')
parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')

args = parser.parse_args()
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    print('Invalid log level: {}'.format(args.log))
    exit()

if os.path.exists(LOGHOME) is False:
    os.mkdir(LOGHOME)

filename = os.path.join(LOGHOME, 'delivery-board.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=numeric_level)

deliver = True

desk = DeliveryBoard()
emailer = Emailer(loglevel=DEBUG)


messages = desk.upcoming()
emailer.send(messages, deliver=deliver)
logging.info('Delivery Board: Upcoming {} reminders sent'.format(len(messages)))
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
