#!/usr/bin/env <PATH_DESKSREMINDER>/env/bin/python
__author__ = 'Manuel Escriche'

import os
import logging
import argparse
from logging import DEBUG
from Basics.emailer import Emailer
from Desks.coaches_desk import CoachesHelpDesk
from Basics.itemsReport import getTextMessagesReport
from Basics.settings import LOGHOME

parser = argparse.ArgumentParser(prog='Coaches Desk Reminders', description='')
parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')
args = parser.parse_args()
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    print('Invalid log level: {}'.format(args.log))
    exit()

filename = os.path.join(LOGHOME, 'coaches-helpdesk.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=numeric_level)



desk = CoachesHelpDesk()
emailer = Emailer(log_level=DEBUG)

deliver = True

messages = desk.open()
emailer.send(messages, deliver=deliver)
logging.info('Coaches Help desk: Open {} reminders sent'.format(len(messages)))
items0 = getTextMessagesReport(messages)

messages = desk.inProgress()
emailer.send(messages, deliver=deliver)
logging.info('Coaches Help desk: In Progress {} reminders sent'.format(len(messages)))
items1 = getTextMessagesReport(messages)

messages = desk.answered()
emailer.send(messages, deliver=deliver)
logging.info('Coaches Help desk: Answered {} reminders sent'.format(len(messages)))
items2 = getTextMessagesReport(messages)

messages = desk.impeded()
emailer.send(messages, deliver=deliver)
logging.info('Coaches Help desk: Impeded {} reminders sent'.format(len(messages)))
items3 = getTextMessagesReport(messages)


message = """
Dear Reminders Admin,

Please, have a summary of reminders sent for Coaches Desk:
  Open issues
        """ + items0 + """

Please, have a summary of reminders sent for Coaches Desk:
    In Progress issues
        """ + items1 + """

Please, have a summary of reminders sent for Coaches Desk:
    Answered issues
        """ + items2 + """

Please, have a summary of reminders sent for Coaches Desk:
    Impeded issues
        """ + items3 + """

Kind regards,
    Fernando
"""

emailer.send_adm_msg(subject='Report for Coaches Help Desk', intext=message, deliver=deliver)
