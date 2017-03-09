#!/usr/bin/env <PATH_DESKSREMINDER>/env/bin/python
__author__ = 'Manuel Escriche'

import os
import logging
import argparse
from logging import DEBUG
from Basics.emailer import Emailer
from Desks.delivery_board import DeliveryBoard
from Basics.itemsReport import getTextMessagesReport
from Basics.settings import LOGHOME

parser = argparse.ArgumentParser(prog='Delivery Board Reminders', description='')
parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')
args = parser.parse_args()
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    print('Invalid log level: {}'.format(args.log))
    exit()

filename = os.path.join(LOGHOME, 'delivery-board.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=numeric_level)

deliver = True

desk = DeliveryBoard()
emailer = Emailer(log_level=DEBUG)


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
