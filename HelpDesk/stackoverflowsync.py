#!/usr/bin/env <PATH_HELPDESK>/env/bin/python
# -*- encoding: utf-8 -*-
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

from datetime import datetime
from HelpDesk.platforms.servers import StackExchange
from HelpDesk.desks.helpdeskImporter import HelpDeskImporter
from logging import error, exception, info, debug
from logging import _nameToLevel as nameToLevel
from argparse import ArgumentParser
from sys import exc_info
from random import choice
from Common.logging_conf import LoggingConf
from Config.settings import JIRA_URL


__author__ = "Fernando López <fernando.lopez@fiware.org"


class StackOverflowSync(LoggingConf):
    def __init__(self, loglevel):
        """
        Initialize the script and fix the log level.
        :return: Nothing.
        """
        super(StackOverflowSync, self).__init__(loglevel=loglevel, log_file='stackoverflow.log')

        info('\n\n---- StackOverflow Synchronization----\n')

        # Tell urlib3 to use the pyOpenSSL
        # urllib3.contrib.pyopenssl.inject_into_urllib3()

        # Create a PoolManager that verifies certificates when performing requests
        # http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

        info("Getting the HelpDesk monitors data")

        self.help_desk = HelpDeskImporter()
        self.stack = StackExchange()
        self.list_questions = None

        try:
            self.help_desk.get_monitors()
        except Exception as e:
            error(e)
            exception('No connection to JIRA https://{}'.format(JIRA_URL))
            exception("Unexpected error: {}".format(exc_info()[0]))
            exit()

    def get_stack_monitor(self):
        """
        Get the list of questions in StackOverflow and the relation of questions already monitored in the system.
        :return: The StackOverflow data.
        """
        info("Getting the StackOverflow data")

        try:
            # raise Exception
            self.stack.get_questions()
        except Exception as e:
            error(e)
            info('Failed to get questions from server')
        finally:
            self.stack.match(self.help_desk.monitors)

    def questions_with_no_answer(self, partition_date):
        """
        Get the list of questions in StackOverflow with no response.
        :param partition_date: Date from which we check the new questions.
        :return: Nothing
        """
        # Firstly: Get the list of monitored and unmonitored questions with no answer
        info("Obtaining list of questions with no answer")

        list_questions = filter(lambda x: not x.answer_count, self.stack.questions)
        self.help_desk.update_with(list_questions)

        answered_questions = filter(lambda x: x.answer_count > 0 and not x.is_answered, self.stack.questions)

        new_questions = filter(lambda x: x.added_at >= partition_date, answered_questions)
        self.help_desk.update_with(new_questions)

        old_questions = filter(lambda x: x.added_at < partition_date, answered_questions)

        mon_old_questions = filter(lambda x: x.monitor, old_questions)
        self.help_desk.update_with_time(mon_old_questions)

        unmon_old_questions = list(filter(lambda x: not x.monitor, old_questions))

        if len(unmon_old_questions) > 0:
            self.help_desk.update_with_time([choice(unmon_old_questions)])
        else:
            info('NOT available answered questions for synchronization with help desk')

    def questions_with_answers(self, partition_date):
        """
        Get the list of questions with a answer but not reflected in Jira.
        :param partition_date: Date from which we check the new questions.
        :return: The list of questions that need to be monitored.
        """
        # Secondly: Get the list of questions answered to check if they are monitored
        info("Obtaining list of questions answers")

        accepted_questions = filter(lambda x: x.is_answered, self.stack.questions)

        new_questions = filter(lambda x: x.added_at >= partition_date, accepted_questions)
        self.help_desk.update_with(new_questions)

        old_questions = filter(lambda x: x.added_at < partition_date, accepted_questions)

        mon_old_questions = list(filter(lambda x: x.monitor, old_questions))

        unmon_old_questions = list(filter(lambda x: not x.monitor, old_questions))

        list_questions = mon_old_questions

        if len(unmon_old_questions) > 0:
            list_questions.append(choice(unmon_old_questions))
        else:
            info('NOT available questions with accepted answer for synchronization with help desk')

        self.list_questions = list_questions

    def get_answers(self):
        """

        :return:
        """
        info("Getting the final list of StackOverflow questions")

        try:
            self.stack.get_answers(self.list_questions)
        except Exception as e:
            error(e)
            exception('Failed to get answers from server')
            exception("Unexpected error: {}".format(exc_info()[0]))
        else:
            self.help_desk.update_with_time(self.list_questions)

    def report(self):
        def pq(a_question):
            result = 'None'
            if a_question.monitor:
                result = a_question.monitor.fields.status

            return result

        for question in self.list_questions:
            debug('{}, monitor={}, monitor status={}, question url={}'
                  .format(question, question.monitor, pq(question), question.url))

    def get_number_issues_created(self):
        return self.help_desk.n_monitors

    def get_number_transitions(self):
        return self.help_desk.n_transitions

    def get_number_assignments(self):
        return self.help_desk.n_assigments

    def get_questions(self):
        return len(self.stack.questions)

    def process(self, year, month, day):
        self.get_stack_monitor()

        dividing_day = datetime(year=year, month=month, day=day)

        self.questions_with_no_answer(partition_date=dividing_day)
        self.questions_with_answers(partition_date=dividing_day)

        self.get_answers()

        info('helpdesk: # issues created = {}'.format(self.get_number_issues_created()))
        info('helpdesk: # issues transitions = {}'.format(self.get_number_transitions()))
        info('helpdesk: # issues assignments = {}'.format(self.get_number_assignments()))
        info('stackoverflow questions= {}'.format(self.get_questions()))

        self.close()


if __name__ == "__main__":
    # Create the scripts arguments to execute the scripts
    parser = ArgumentParser(prog='StackOverflow', description='StackOverflow synchronising script')
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

    stackoverflowSync = StackOverflowSync(loglevel=loglevel)
    stackoverflowSync.process(year=2015, month=9, day=21)
