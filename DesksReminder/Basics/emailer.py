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

import smtplib
import logging
import base64
import urllib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from settings import ACCESS_TOKEN, REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET, SENDER
from constants import SIGNATURE, GOOGLE_ACCOUNTS_BASE_URL
from logging import INFO, DEBUG

__author__ = 'fla'


class Emailer:
    def __init__(self, log_level=INFO):
        self._sender = SENDER

        # My OAuth2 access token
        self.access_token = ACCESS_TOKEN

        # My OAuth2 refresh token
        self.refresh_token = REFRESH_TOKEN

        # The client_id used in my tests
        self.client_id = CLIENT_ID

        # The client_secret of my gmail account
        self.client_secret = CLIENT_SECRET

        # The URL root for accessing Google Accounts.
        self.GOOGLE_ACCOUNTS_BASE_URL = GOOGLE_ACCOUNTS_BASE_URL

        # The signature of my emails
        self.signature = SIGNATURE

        # Log level
        self.log_level = log_level

    def generate_oauth2string(self, username, base64_encode=True):
        """Generates an IMAP OAuth2 authentication string.

        See https://developers.google.com/google-apps/gmail/oauth2_overview

        Args:
            username: the username (email address) of the account to authenticate
            base64_encode: Whether to base64-encode the output.

        Returns:
            The SASL argument for the OAuth2 mechanism.
        """
        auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, self.access_token)

        if base64_encode:
            auth_string = base64.b64encode(auth_string)

        return auth_string

    def accounts_url(self, command):
        """Generates the Google Accounts URL.

        Args:
            command: The command to execute.

        Returns:
            A URL for the given command.
        """
        return '%s/%s' % (self.GOOGLE_ACCOUNTS_BASE_URL, command)

    def refresh_old_token(self):
        """Obtains a new token given a refresh token.

        See https://developers.google.com/accounts/docs/OAuth2InstalledApp#refresh

        Returns:
            The decoded response from the Google Accounts server, as a dict. Expected
            fields include 'access_token', 'expires_in', and 'refresh_token'.
        """
        params = dict()
        params['client_id'] = self.client_id
        params['client_secret'] = self.client_secret
        params['refresh_token'] = self.refresh_token
        params['grant_type'] = 'refresh_token'
        request_url = self.accounts_url('o/oauth2/token')

        response = urllib.urlopen(request_url, urllib.urlencode(params)).read()

        self.access_token = json.loads(response)['access_token']

    def _deliver(self, msg):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        try:
            logging.info("[+] Connecting To Mail Server.")

            if self.log_level == DEBUG:
                server.set_debuglevel(True)

            server.ehlo()

            logging.debug("[+] Starting Encrypted Session.")
            server.ehlo()
            server.starttls()

            logging.debug("[+] Logging Into Mail Server.")
            oauth_string = self.generate_oauth2string(username=self._sender)
            (code, message) = server.docmd('AUTH', 'XOAUTH2 ' + oauth_string)

            if code == 334:
                # The token is invalid an should be refresh
                logging.debug("[+] oAuth2 access token expired, refreshing it.")
                self.refresh_old_token()

                server.close()
                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.set_debuglevel(True)
                server.ehlo()

                logging.debug("[+] Starting Encrypted Session.")
                server.ehlo()
                server.starttls()

                logging.debug("[+] Logging Into Mail Server again.")
                oauth_string = self.generate_oauth2string(username=self._sender)
                server.docmd('AUTH', 'XOAUTH2 ' + oauth_string)

            logging.debug("[+] Sending Mail.")
            server.sendmail(self._sender, msg['To'], msg.as_string())

            server.close()
            logging.info("[+] Mail Sent Successfully.")

        except Exception as e:
            logging.exception(e)
            logging.exception("[-] Sending Mail Failed.")

    def send(self, messages, deliver=False):
        for n, item in enumerate(messages):
            logging.info('#{}, Key:{}, To:{}, Summary:{}'
                         .format(n, item['issue'].key, item['displayname'].encode('utf-8'), item['summary']))

            logging.debug('{} \n {}'.format(item['subject'], item['body']))

            if deliver:
                self.send_msg(item['email'], item['subject'], item['body'])

    def send_msg(self, to, subject, intext):
        msg = MIMEText(intext + self.signature)

        msg['From'] = self._sender
        msg['To'] = to
        msg['Subject'] = subject

        self._deliver(msg)

    def send_adm_msg(self, subject, intext):
        msg = MIMEText(intext + self.signature)

        msg['From'] = self._sender
        msg['To'] = self._sender
        msg['Subject'] = 'FIWARE: Reminders: ' + subject

        self._deliver(msg)

    def send_html_adm_msg(self, subject, inmsg):
        msg = MIMEMultipart('alternative')

        msg['From'] = self._sender
        msg['To'] = self._sender
        msg['Subject'] = 'FIWARE: Reminders: ' + subject

        part1 = MIMEText(inmsg, 'html')
        part2 = MIMEText(self.signature, 'plain')

        msg.attach(part1)
        msg.attach(part2)

        self._deliver(msg)

    def send_msg_attachment(self, to, subject, intext, infile):
        msg = MIMEMultipart()

        msg['From'] = self._sender
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(intext + self.signature))

        fp = open(infile, 'rb')
        filemsg = MIMEApplication(fp.read(), _subtype="xlsx")
        fp.close()
        filemsg.add_header('Content-Disposition', 'attachment; filename = {}'.format(infile))
        msg.attach(filemsg)
        self._deliver(msg)

if __name__ == "__main__":
    pass
