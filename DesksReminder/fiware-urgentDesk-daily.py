#!/usr/bin/env <PATH_DESKSREMINDER>/env/bin/python
import os
import logging
import argparse

from Desks.urgent_desk import UrgentDesk
from Basics.emailer import Emailer
from Basics.itemsReport import getTextMessagesReport
from Basics.settings import LOGHOME

__author__ = 'Manuel Escriche'

parser = argparse.ArgumentParser(prog='Urgent Desk Reminders', description='')
parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')

args = parser.parse_args()
log_level = getattr(logging, args.log.upper(), None)

if not isinstance(log_level, int):
    print('Invalid log level: {}'.format(args.log))
    exit()

if os.path.exists(LOGHOME) is False:
    os.mkdir(LOGHOME)

filename = os.path.join(LOGHOME, 'urgentdesk-daily.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=log_level)


desk = UrgentDesk()
emailer = Emailer(log_level=log_level)

deliver = True

messages = desk.onDeadline()
emailer.send(messages, deliver=deliver)
logging.info('urgent desk: on deadline {} reminders sent'.format(len(messages)))
items0 = getTextMessagesReport(messages)

messages = desk.upcoming()
emailer.send(messages, deliver=deliver)
logging.info('urgent desk: upcoming {} reminders sent'.format(len(messages)))
items1 = getTextMessagesReport(messages)


message = """
Dear Reminders Admin,

Please, have a summary of reminders sent for Urgent Desk:
    On Deadline issues
        """ + items0 + """

Please, have a summary of reminders sent for Urgent Desk:
    Upcoming issues
        """ + items1 + """

Kind regards,
    Fernando
"""

emailer.send_adm_msg(subject='Report for Urgent Desk - Upcoming', intext=message, deliver=deliver)
