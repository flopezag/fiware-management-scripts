import requests
from Config.settings import API_KEY_BACKLOG, API_USER_BACKLOG, URL_BACKLOG

__author__ = 'Manuel Escriche'

domain = URL_BACKLOG
auth = API_USER_BACKLOG, API_KEY_BACKLOG


def find_enablersbook():
    url = '{}'.format(domain) + '/api/enablersbook'
    answer = requests.get(url, auth=auth)

    if not answer.ok:
        raise Exception

    return answer.json()['book']


def find_nodesbook():
    url = '{}'.format(domain) + '/api/nodesbook'
    answer = requests.get(url, auth=auth)

    if not answer.ok:
        raise Exception

    return answer.json()['book']


def find_chaptersbook():
    url = '{}'.format(domain) + '/api/chaptersbook'
    answer = requests.get(url, auth=auth)

    if not answer.ok:
        raise Exception

    return answer.json()['book']
