#!/usr/bin/env <PATH_HELPDESK>/env/bin/python
from Config.settings import LOGHOME
from HelpDesk.desks.coaches import CoachesHelpDesk
from logging import error, exception, info, basicConfig
from logging import _nameToLevel as nameToLevel
from argparse import ArgumentParser
from sys import exc_info
from os.path import exists, join
from os import mkdir

__author__ = 'Manuel Escriche'

parser = ArgumentParser(prog='Coaches Help Desk caretaker', description='Coaches updating script')
parser.add_argument('-l', '--log',
                    default='INFO',
                    help='The logging level to be used.')

args = parser.parse_args()
loglevel = None

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

filename = join(LOGHOME, 'coaches.log')
basicConfig(filename=filename,
            format='%(asctime)s|%(levelname)s:%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=loglevel)


try:
    coaches = CoachesHelpDesk()

    coaches.assign_request()
    coaches.clone_to_main()
    coaches.naming()

    info('coaches helpdesk: # issues updated = {}'.format(coaches.n_assignment))
    info('coaches helpdesk: # cloned issues = {}'.format(coaches.n_clones))
    info('coaches helpdesk: # renamed issues = {}'.format(coaches.n_renamed))
except Exception as e:
    error(e)
    exception("Unexpected error: {}".format(exc_info()[0]))
    exit()
