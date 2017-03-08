#!/usr/bin/env <PATH_DESKSREMINDER>/env/bin/python
__author__ = 'Manuel Escriche'

import os
import logging
import argparse

from logging import DEBUG
from Basics.emailer import Emailer
from Desks.help_desk import LabHelpDesk
from Basics.itemsReport import getTextMessagesReport
from Basics.settings import LOGHOME

parser = argparse.ArgumentParser(prog='Main Help Desk - Lab channel Reminders', description='')
parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')
args = parser.parse_args()
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    print('Invalid log level: {}'.format(args.log))
    exit()

filename = os.path.join(LOGHOME, 'helpdesk-lab.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=numeric_level)



desk = LabHelpDesk()
emailer = Emailer(log_level=DEBUG)
deliver = True

messages = desk.open()
emailer.send(messages, deliver=deliver)
logging.info('Help desk - Lab channel: Open {} reminders sent'.format(len(messages)))
items0 = getTextMessagesReport(messages)

messages = desk.inProgress()
emailer.send(messages, deliver=deliver)
logging.info('Help desk - Lab channel: In Progress {} reminders sent'.format(len(messages)))
items1 = getTextMessagesReport(messages)

messages = desk.answered()
emailer.send(messages, deliver=deliver)
logging.info('Help desk - Lab channel: Answered {} reminders sent'.format(len(messages)))
items2 = getTextMessagesReport(messages)

messages = desk.impeded()
emailer.send(messages, deliver=deliver)
logging.info('Help desk - Lab channel: Impeded {} reminders sent'.format(len(messages)))
items3 = getTextMessagesReport(messages)


message = """
Dear Reminders Admin,

Please, have a summary of reminders sent for Lab Channels:
  Open issues
        """ + items0 + """

Please, have a summary of reminders sent for Lab Channels:
    In Progress issues
        """ + items1 + """

Please, have a summary of reminders sent for Lab Channels:
    Answered issues
        """ + items2 + """

Please, have a summary of reminders sent for Lab Channels:
    Impeded issues
        """ + items3 + """

Kind regards,
    Fernando
"""

emailer.send_adm_msg(subject='Report for Help Desk - Lab Channel', intext=message, deliver=deliver)
