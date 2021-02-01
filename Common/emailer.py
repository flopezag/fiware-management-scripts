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

from smtplib import SMTP, SMTP_SSL, SMTPServerDisconnected, SMTPException
from logging import info, debug, exception
from base64 import b64encode
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlencode
from json import loads
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from Config.settings import ACCESS_TOKEN, REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET, SENDER
from Config.constants import SIGNATURE, GOOGLE_ACCOUNTS_BASE_URL
from logging import INFO, DEBUG
import ssl
from ssl import SSLError

__author__ = 'fla'


class Emailer:
    def __init__(self, loglevel=INFO):
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
        self.log_level = loglevel

        # Allow unverified SSL Context
        ssl._create_default_https_context = ssl._create_unverified_context

        # Creating SMTP Client
        self.server = 0
        self.__open__()

    # Deleting (Calling destructor)
    def __del__(self):
        info("[+] Destructor called, SMTP Client deleted.")

        if self.server is None:
            return
        else:
            try:
                try:
                    self.server.quit()
                except (SSLError, SMTPServerDisconnected):
                    # This happens when calling quit() on a TLS connection
                    # sometimes, or when the connection was already disconnected
                    # by the server.
                    self.server.close()
                except SMTPException:
                    if self.fail_silently:
                        return
                    raise
            finally:
                self.server = None

    def __open__(self):
        self.server = SMTP_SSL('smtp.gmail.com', 465)
        try:
            info("[+] Connecting To Mail Server.")

            if self.log_level == DEBUG:
                self.server.set_debuglevel(2)
            else:
                self.server.set_debuglevel(0)

            self.server.ehlo()

            debug("[+] Starting Encrypted Session.")
            self.server.ehlo()
            # server.starttls()

            debug("[+] Logging Into Mail Server.")
            oauth_string = self.generate_oauth2string(username=self._sender)
            (code, message) = self.server.docmd('AUTH', 'XOAUTH2 ' + oauth_string.decode())

            if code == 334:
                # The token is invalid an should be refresh
                debug("[+] oAuth2 access token expired, refreshing it.")
                self.refresh_old_token()

                # server.close()
                self.server.quit()
                self.server = SMTP_SSL('smtp.gmail.com', 465)

                if self.log_level == DEBUG:
                    self.server.set_debuglevel(2)
                else:
                    self.server.set_debuglevel(0)

                self.server.ehlo()

                debug("[+] Starting Encrypted Session.")
                self.server.ehlo()
                # server.starttls()

                debug("[+] Logging Into Mail Server again.")
                oauth_string = self.generate_oauth2string(username=self._sender)
                self.server.docmd('AUTH', 'XOAUTH2 ' + oauth_string.decode())
        except Exception as e:
            exception(e)
            exception("[-] Sending Mail Failed.")

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
            auth_string = b64encode(auth_string.encode())

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
        data = dict()
        data['client_id'] = self.client_id
        data['client_secret'] = self.client_secret
        data['refresh_token'] = self.refresh_token
        data['grant_type'] = 'refresh_token'
        request_url = self.accounts_url('o/oauth2/token')

        data = urlencode(data)
        data = data.encode('utf-8')  # data should be bytes
        req = Request(request_url, data)

        try:
            resp = urlopen(req)
            respdata = resp.read()

            self.access_token = loads(respdata)['access_token']
        except URLError:
            debug("Unable to get a new refreshed token ...")

    def send(self, messages, deliver=False):
        for n, item in enumerate(messages):
            info('#{}, Key:{}, To:{}, Summary:{}'
                 .format(n, item['issue'].key, item['displayname'].encode('utf-8'), item['summary']))

            debug('{} \n {}'.format(item['subject'], item['body']))

            if deliver:
                self.send_msg(item['email'], item['subject'], item['body'])

    def send_msg(self, to, subject, intext, deliver=True):
        msg = MIMEText(intext + self.signature)

        msg['From'] = self._sender
        msg['To'] = to
        msg['Subject'] = subject

        if deliver:
            debug("[+] Sending Mail.")
            self.server.sendmail(self._sender, msg['To'], msg.as_string())
            info("[+] Mail Sent Successfully to {}.".format(msg['To']))

    def send_adm_msg(self, subject, intext, deliver=True):
        msg = MIMEText(intext + self.signature)

        msg['From'] = self._sender
        msg['To'] = self._sender
        msg['Subject'] = 'FIWARE: Reminders: ' + subject

        if deliver:
            debug("[+] Sending Mail.")
            self.server.sendmail(self._sender, msg['To'], msg.as_string())
            info("[+] Mail Sent Successfully to {}.".format(msg['To']))

    def send_html_adm_msg(self, subject, inmsg, deliver=True):
        msg = MIMEMultipart('alternative')

        msg['From'] = self._sender
        msg['To'] = self._sender
        msg['Subject'] = 'FIWARE: Reminders: ' + subject

        part1 = MIMEText(inmsg, 'html')
        part2 = MIMEText(self.signature, 'plain')

        msg.attach(part1)
        msg.attach(part2)

        if deliver:
            debug("[+] Sending Mail.")
            self.server.sendmail(self._sender, msg['To'], msg.as_string())
            info("[+] Mail Sent Successfully to {}.".format(msg['To']))

    def send_msg_attachment(self, to, subject, intext, infile, deliver=True):
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

        if deliver:
            debug("[+] Sending Mail.")
            self.server.sendmail(self._sender, msg['To'], msg.as_string())
            debug("[+] Mail Sent Successfully to {}.".format(msg['To']))


if __name__ == "__main__":
    pass
