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

import sys
import logging
import argparse
import os
import random

from datetime import datetime
from platforms.servers import StackExchange
from Basics.settings import LOGHOME
from desks.helpdeskImporter import HelpDeskImporter


__author__ = "Fernando López <fernando.lopez@fiware.org"


def init_logging():
    """
    Initialize the script and fix the log level.
    :return: Nothing.
    """
    # Tell urlib3 to use the pyOpenSSL
    # urllib3.contrib.pyopenssl.inject_into_urllib3()

    # Create a PoolManager that verifies certificates when performing requests
    # http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    # Create the scripts arguments to execute the scripts
    parser = argparse.ArgumentParser(prog='StackOverflow', description='StackOverflow synchronising script')
    parser.add_argument('-l', '--log',
                        default='INFO',
                        help='The logging level to be used.')

    args = parser.parse_args()

    log_level = getattr(logging, args.log.upper(), None)
    if not isinstance(log_level, int):
        print('Invalid log level: {}'.format(args.log))
        print('Please use one of the following values:')
        print('   * CRITICAL')
        print('   * ERROR')
        print('   * WARNING')
        print('   * INFO')
        print('   * DEBUG')
        print('   * NOTSET')
        exit()

    if os.path.exists(LOGHOME) is False:
        os.mkdir(LOGHOME)

    filename = os.path.join(LOGHOME, 'stackoverflow.log')
    logging.basicConfig(filename=filename,
                        format='%(asctime)s|%(levelname)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=log_level)


def get_help_desk():
    """
    Initialize the HelpDesk and obtain the monitors lists from the pickle file.
    :return: the helpdesk.
    """
    logging.info("Getting the HelpDesk monitors data")

    help_desk = HelpDeskImporter()

    try:
        help_desk.get_monitors()
    except Exception as e:
        logging.error(e)
        logging.exception('No connection to JIRA https://jira.fiware.org')
        logging.exception("Unexpected error: {}".format(sys.exc_info()[0]))
        exit()

    return help_desk


def get_stack_monitor(help_desk):
    """
    Get the list of questions in StackOverflow and the relation of questions already monitored in the system.
    :return: The StackOverflow data.
    """
    logging.info("Getting the StackOverflow data")

    stack = StackExchange()
    try:
        # raise Exception
        stack.get_questions()
    except Exception as e:
        logging.error(e)
        logging.info('Failed to get questions from server')
    finally:
        stack.match(help_desk.monitors)

    return stack


def questions_with_no_answer(help_desk, initial_list, partition_date):
    """
    Get the list of questions in StackOverflow with no response.
    :param help_desk: The list of Help Desk questions that we have in Jira.
    :param initial_list: The complete lists of questions in StackOverflow to check.
    :param partition_date: Date from which we check the new questions.
    :return: Nothing
    """
    # Firstly: Get the list of monitored and unmonitored questions with no answer
    logging.info("Obtaining list of questions with no answer")

    list_questions = filter(lambda x: not x.answer_count, initial_list.questions)
    help_desk.update_with(list_questions)

    answered_questions = filter(lambda x: x.answer_count > 0 and not x.is_answered, initial_list.questions)

    new_questions = filter(lambda x: x.added_at >= partition_date, answered_questions)
    help_desk.update_with(new_questions)

    old_questions = filter(lambda x: x.added_at < partition_date, answered_questions)

    mon_old_questions = filter(lambda x: x.monitor, old_questions)
    help_desk.update_with_time(mon_old_questions)

    unmon_old_questions = filter(lambda x: not x.monitor, old_questions)

    if len(unmon_old_questions) > 0:
        help_desk.update_with_time([random.choice(unmon_old_questions)])
    else:
        logging.info('NOT available answered questions for synchronization with help desk')


def questions_with_answers(help_desk, initial_list, partition_date):
    """
    Get the list of questions with a answer but not reflected in Jira.
    :param help_desk: The list of Help Desk questions that we have in Jira.
    :param initial_list: The complete lists of questions in StackOverflow to check.
    :param partition_date: Date from which we check the new questions.
    :return: The list of questions that need to be monitored.
    """
    # Secondly: Get the list of questions answered to check if they are monitored
    logging.info("Obtaining list of questions answers")

    accepted_questions = filter(lambda x: x.is_answered, initial_list.questions)

    new_questions = filter(lambda x: x.added_at >= partition_date, accepted_questions)
    help_desk.update_with(new_questions)

    old_questions = filter(lambda x: x.added_at < partition_date, accepted_questions)

    mon_old_questions = filter(lambda x: x.monitor, old_questions)

    unmon_old_questions = filter(lambda x: not x.monitor, old_questions)

    list_questions = mon_old_questions

    if len(unmon_old_questions) > 0:
        list_questions.append(random.choice(unmon_old_questions))
    else:
        logging.info('NOT available questions with accepted answer for synchronization with help desk')

    return list_questions


def get_answers(sof_questions, help_desk, list_questions):
    """

    :param sof_questions:
    :param help_desk:
    :param list_questions:
    :return:
    """
    logging.info("Getting the final list of StackOverflow questions")

    try:
        sof_questions.get_answers(list_questions)
    except Exception as e:
        logging.error(e)
        logging.exception('Failed to get answers from server')
        logging.exception("Unexpected error: {}".format(sys.exc_info()[0]))
    else:
        help_desk.update_with_time(list_questions)


def report(list_questions):
    def pq(a_question):
        result = 'None'
        if a_question.monitor:
            result = a_question.monitor.fields.status

        return result

    for question in list_questions:
        logging.debug('{}, monitor={}, monitor status={}, question url={}'
                      .format(question, question.monitor, pq(question), question.url))


if __name__ == "__main__":
    init_logging()

    hd = get_help_desk()

    sof = get_stack_monitor(hd)

    dividing_day = datetime(year=2015, month=9, day=21)

    questions_with_no_answer(help_desk=hd, initial_list=sof, partition_date=dividing_day)

    questions = questions_with_answers(help_desk=hd, initial_list=sof, partition_date=dividing_day)

    get_answers(sof_questions=sof, help_desk=hd, list_questions=questions)

    logging.info('helpdesk: # issues created = {}'.format(hd.n_monitors))
    logging.info('helpdesk: # issues transitions = {}'.format(hd.n_transitions))
    logging.info('helpdesk: # issues assignments = {}'.format(hd.n_assigments))
    logging.info('stackoverflow questions= {}'.format(len(sof.questions)))
