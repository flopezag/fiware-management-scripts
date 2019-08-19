import json
import pickle
import logging
from math import ceil
from datetime import datetime
import time
import os
import re
import requests
from HelpDesk.platforms.questions import ASK, SOF
from Config.settings import STOREHOME, API_KEY_STACKOVERFLOW

__author__ = 'Manuel Escriche'


class QAPlatform(object):
    def __init__(self, domain):
        self.base_url = 'https://{}'.format(domain)
        self.filename = 'FIWARE.Helpdesk.' + self.name + '.pkl'
        try:
            self.timestamp, self.questions = self.load()
        except Exception as e:
            logging.error(e)
            logging.error('failed to load questions file {}'.format(self.filename))
            self.timestamp, self.questions = None, []

    def match(self, monitors):
        n_matches = 0
        for question in self.questions:
            for monitor in monitors:
                if self.__comp_urls(monitor.fields.customfield_11000, question.url):
                    question.monitor = monitor
                    n_matches += 1
                    break
        logging.info('questions={}, monitors={}, matches={}'.format(len(self.questions), len(monitors), n_matches))

    def save(self):
        self.filename = os.path.join(STOREHOME, self.filename)
        with open(self.filename, 'wb') as f:
            pickle.dump((self.timestamp, self.questions), f, pickle.HIGHEST_PROTOCOL)
        logging.info('saved questions to file: {}'.format(self.filename))

    def load(self):
        with open(os.path.join(STOREHOME, self.filename), 'rb') as f:
            timestamp, questions = pickle.load(f)
        logging.info('loaded questions from file: {}'.format(self.filename))
        return timestamp, questions

    def __comp_urls(self, url1, url2):
        """
        Compare two urls discarding the protocol
        :param url1: The first url to compare
        :param url2: The second url to compare
        :return: True if the url1 is equal to url2, discarding the protocol, False otherwise
        """
        match1 = re.match(r'http[s]?(.*)', url1, re.M | re.I)
        match2 = re.match(r'http[s]?(.*)', url2, re.M | re.I)

        result = False

        if match1 and match2:
            result = match1.group(1) == match2.group(1)
        else:
            logging.error("No match with the 2 urls!!!!!")
            logging.error("url1: {}".format(url1))
            logging.error("url2: {}".format(url2))

        return result


class AskBot(QAPlatform):
    def __init__(self, domain='ask.fiware.org'):
        self.name = 'Askbot'
        # super().__init__(domain)
        super(self.__class__, self).__init__(domain)
        self.questions_url = self.base_url + '/api/v1/questions/'

    def get_questions(self):
        # self.timestamp = datetime.now().timestamp()
        self.timestamp = time.time()
        self.questions = []
        params = {'scope': 'all', 'sort': 'age-asc'}
        page, total_pages = 1, 2
        while page <= total_pages:
            params['page'] = page
            indata = requests.get(self.questions_url, params=params)
            indata = json.loads(indata.text)
            total_pages = int(indata['pages'])
            logging.debug('page={}, total pages={}'.format(page, total_pages))
            self.questions.extend([ASK(**item) for item in indata['questions']])
            page += 1
        self.save()


class StackExchange(QAPlatform):
    def __init__(self, domain='api.stackexchange.com'):
        self.name = 'StackOverflow'
        # super().__init__(domain)
        super(self.__class__, self).__init__(domain)
        self.questions_url = self.base_url + '/2.2/search'
        self.answers_url = self.base_url + '/2.2/answers'
        self.app_key = API_KEY_STACKOVERFLOW

    def get_questions(self):
        # self.timestamp = datetime.now().timestamp()
        self.timestamp = time.time()
        self.questions = []
        params = {'tagged': 'fiware', 'site': 'stackoverflow', 'filter': 'withbody', 'key': self.app_key}
        has_more, page, total = True, 1, 0
        while has_more:
            params['page'] = page
            indata = requests.get(self.questions_url, params=params)
            indata = json.loads(indata.text)
            has_more = indata['has_more']
            logging.debug('more pages = {}, quota remaining = {}'.format(indata['has_more'], indata['quota_remaining']))
            self.questions.extend([SOF(**item) for item in indata['items']])
            page += 1
        self.save()

    def get_answers(self, questions):
        answers = [question.accepted_answer_id for question in questions if question.accepted_answer_id]
        total = len(answers)
        params = {'tagged': 'fiware', 'site': 'stackoverflow'}
        rounds = ceil(total / 100)
        data = []
        iteration, chunk = 1, 100
        while iteration <= rounds:
            _min = chunk * (iteration - 1)
            _max = _min + chunk
            url = self.answers_url + '/' + ';'.join(answers[_min:_max]) + '/'
            has_more, page, total = True, 1, 0
            while has_more:
                params['page'] = page
                indata = requests.get(url, params=params)
                indata = json.loads(indata.text)

                # Check if we have some error in the call to stackoverflow
                if 'error_id' in indata:
                    logging.error('Error in the request to StackOverflow: {}'.format(indata['error_message']))
                    has_more = False
                else:
                    has_more = indata['has_more'] if 'has_more' in indata else False
                    data.extend(indata['items'])

                page += 1

            iteration += 1

        for question in questions:
            for answer in data:
                answer_id = str(answer['answer_id'])
                question_id = str(answer['question_id'])
                if question.qid == question_id and question.accepted_answer_id == answer_id:
                    question.answer_date = datetime.fromtimestamp(int(answer['creation_date']))
                    question.answer_date = datetime.fromtimestamp(int(answer['creation_date']))
                    logging.debug('qid={}, answer={}, answer_date={}'.format(question.qid,
                                                                             question.accepted_answer_id,
                                                                             question.answer_date))
