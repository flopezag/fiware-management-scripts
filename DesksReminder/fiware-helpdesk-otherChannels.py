#!/usr/bin/env <PATH_DESKSREMINDER>/env/bin/python

__author__ = 'Manuel Escriche'

import os, logging, argparse
from Basics.emailer import Emailer
from Desks.help_desk import OthersHelpDesk
from Basics.itemsReport import getTextMessagesReport
from Basics.settings import LOGHOME

parser = argparse.ArgumentParser(prog='Main Help Desk - Other channels Reminders', description='')
parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')
args = parser.parse_args()
log_level = getattr(logging, args.log.upper(), None)
if not isinstance(log_level, int):
    print('Invalid log level: {}'.format(args.log))
    exit()

filename = os.path.join(LOGHOME, 'helpdesk-otherChannels.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=log_level)



desk = OthersHelpDesk()
emailer = Emailer(log_level=log_level)

deliver = True

messages = desk.open()
emailer.send(messages, deliver=deliver)
logging.info('Help desk - Others channel: Open {} reminders sent'.format(len(messages)))
items0 = getTextMessagesReport(messages)

messages = desk.inProgress()
emailer.send(messages, deliver=deliver)
logging.info('Help desk - Others channel: In Progress {} reminders sent'.format(len(messages)))
items1 = getTextMessagesReport(messages)

messages = desk.answered()
emailer.send(messages, deliver=deliver)
logging.info('Help desk - Others channel: Answered {} reminders sent'.format(len(messages)))
items2 = getTextMessagesReport(messages)

messages = desk.impeded()
emailer.send(messages, deliver=deliver)
logging.info('Help desk - Others channel: Impeded {} reminders sent'.format(len(messages)))
items3 = getTextMessagesReport(messages)


message = """
Dear Reminders Admin,

Please, have a summary of reminders sent for Other Channels:
  Open issues
        """ + items0 + """

Please, have a summary of reminders sent for Other Channels:
    In Progress issues
        """ + items1 + """

Please, have a summary of reminders sent for Other Channels:
    Answered issues
        """ + items2 + """

Please, have a summary of reminders sent for Other Channels:
    Impeded issues
        """ + items3 + """

Kind regards,
    Fernando
"""


emailer.send_adm_msg(subject='Report for Help Desk - Other Channels', intext=message, deliver=deliver)
