#!/usr/bin/env <PATH_DESKSREMINDER>/env/bin/python
__author__ = 'Manuel Escriche'

import os, logging, argparse
from Desks.urgent_desk import UrgentDesk
from Basics.emailer import Emailer
from Basics.itemsReport import getTextMessagesReport
from Basics.settings import LOGHOME

parser = argparse.ArgumentParser(prog='Urgent Desk Reminders', description='')
parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')
args = parser.parse_args()
log_level = getattr(logging, args.log.upper(), None)
if not isinstance(log_level, int):
    print('Invalid log level: {}'.format(args.log))
    exit()

filename = os.path.join(LOGHOME, 'urgentdesk-weekly.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=log_level)

desk = UrgentDesk()
emailer = Emailer(log_level=log_level)

deliver = True

messages = desk.impeded()
emailer.send(messages, deliver=deliver)
logging.info('urgent desk: impeded {} reminders sent'.format(len(messages)))
items0 = getTextMessagesReport(messages)

messages = desk.overdue()
emailer.send(messages, deliver=deliver)
logging.info('urgent desk: overdue {} reminders sent'.format(len(messages)))
items1 = getTextMessagesReport(messages)


message = """
Dear Reminders Admin,

Please, have a summary of reminders sent for Urgent Desk:
    Impeded issues
        """ + items0 + """

Please, have a summary of reminders sent for Urgent Desk:
    Overdue issues
        """ + items1 + """

Kind regards,
    Fernando
"""

emailer.send_adm_msg(subject='Report for Urgent Desk -  Overdue & Impeded', intext=message, deliver=deliver)
