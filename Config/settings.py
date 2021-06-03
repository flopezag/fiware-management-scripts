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
from configparser import ConfigParser
from os.path import join, exists, dirname, abspath
from os import environ

__author__ = 'fla'

__version__ = '2.0.0'


"""
Default configuration.

The configuration `cfg_defaults` are loaded from `cfg_filename`, if file exists in
/etc/fiware.d/management.ini

Optionally, user can specify the file location manually using an Environment variable called CONFIG_FILE.
"""

name = 'management'

cfg_dir = "/etc/fiware.d"

if environ.get("CONFIG_FILE"):
    cfg_filename = environ.get("CONFIG_FILE")

else:
    cfg_filename = join(cfg_dir, '%s.ini' % name)

Config = ConfigParser()

Config.read(cfg_filename)


def config_section_map(section):
    dict1 = {}
    options = Config.options(section)

    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except Exception as e:
            print("exception on %s!" % option)
            print(e)
            dict1[option] = None

    return dict1


if Config.sections():
    # Data from oauth2 section
    oauth_section = config_section_map("oauth2")
    ACCESS_TOKEN = oauth_section['access_token']
    REFRESH_TOKEN = oauth_section['refresh_token']
    CLIENT_ID = oauth_section['client_id']
    CLIENT_SECRET = oauth_section['client_secret']
    SENDER = oauth_section['sender']

    # Data from jira section
    jira_section = config_section_map("jira")
    JIRA_URL = jira_section['url']
    JIRA_USER = jira_section['user']
    JIRA_PASSWORD = jira_section['password']
    JIRA_VERIFY = jira_section['verify']

    if JIRA_VERIFY == 'True':
        JIRA_VERIFY = True
    elif JIRA_VERIFY == 'False':
        JIRA_VERIFY = False
    else:
        message = 'ERROR, verify attribute in \'management.ini\' file must be either \'True\' or \'False\', found: {}'
        print(message.format(JIRA_VERIFY))

    # Data from stackoverflow section
    stackoverflow_section = config_section_map("stackoverflow")
    API_KEY_STACKOVERFLOW = stackoverflow_section['api_key']

    # Data from backlog.fiware.org section
    backlog_section = config_section_map("backlog.fiware.org")
    API_KEY_BACKLOG = backlog_section['api_key']
    API_USER_BACKLOG = backlog_section['api_user']
    URL_BACKLOG = backlog_section['url']

    # FLUAs assignee list
    fluas_section = config_section_map("fluas")
    assignees = fluas_section['assignee']
    ASSIGNEES = assignees.replace(' ', '').split(',')

else:
    msg = '\nERROR: There is not defined CONFIG_FILE environment variable ' \
            '\n       pointing to configuration file or there is no management.ini file' \
            '\n       in the /etc/init.d directory.' \
            '\n\n       Please correct at least one of them to execute the program.\n\n\n'

    exit(msg)

# Settings file is inside Basics directory, therefore I have to go back to the parent directory
# to have the Code Home directory
CODEHOME = dirname(dirname(abspath(__file__)))
LOGHOME = join(CODEHOME, 'logs')
STOREHOME = join(join(CODEHOME, 'HelpDesk'), 'store')

CERTIFICATE = join(join(CODEHOME, 'Config'), 'jira_fiware_org.crt')

if not exists(CERTIFICATE):
    msg = '\nERROR: There is not Certificate to access to the Jira server. ' \
          '\n       It will produce warnings in the execution of the Jira requests.' \
          '\n\n       Please correct it if you do not want to see these messages.\n\n\n'

    print(msg)

    CERTIFICATE = False
