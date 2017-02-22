#!/usr/bin/env <PATH_HELPDESK>/env/bin/python

import sys
import logging
import argparse

import os
from Basics.settings import LOGHOME
from desks.helpdesk import HelpDesk

__author__ = 'Manuel Escriche'

parser = argparse.ArgumentParser(prog='Main Help Desk Caretaker', description='Main help desk updating script')
parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')

args = parser.parse_args()
log_level = getattr(logging, args.log.upper(), None)
if not isinstance(log_level, int):
    print('Invalid log level: {}'.format(args.log))
    exit()

filename = os.path.join(LOGHOME, 'mainhelpdesk.log')
logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=log_level)

try:
    helpdesk = HelpDesk()
except Exception as e:
    logging.error(e)
    logging.exception("Unexpected error: {}".format(sys.exc_info()[0]))
    exit()
else:
    helpdesk.channel_requests()
    helpdesk.assign_requests()
    helpdesk.remove_spam()
    helpdesk.naming()

logging.info('main helpdesk: # issues assigned = {}'.format(helpdesk.n_assignments))
logging.info('main helpdesk: # issues channeled = {}'.format(helpdesk.n_channeled))
logging.info('main helpdesk: # issues deleted = {}'.format(helpdesk.n_removed))
logging.info('main helpdesk: # issues renamed = {}'.format(helpdesk.n_renamed))
