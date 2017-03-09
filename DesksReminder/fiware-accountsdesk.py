#!/usr/bin/env <PATH_DESKSREMINDER>/env/bin/python

import os
import logging
import argparse
from logging import DEBUG
from Basics.settings import LOGHOME
from Basics.emailer import Emailer
from Desks.accounts_desk import AccountsDesk
from Basics.itemsReport import getTextMessagesReport

__author__ = 'Manuel Escriche'

parser = argparse.ArgumentParser(prog='Accounts Desk Reminders', description='')
parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')

args = parser.parse_args()
numeric_level = getattr(logging, args.log.upper(), None)

if not isinstance(numeric_level, int):
    print('Invalid log level: {}'.format(args.log))
    exit()

filename = os.path.join(LOGHOME, 'accounts-desk.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=numeric_level)



desk = AccountsDesk()
emailer = Emailer(log_level=DEBUG)

deliver = True

messages = desk.open()
emailer.send(messages, deliver=deliver)
logging.info('Accounts desk: Open {} reminders sent'.format(len(messages)))
items0 = getTextMessagesReport(messages)

messages = desk.inProgress()
emailer.send(messages, deliver=deliver)
logging.info('Accounts desk: In Progress {} reminders sent'.format(len(messages)))
items1 = getTextMessagesReport(messages)

messages = desk.scheduled()
emailer.send(messages, deliver=deliver)
logging.info('Accounts desk: Scheduled {} reminders sent'.format(len(messages)))
items2 = getTextMessagesReport(messages)

messages = desk.answered()
emailer.send(messages, deliver=deliver)
logging.info('Accounts desk: Answered {} reminders sent'.format(len(messages)))
items3 = getTextMessagesReport(messages)

messages = desk.rejected()
emailer.send(messages, deliver=deliver)
logging.info('Accounts desk: Rejected {} reminders sent'.format(len(messages)))
items4 = getTextMessagesReport(messages)

message = """
Dear Reminders Admin,

Please, have a summary of reminders sent for Accounts Desk:
  Open issues
        """ + items0 + """

Please, have a summary of reminders sent for Accounts Desk:
    In Progress issues
        """ + items1 + """

Please, have a summary of reminders sent for Accounts Desk:
    Answered issues
        """ + items2 + """

Please, have a summary of reminders sent for Accounts Desk:
    Impeded issues
        """ + items3 + """

Please, have a summary of reminders sent for Accounts Desk:
    Rejected Issues
        """ + items4 + """

Kind regards,
    Fernando
"""

emailer.send_adm_msg(subject='Report for Accounts Desk', intext=message, deliver=deliver)
