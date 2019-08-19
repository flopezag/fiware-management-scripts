#!/usr/bin/env <PATH_HELPDESK>/env/bin/python
# -*- coding: utf-8 -*-
##
# Copyright 2017 FIWARE Foundation, e.V.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##
import sys
import logging
import argparse
import os

from Config.settings import LOGHOME
from HelpDesk.desks.helpdeskImporter import HelpDeskImporter
from HelpDesk.desks.helpdesk import HelpDesk
from HelpDesk.platforms.servers import AskBot

__author__ = 'Fernando López'


class AskbotSync:
    def __init__(self, loglevel):
        if os.path.exists(LOGHOME) is False:
            os.mkdir(LOGHOME)

        filename = os.path.join(LOGHOME, 'askbot.log')
        logging.basicConfig(filename=filename,
                            format='%(asctime)s|%(levelname)s:%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=loglevel)

        try:
            self.helpdesk = HelpDeskImporter()
            self.helpdesk.get_monitors()
        except Exception as e:
            logging.error(e)
            logging.error('No connection to JIRA https://jira.fiware.org')
            logging.error("Unexpected error: {}".format(sys.exc_info()[0]))
            exit()

        self.askbot = AskBot()

    def process(self):
        def get_status(q):
            if q.monitor:
                result = q.monitor.fields.status
            else:
                result = 'None'

            return result

        try:
            self.askbot.get_questions()
        except Exception as e:
            logging.error(e)
            logging.error('Failed to get questions from server')
        finally:
            self.askbot.match(self.helpdesk.monitors)

        for question in self.askbot.questions:
            logging.debug('{}, monitor={}, monitor status={}, question url={}'
                          .format(question, question.monitor, get_status(q=question), question.url))

        self.helpdesk.update_with(self.askbot.questions)

        logging.info('helpdesk: # issues created = {}'.format(self.helpdesk.n_monitors))
        logging.info('helpdesk: # issues transitions = {}'.format(self.helpdesk.n_transitions))
        logging.info('askbot questions = {}'.format(len(self.askbot.questions)))

        log = logging.getLogger()
        log.handlers.clear()


class HelpDeskCaretaker:
    def __init__(self, loglevel):
        if os.path.exists(LOGHOME) is False:
            os.mkdir(LOGHOME)

        filename = os.path.join(LOGHOME, 'mainhelpdesk.log')
        logging.basicConfig(filename=filename,
                            format='%(asctime)s|%(levelname)s:%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=loglevel)

        try:
            self.helpdesk = HelpDesk()
        except Exception as e:
            logging.error(e)
            logging.exception("Unexpected error: {}".format(sys.exc_info()[0]))
            exit()

    def process(self):
        self.helpdesk.channel_requests()
        self.helpdesk.assign_requests()
        self.helpdesk.remove_spam()
        self.helpdesk.naming()

        logging.info('main helpdesk: # issues assigned = {}'.format(self.helpdesk.n_assignments))
        logging.info('main helpdesk: # issues channeled = {}'.format(self.helpdesk.n_channeled))
        logging.info('main helpdesk: # issues deleted = {}'.format(self.helpdesk.n_removed))
        logging.info('main helpdesk: # issues renamed = {}'.format(self.helpdesk.n_renamed))

        log = logging.getLogger()
        log.handlers.clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Askbot', description='Synchronising scripts')
    parser.add_argument('-l', '--log',
                        default='INFO',
                        help='The logging level to be used.')

    args = parser.parse_args()
    log_level = getattr(logging, args.log.upper(), None)

    if not isinstance(log_level, int):
        print('Invalid log level: {}'.format(args.log))
        exit()

    accountReminder = AskbotSync(loglevel=log_level)
    accountReminder.process()

    helpdeskCaretaker = HelpDeskCaretaker(loglevel=log_level)
    helpdeskCaretaker.process()
