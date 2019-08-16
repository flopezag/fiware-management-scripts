#!/usr/bin/env <PATH_DESKSREMINDER>/env/bin/python
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
import os
import logging
import argparse
from DesksReminder.Basics.emailer import Emailer
from DesksReminder.Desks.help_desk import TechHelpDesk, LabHelpDesk, OthersHelpDesk
from DesksReminder.Basics.itemsReport import getTextMessagesReport
from DesksReminder.Basics.settings import LOGHOME
from DesksReminder.Desks.urgent_desk import UrgentDesk
from DesksReminder.Desks.accounts_desk import AccountsDesk

__author__ = 'Fernando López'


class HelpDeskReminder:
    def __init__(self, logginglevel, channel, mailer=None, deliver=True):
        if mailer is None:
            self.mailer = Emailer(loglevel=logginglevel)
        else:
            self.mailer = mailer

        self.channel = channel

        if isinstance(channel, TechHelpDesk):
            self.channelTxt = "Tech Channels"
        elif isinstance(channel, LabHelpDesk):
            self.channelTxt = "Lab Channels"
        elif isinstance(channel, OthersHelpDesk):
            self.channelTxt = "Other Channels"

        self.deliver = deliver

    def process(self):
        messages = self.channel.open()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('Help desk - Tech channel: Open {} reminders sent'.format(len(messages)))
        items0 = getTextMessagesReport(messages)

        messages = self.channel.inProgress()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('Help desk - Tech channel: In Progress {} reminders sent'.format(len(messages)))
        items1 = getTextMessagesReport(messages)

        messages = self.channel.answered()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('Help desk - Tech channel: Answered {} reminders sent'.format(len(messages)))
        items2 = getTextMessagesReport(messages)

        messages = self.channel.impeded()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('Help desk - Tech channel: Impeded {} reminders sent'.format(len(messages)))
        items3 = getTextMessagesReport(messages)

        message = """
        Dear Reminders Admin,

        Please, have a summary of reminders sent for """ + self.channelTxt + """:
            Open issues
                """ + items0 + """

        Please, have a summary of reminders sent for """ + self.channelTxt + """:
            In Progress issues
                """ + items1 + """

        Please, have a summary of reminders sent for """ + self.channelTxt + """:
            Answered issues
                """ + items2 + """

        Please, have a summary of reminders sent for """ + self.channelTxt + """:
            Impeded issues
                """ + items3 + """

        Kind regards,
            Fernando
        """

        subject = 'Report for Help Desk - {}'.format(self.channelTxt)
        self.mailer.send_adm_msg(subject=subject, intext=message, deliver=self.deliver)


class HelpDeskTechReminder(HelpDeskReminder):
    def __init__(self, loglevel, mailer=None):
        super(HelpDeskTechReminder, self).__init__(logginglevel=loglevel, channel=TechHelpDesk(), mailer=mailer)

        if os.path.exists(LOGHOME) is False:
            os.mkdir(LOGHOME)

        filename = os.path.join(LOGHOME, 'helpdesk-tech.log')
        logging.basicConfig(filename=filename,
                            format='%(asctime)s|%(levelname)s:%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=loglevel)

    def process(self, deliver=True):
        super(HelpDeskTechReminder, self).process()

        log = logging.getLogger()
        log.handlers.clear()


class HelpDeskLabReminder(HelpDeskReminder):
    def __init__(self, loglevel, mailer=None):
        super(HelpDeskLabReminder, self).__init__(logginglevel=loglevel, channel=LabHelpDesk(), mailer=mailer)

        if os.path.exists(LOGHOME) is False:
            os.mkdir(LOGHOME)

        filename = os.path.join(LOGHOME, 'helpdesk-lab.log')
        logging.basicConfig(filename=filename,
                            format='%(asctime)s|%(levelname)s:%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=loglevel)

    def process(self, deliver=True):
        super(HelpDeskLabReminder, self).process()

        log = logging.getLogger()
        log.handlers.clear()


class HelpDeskOtherReminder(HelpDeskReminder):
    def __init__(self, loglevel, mailer=None):
        super(HelpDeskOtherReminder, self).__init__(logginglevel=loglevel, channel=OthersHelpDesk(), mailer=mailer)

        if os.path.exists(LOGHOME) is False:
            os.mkdir(LOGHOME)

        filename = os.path.join(LOGHOME, 'helpdesk-other.log')
        logging.basicConfig(filename=filename,
                            format='%(asctime)s|%(levelname)s:%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=loglevel)

    def process(self, deliver=True):
        super(HelpDeskOtherReminder, self).process()

        log = logging.getLogger()
        log.handlers.clear()


class UrgentDeskReminder:
    def __init__(self, loglevel, mailer=None, deliver=True):
        if mailer is None:
            self.mailer = Emailer(loglevel=loglevel)
        else:
            self.mailer = mailer

        self.desk = UrgentDesk()
        self.deliver = deliver

        if os.path.exists(LOGHOME) is False:
            os.mkdir(LOGHOME)

        filename = os.path.join(LOGHOME, 'urgentdesk.log')
        logging.basicConfig(filename=filename,
                            format='%(asctime)s|%(levelname)s:%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=loglevel)

    def process(self):
        messages = self.desk.onDeadline()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('urgent desk: on deadline {} reminders sent'.format(len(messages)))
        items0 = getTextMessagesReport(messages)

        messages = self.desk.upcoming()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('urgent desk: upcoming {} reminders sent'.format(len(messages)))
        items1 = getTextMessagesReport(messages)

        messages = self.desk.impeded()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('urgent desk: impeded {} reminders sent'.format(len(messages)))
        items2 = getTextMessagesReport(messages)

        messages = self.desk.overdue()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('urgent desk: overdue {} reminders sent'.format(len(messages)))
        items3 = getTextMessagesReport(messages)

        message = """
        Dear Reminders Admin,

        Please, have a summary of reminders sent for Urgent Desk:
            On Deadline issues
                """ + items0 + """

            Upcoming issues
                """ + items1 + """

            Impeded issues
                """ + items2 + """

            Overdue issues
                """ + items3 + """

        Kind regards,
            Fernando
        """

        self.mailer.send_adm_msg(subject='Report for Urgent Desk - Upcoming', intext=message, deliver=self.deliver)

        log = logging.getLogger()
        log.handlers.clear()


class AccountsDeskReminder:
    def __init__(self, loglevel, mailer=None, deliver=True):
        if mailer is None:
            self.mailer = Emailer(loglevel=loglevel)
        else:
            self.mailer = mailer

        self.desk = AccountsDesk()
        self.deliver = deliver

        if os.path.exists(LOGHOME) is False:
            os.mkdir(LOGHOME)

        filename = os.path.join(LOGHOME, 'urgentdesk.log')
        logging.basicConfig(filename=filename,
                            format='%(asctime)s|%(levelname)s:%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=loglevel)

    def process(self):
        messages = self.desk.open()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('Accounts desk: Open {} reminders sent'.format(len(messages)))
        items0 = getTextMessagesReport(messages)

        messages = self.desk.inProgress()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('Accounts desk: In Progress {} reminders sent'.format(len(messages)))
        items1 = getTextMessagesReport(messages)

        messages = self.desk.scheduled()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('Accounts desk: Scheduled {} reminders sent'.format(len(messages)))
        items2 = getTextMessagesReport(messages)

        messages = self.desk.answered()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('Accounts desk: Answered {} reminders sent'.format(len(messages)))
        items3 = getTextMessagesReport(messages)

        messages = self.desk.rejected()
        #self.mailer.send(messages, deliver=self.deliver)
        logging.info('Accounts desk: Rejected {} reminders sent'.format(len(messages)))
        items4 = getTextMessagesReport(messages)

        message = """
        Dear Reminders Admin,

        Please, have a summary of reminders sent for Accounts Desk:
          Open issues
                """ + items0 + """

        Please, have a summary of reminders sent for Accounts Desk:
            In Progress issues
                """ + items1 + """

        Please, have a summary of reminders sent for Accounts Desk:
            Answered issues
                """ + items2 + """

        Please, have a summary of reminders sent for Accounts Desk:
            Impeded issues
                """ + items3 + """

        Please, have a summary of reminders sent for Accounts Desk:
            Rejected Issues
                """ + items4 + """

        Kind regards,
            Fernando
        """

        self.mailer.send_adm_msg(subject='Report for Accounts Desk', intext=message, deliver=self.deliver)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Main Help Desk - Channel Reminders', description='')
    parser.add_argument('-l', '--log',
                        default='INFO',
                        help='The logging level to be used.')

    args = parser.parse_args()
    log_level = getattr(logging, args.log.upper(), None)

    if not isinstance(log_level, int):
        print('Invalid log level: {}'.format(args.log))
        exit()

    mailer = Emailer(loglevel=log_level)

    '''
    techReminder = HelpDeskTechReminder(loglevel=log_level, mailer=mailer)
    techReminder.process()

    labReminder = HelpDeskLabReminder(loglevel=log_level, mailer=mailer)
    labReminder.process()

    otherReminder = HelpDeskOtherReminder(loglevel=log_level, mailer=mailer)
    otherReminder.process()
    
    urgentReminder = UrgentDeskReminder(loglevel=log_level, mailer=mailer)
    urgentReminder.process()
    '''

    accountReminder = AccountsDeskReminder(loglevel=log_level, mailer=mailer)
    accountReminder.process()
