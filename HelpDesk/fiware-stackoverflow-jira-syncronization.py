#!/usr/bin/env <PATH_HELPDESK>/env/bin/python

import sys
import logging
import argparse
import os
import random

from datetime import datetime
from Basics.settings import LOGHOME
from desks.helpdeskImporter import HelpDeskImporter
from platforms.servers import StackExchange

__author__ = 'Manuel Escriche'

parser = argparse.ArgumentParser(prog='StackOverflow', description='StackOverflow synchronising script')
parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')

args = parser.parse_args()

log_level = getattr(logging, args.log.upper(), None)
if not isinstance(log_level, int):
    print('Invalid log level: {}'.format(args.log))
    exit()

filename = os.path.join(LOGHOME, 'stackoverflow.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=log_level)

helpdesk = HelpDeskImporter()

try:
    helpdesk.get_monitors()
except Exception as e:
    logging.error(e)
    logging.exception('No connection to JIRA https://jira.fiware.org')
    logging.exception("Unexpected error: {}".format(sys.exc_info()[0]))
    exit()

pq = lambda q: q.monitor.fields.status if q.monitor else 'None'

stack = StackExchange()
try:
    # raise Exception
    stack.get_questions()
except Exception as e:
    logging.error(e)
    logging.info('Failed to get questions from server')
finally:
    stack.match(helpdesk.monitors)

questions = [question for question in stack.questions if not question.answer_count]
helpdesk.update_with(questions)

######################################
dividing_day = datetime(year=2015, month=9, day=21)
answered_questions = \
    [question for question in stack.questions if question.answer_count > 0 and not question.is_answered]

new_questions = [question for question in answered_questions if question.added_at >= dividing_day]
helpdesk.update_with(new_questions)

old_questions = [question for question in answered_questions if question.added_at < dividing_day]

mon_old_questions = [question for question in old_questions if question.monitor]
helpdesk.update_with_time(mon_old_questions)

unmon_old_questions = [question for question in old_questions if not question.monitor]

if len(unmon_old_questions) > 0:
    helpdesk.update_with_time([random.choice(unmon_old_questions)])
else:
    logging.info('NOT available answered questions for synchronization with help desk')

# elif args.mode == 'accepted':
    # accepted answer

#################################################################################
accepted_questions = [question for question in stack.questions if question.is_answered]
new_questions = [question for question in accepted_questions if question.added_at >= dividing_day]
helpdesk.update_with(new_questions)

old_questions = [question for question in accepted_questions if question.added_at < dividing_day]

mon_old_questions = [question for question in old_questions if question.monitor]
unmon_old_questions = [question for question in old_questions if not question.monitor]
questions = mon_old_questions

if len(unmon_old_questions) > 0:
    questions.append(random.choice(unmon_old_questions))
else:
    logging.info('NOT available questions with accepted answer for synchronization with help desk')

try:
    stack.get_answers(questions)
except Exception as e:
    logging.error(e)
    logging.exception('Failed to get answers from server')
    logging.exception("Unexpected error: {}".format(sys.exc_info()[0]))
else:
    helpdesk.update_with_time(questions)


logging.info('helpdesk: # issues created = {}'.format(helpdesk.n_monitors))
logging.info('helpdesk: # issues transitions = {}'.format(helpdesk.n_transitions))
logging.info('helpdesk: # issues assignments = {}'.format(helpdesk.n_assigments))
logging.info('stackoverflow questions= {}'.format(len(stack.questions)))


def report(questions):
    for question in questions:
        logging.debug('{}, monitor={}, monitor status={}, question url={}'
                      .format(question, question.monitor, pq(question), question.url))
