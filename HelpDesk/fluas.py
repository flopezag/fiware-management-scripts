#!/usr/bin/env <PATH_HELPDESK>/env/bin/python
# -*- coding: utf-8 -*-
##
# Copyright 2021 FIWARE Foundation, e.V.
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
from Common.logging_conf import LoggingConf
from jira import JIRA
from Common.emailer import Emailer
from Config.settings import JIRA_USER, JIRA_PASSWORD, JIRA_URL, ASSIGNEES
from logging import DEBUG, info, warning, error, exception
from sys import exc_info
from datetime import datetime

__author__ = 'Fernando Lopez'


class FLUAs:
    def __init__(self, loglevel, mailer, domain=JIRA_URL):
        self.base_url = 'https://{}'.format(domain)
        self.user = JIRA_USER
        self.password = JIRA_PASSWORD
        options = {'server': self.base_url, 'verify': False}
        self.jira = JIRA(options=options, basic_auth=(self.user, self.password))

        if mailer == '':
            self.emailer = Emailer(loglevel=loglevel)

        self.issues = list()
        self.maximum_requested_issues = 25
        self.assignees = ASSIGNEES

        # Number of weeks assigned to each assignee
        self.number_weeks = 2

    def get_issues(self):
        """
        Get the complete list of unresolved FLUA tickets filtering unnecessary fields and save the result
        into the issues variable class
        :return: nothing
        """
        # Get the complete list of unresolved FLUA tickets
        query = 'project = FLUA AND issuetype = UpgradeAccount AND resolution = Unresolved'
        # issues = sorted(self.jira.search_issues(query, maxResults=25), key=lambda item: item.key)

        issue = self.jira.search_issues(query, startAt=0, maxResults=0, json_result=True)

        for i in range(0, issue['total']//self.maximum_requested_issues):
            aux = self.jira.search_issues(query,
                                          startAt=i*self.maximum_requested_issues,
                                          maxResults=self.maximum_requested_issues,
                                          json_result=True)

            aux = list(map(lambda x:
                           {
                               'id': x['id'],
                               'self': x['self'],
                               'key': x['key'],
                               'created': x['fields']['created'],
                               'assignee': x['fields']['assignee']['name']},
                           aux['issues']))

            self.issues += aux

        rest = issue['total'] % self.maximum_requested_issues
        if rest != 0:
            aux = self.jira.search_issues(query,
                                          startAt=(i+1)*self.maximum_requested_issues,
                                          maxResults=rest,
                                          json_result=True)

            aux = list(map(lambda x:
                           {
                               'id': x['id'],
                               'self': x['self'],
                               'key': x['key'],
                               'created': x['fields']['created'],
                               'assignee': x['fields']['assignee']['name']},
                           aux['issues']))

            self.issues += aux

        info(f"# of reading issues: {len(self.issues)}")

    def change_assignees(self):
        """
        Change the assignee of each of the issues identified in the FLUAs project as not resolved (obtained after
        calling get_issues() method) taking into account the creation date of it and the configured list of candidates
        to manage the tickets defined in management.ini
        :return: Nothing
        """
        [self.__change_assignee__(issue=issue) for issue in self.issues]

    def __change_assignee__(self, issue):
        assignee = self.__get_assignee_number__(issue['created'])
        assignee = self.assignees[assignee]

        # requires issue assign permission, which is different from issue editing permission!
        key = issue['key']
        issue = self.jira.issue(key)

        current_assignee = issue.fields.assignee.name
        if current_assignee != assignee:
            info("Changing assignee for issue {} from {} to {}".format(key, current_assignee, assignee))
            self.jira.assign_issue(issue, assignee)

    def __get_assignee_number__(self, a_date):
        """
        Return the corresponding week number taking into account a date
        :param a_date: The date in string format
        :return: the corresponding week number to that date
        """
        a_date = datetime.strptime(a_date, "%Y-%m-%dT%H:%M:%S.%f%z").date()
        week_number = a_date.isocalendar()[1]

        # each assignee is assigned during 2 weeks, and we have to obtain the
        # corresponding assignee from the total list of assignee
        # (i-1)//2 %3
        value = ((week_number - 1) // self.number_weeks) % len(self.assignees)
        return value


class FLUAsCaretaker(LoggingConf):
    def __init__(self, loglevel, mailer):
        super(FLUAsCaretaker, self).__init__(loglevel=loglevel, log_file='fluas-caretaker.log')

        info('\n\n---- FLUAS Caretakers----\n')

        try:
            self.fluas = FLUAs(loglevel=loglevel, mailer=mailer)
        except Exception as e:
            error(e)
            exception("Unexpected error: {}".format(exc_info()[0]))
            exit()

    def process(self):
        self.fluas.get_issues()
        self.fluas.change_assignees()


if __name__ == "__main__":
    mailer = Emailer(loglevel=DEBUG)

    fluas = FLUAsCaretaker(loglevel=DEBUG, mailer=mailer)
    fluas.process()
