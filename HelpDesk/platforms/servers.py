from math import ceil
from datetime import datetime
from HelpDesk.platforms.questions import ASK, SOF
from Config.settings import STOREHOME, API_KEY_STACKOVERFLOW
from logging import info, debug, error, warning
from os.path import join, exists
from os import makedirs
from pickle import dump, load, HIGHEST_PROTOCOL
from re import match, M, I
from requests import get
from json import loads
from time import time

__author__ = 'Manuel Escriche'


class QAPlatform:
    def __init__(self, domain, name):
        self.name = name
        self.base_url = 'https://{}'.format(domain)
        self.filename = 'FIWARE.Helpdesk.' + self.name + '.pkl'

        try:
            self.timestamp, self.questions = self.load()
        except Exception as e:
            error(e)
            error('failed to load questions file {}'.format(self.filename))
            self.timestamp, self.questions = None, []

    def match(self, monitors):
        n_matches = 0
        for question in self.questions:
            for monitor in monitors:
                if self.__comp_urls(monitor.fields.customfield_11000, question.url):
                    question.monitor = monitor
                    n_matches += 1
                    break

        info('questions={}, monitors={}, matches={}'.format(len(self.questions), len(monitors), n_matches))

    def save(self):
        self.filename = join(STOREHOME, self.filename)
        with open(self.filename, 'wb') as f:
            dump((self.timestamp, self.questions), f, HIGHEST_PROTOCOL)

        info('saved questions to file: {}'.format(self.filename))

    def load(self):
        timestamp = 0.0
        questions = list()
        filename = join(STOREHOME, self.filename)

        if not exists(STOREHOME):
            warning("WARNING, the store dictionary did not exist, creating it...")
            makedirs(STOREHOME)
        elif not exists(filename):
            warning("WARNING, {} file does not exits. It will be generated in the next steps".format(self.filename))
        else:
            with open(filename, 'rb') as f:
                timestamp, questions = load(f)

        info('loaded questions from file: {}'.format(self.filename))
        return timestamp, questions

    def __comp_urls(self, url1, url2):
        """
        Compare two urls discarding the protocol
        :param url1: The first url to compare
        :param url2: The second url to compare
        :return: True if the url1 is equal to url2, discarding the protocol, False otherwise
        """
        match1 = match(r'http[s]?(.*)', url1, M | I)
        match2 = match(r'http[s]?(.*)', url2, M | I)

        result = False

        if match1 and match2:
            result = match1.group(1) == match2.group(1)
        else:
            error("No match with the 2 urls!!!!!")
            error("url1: {}".format(url1))
            error("url2: {}".format(url2))

        return result


class AskBot(QAPlatform):
    def __init__(self, domain='ask.fiware.org'):
        super(self.__class__, self).__init__(domain=domain, name='Askbot')

        self.questions_url = self.base_url + '/api/v1/questions/'

    def get_questions(self):
        self.timestamp = time()
        self.questions = []
        params = {'scope': 'all', 'sort': 'age-asc'}
        page, total_pages = 1, 2
        while page <= total_pages:
            params['page'] = page
            indata = get(self.questions_url, params=params)
            indata = loads(indata.text)
            total_pages = int(indata['pages'])
            debug('page={}, total pages={}'.format(page, total_pages))
            self.questions.extend([ASK(**item) for item in indata['questions']])
            page += 1
        self.save()


class StackExchange(QAPlatform):
    def __init__(self, domain='api.stackexchange.com'):
        super(self.__class__, self).__init__(domain=domain, name='StackOverflow')

        self.questions_url = self.base_url + '/2.2/search'
        self.answers_url = self.base_url + '/2.2/answers'
        self.app_key = API_KEY_STACKOVERFLOW

    def get_questions(self):
        # self.timestamp = datetime.now().timestamp()
        self.timestamp = time()
        self.questions = []
        params = {'tagged': 'fiware', 'site': 'stackoverflow', 'filter': 'withbody', 'key': self.app_key}
        has_more, page, total = True, 1, 0
        while has_more:
            params['page'] = page
            indata = get(self.questions_url, params=params)
            indata = loads(indata.text)
            has_more = indata['has_more']
            debug('more pages = {}, quota remaining = {}'.format(indata['has_more'], indata['quota_remaining']))
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
                indata = get(url, params=params)
                indata = loads(indata.text)

                # Check if we have some error in the call to stackoverflow
                if 'error_id' in indata:
                    error('Error in the request to StackOverflow: {}'.format(indata['error_message']))
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
                    debug('qid={}, answer={}, answer_date={}'
                          .format(question.qid, question.accepted_answer_id, question.answer_date))
