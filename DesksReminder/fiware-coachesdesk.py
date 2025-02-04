#!/usr/bin/env <PATH_DESKSREMINDER>/env/bin/python
from os.path import exists, join
from os import mkdir
from argparse import ArgumentParser
from logging import DEBUG, info, basicConfig
from logging import _nameToLevel as nameToLevel
from Common.emailer import Emailer
from DesksReminder.Desks.coaches_desk import CoachesHelpDesk
from DesksReminder.Basics.itemsReport import getTextMessagesReport
from Config.settings import LOGHOME

__author__ = 'Manuel Escriche'

parser = ArgumentParser(prog='Coaches Desk Reminders', description='')
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

filename = join(LOGHOME, 'coaches-helpdesk.log')
basicConfig(filename=filename,
            format='%(asctime)s|%(levelname)s:%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=loglevel)


desk = CoachesHelpDesk()
emailer = Emailer(loglevel=DEBUG)

deliver = True

messages = desk.open()
emailer.send(messages, deliver=deliver)
info('Coaches Help desk: Open {} reminders sent'.format(len(messages)))
items0 = getTextMessagesReport(messages)

messages = desk.inProgress()
emailer.send(messages, deliver=deliver)
info('Coaches Help desk: In Progress {} reminders sent'.format(len(messages)))
items1 = getTextMessagesReport(messages)

messages = desk.answered()
emailer.send(messages, deliver=deliver)
info('Coaches Help desk: Answered {} reminders sent'.format(len(messages)))
items2 = getTextMessagesReport(messages)

messages = desk.impeded()
emailer.send(messages, deliver=deliver)
info('Coaches Help desk: Impeded {} reminders sent'.format(len(messages)))
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
