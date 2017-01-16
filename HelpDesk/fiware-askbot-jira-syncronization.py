#!/usr/bin/env /home/mev/HelpDesk/helpdesk-sync/bin/python

import sys
import logging
import argparse
import os

from Basics.settings import LOGHOME
from desks.helpdeskImporter import HelpDeskImporter
from platforms.servers import AskBot

__author__ = 'Manuel Escriche'

parser = argparse.ArgumentParser(prog='Askbot', description='Askbot synchronising script')
parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')

args = parser.parse_args()
log_level = getattr(logging, args.log.upper(), None)

if not isinstance(log_level, int):
    print('Invalid log level: {}'.format(args.log))
    exit()


filename = os.path.join(LOGHOME, 'askbot.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=log_level)

try:
    helpdesk = HelpDeskImporter()
    helpdesk.get_monitors()
except Exception as e:
    logging.error(e)
    logging.error('No connection to JIRA https://jira.fiware.org')
    logging.error("Unexpected error: {}".format(sys.exc_info()[0]))
    exit()


askbot = AskBot()

try:
    askbot.get_questions()
except Exception as e:
    logging.error(e)
    logging.error('Failed to get questions from server')
finally:
    askbot.match(helpdesk.monitors)

pq = lambda q: q.monitor.fields.status if q.monitor else 'None'

for question in askbot.questions:
    logging.debug('{}, monitor={}, monitor status={}, question url={}'
                  .format(question, question.monitor, pq(question), question.url))

helpdesk.update_with(askbot.questions)

logging.info('helpdesk: # issues created = {}'.format(helpdesk.n_monitors))
logging.info('helpdesk: # issues transitions = {}'.format(helpdesk.n_transitions))
logging.info('askbot questions = {}'.format(len(askbot.questions)))
