#!/usr/bin/env <PATH_HELPDESK>/env/bin/python
import sys
import logging
import argparse

import os
# from settings import settings
from Config.settings import LOGHOME
from HelpDesk.desks.coaches import CoachesHelpDesk

__author__ = 'Manuel Escriche'

parser = argparse.ArgumentParser(prog='Coaches Help Desk caretaker', description='Coaches updating script')
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

filename = os.path.join(LOGHOME, 'coaches.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=log_level)


try:
    coaches = CoachesHelpDesk()
except Exception as e:
    logging.error(e)
    logging.exception("Unexpected error: {}".format(sys.exc_info()[0]))
    exit()

coaches.assign_request()
coaches.clone_to_main()
coaches.naming()

logging.info('coaches helpdesk: # issues updated = {}'.format(coaches.n_assignment))
logging.info('coaches helpdesk: # cloned issues = {}'.format(coaches.n_clones))
logging.info('coaches helpdesk: # renamed issues = {}'.format(coaches.n_renamed))
