#!/usr/bin/env python
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
from logging import _nameToLevel as nameToLevel
from argparse import ArgumentParser
from Common.emailer import Emailer
from DesksReminder.reminders import HelpDeskTechReminder, HelpDeskLabReminder, HelpDeskOtherReminder, \
                                    UrgentDeskReminder, AccountsDeskReminder
from HelpDesk.synchronization import AskbotSync, HelpDeskCaretaker
from HelpDesk.stackoverflowsync import StackOverflowSync
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
from time import time

import socket

__author__ = 'Fernando López'
__version__ = "1.3.0"


def init():
    parser = ArgumentParser(prog='Jira Management Scripts', description='')

    parser.add_argument('-l',
                        '--log',
                        default='INFO',
                        help='The logging level to be used.')

    parser.add_argument('-a',
                        '--analysis',
                        dest='analysis',
                        type=str,
                        choices=['Tech', 'Lab', 'Other', 'Urgent', 'Accounts', 'Askbot', 'Stackoverflow', 'Caretaker'],
                        required=True,
                        help='The type of analysis of jira to develop.')

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

    # Set the default socket timeout to a value that prevents connections
    # to our SMTP server from timing out, due to sendmail's greeting pause
    # feature.
    socket.setdefaulttimeout(10)

    return loglevel, args.analysis


if __name__ == "__main__":
    start_time = time()

    loglevel, option = init()

    mailer = Emailer(loglevel=loglevel)

    disable_warnings(InsecureRequestWarning)

    today = datetime.today().weekday()

    if today == 0:
        if option == 'Tech':
            # Send reminder of pending JIRA tickets, only every Mondays
            techReminder = HelpDeskTechReminder(loglevel=loglevel, mailer=mailer)
            techReminder.process()
        elif option == 'Lab':
            labReminder = HelpDeskLabReminder(loglevel=loglevel, mailer=mailer)
            labReminder.process()
        elif option == 'Other':
            otherReminder = HelpDeskOtherReminder(loglevel=loglevel, mailer=mailer)
            otherReminder.process()
        elif option == 'Urgent':
            urgentReminder = UrgentDeskReminder(loglevel=loglevel, mailer=mailer)
            urgentReminder.process()
        elif option == 'Accounts':
            accountReminder = AccountsDeskReminder(loglevel=loglevel, mailer=mailer)
            accountReminder.process()

    if option == 'Askbot':
        # Askbot synchronization and Jira caretaker actions, every day
        askbotSync = AskbotSync(loglevel=loglevel)
        askbotSync.process()
    elif option == 'Caretaker':
        # Automatic reassign tickets to owners based on some extracted information, every day
        helpdeskCaretaker = HelpDeskCaretaker(loglevel=loglevel, mailer=mailer)
        helpdeskCaretaker.process()
    elif option == 'Stackoverflow':
        # StackoverFlow synchronization, every day
        stackoverflowSync = StackOverflowSync(loglevel=loglevel)
        stackoverflowSync.process(year=2015, month=9, day=21)

    print("--- %s seconds ---" % (time() - start_time))
