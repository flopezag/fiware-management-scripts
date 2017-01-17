__author__ = 'Manuel Escriche'

import requests
from Basics.settings import API_KEY_BACKLOG

#domain = 'http://127.0.0.1:5000'
domain = 'http://backlog.fiware.org'

auth = 'api', API_KEY_BACKLOG


def find_enablersBook():
    url = '{}'.format(domain) + '/api/enablersbook'
    answer = requests.get(url, auth=auth)

    if not answer.ok:
        raise Exception

    return answer.json()['book']


def find_nodesBook():
    url = '{}'.format(domain) + '/api/nodesbook'
    answer = requests.get(url, auth=auth)

    if not answer.ok:
        raise Exception

    return answer.json()['book']


def find_chaptersBook():
    url = '{}'.format(domain) + '/api/chaptersbook'
    answer = requests.get(url, auth=auth)

    if not answer.ok:
        raise Exception

    return answer.json()['book']
