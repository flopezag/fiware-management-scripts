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
from HelpDesk.desks.helpdeskImporter import HelpDeskImporter
from HelpDesk.desks.helpdesk import HelpDesk
from HelpDesk.platforms.servers import AskBot
from logging import error, exception, info, debug
from logging import _nameToLevel as nameToLevel
from argparse import ArgumentParser
from sys import exc_info
from Common.logging_conf import LoggingConf
from Config.settings import JIRA_URL

__author__ = 'Fernando López'


class AskbotSync(LoggingConf):
    def __init__(self, loglevel):
        super(AskbotSync, self).__init__(loglevel=loglevel, log_file='askbot.log')

        info('\n\n---- Askbot Synchronization----\n')

        try:
            self.helpdesk = HelpDeskImporter()
            self.helpdesk.get_monitors()
        except Exception as e:
            error(e)
            error('No connection to JIRA https://{}'.format(JIRA_URL))
            error("Unexpected error: {}".format(exc_info()[0]))
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
            error(e)
            error('Failed to get questions from server')
        finally:
            self.askbot.match(self.helpdesk.monitors)

        for question in self.askbot.questions:
            debug('{}, monitor={}, monitor status={}, question url={}'
                  .format(question, question.monitor, get_status(q=question), question.url))

        self.helpdesk.update_with(self.askbot.questions)

        info('helpdesk: # issues created = {}'.format(self.helpdesk.n_monitors))
        info('helpdesk: # issues transitions = {}'.format(self.helpdesk.n_transitions))
        info('askbot questions = {}'.format(len(self.askbot.questions)))

        self.close()


class HelpDeskCaretaker(LoggingConf):
    def __init__(self, loglevel, mailer):
        super(HelpDeskCaretaker, self).__init__(loglevel=loglevel, log_file='mainhelpdesk.log')

        info('\n\n---- HELP-DESK Caretakers----\n')

        try:
            self.helpdesk = HelpDesk(loglevel=loglevel, mailer=mailer)
        except Exception as e:
            error(e)
            exception("Unexpected error: {}".format(exc_info()[0]))
            exit()

    def process(self):
        self.helpdesk.channel_requests()
        self.helpdesk.assign_requests()
        self.helpdesk.remove_spam()
        self.helpdesk.naming()

        info('main helpdesk: # issues assigned = {}'.format(self.helpdesk.n_assignments))
        info('main helpdesk: # issues channeled = {}'.format(self.helpdesk.n_channeled))
        info('main helpdesk: # issues deleted = {}'.format(self.helpdesk.n_removed))
        info('main helpdesk: # issues renamed = {}'.format(self.helpdesk.n_renamed))

        self.close()


if __name__ == "__main__":
    parser = ArgumentParser(prog='Askbot', description='Synchronising scripts')
    parser.add_argument('-l', '--log',
                        default='INFO',
                        help='The logging level to be used.')

    args = parser.parse_args()
    loglevel = None

    try:
        loglevel = nameToLevel[args.log.upper()]
    except Exception as e1:
        print('Invalid log level: {}'.format(args.log))
        print('Please use one of the following values:')
        print('   * CRITICAL')
        print('   * ERROR')
        print('   * WARNING')
        print('   * INFO')
        print('   * DEBUG')
        print('   * NOTSET')
        exit()

    askbotSync = AskbotSync(loglevel=loglevel)
    askbotSync.process()

    helpdeskCaretaker = HelpDeskCaretaker(loglevel=loglevel)
    helpdeskCaretaker.process()
