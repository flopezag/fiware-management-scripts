from requests import get
from Config.settings import API_KEY_BACKLOG, API_USER_BACKLOG, URL_BACKLOG

__author__ = 'Manuel Escriche'

domain = URL_BACKLOG
auth = API_USER_BACKLOG, API_KEY_BACKLOG


def find_deliveryboard():
    url = '{}'.format(domain) + '/api/deliveryboard/pending'
    answer = get(url, auth=auth)

    if not answer.ok:
        raise Exception

    return answer.json()['book']


def find_all_trackers():
    url = '{}'.format(domain) + '/api/trackersbook/all'
    answer = get(url, auth=auth)

    if not answer.ok:
        raise Exception

    return answer.json()['trackers']


def find_nodesk_trackers():
    url = '{}'.format(domain) + '/api/trackersbook/nodesk'
    answer = get(url, auth=auth)

    if not answer.ok:
        raise Exception

    return answer.json()['trackers']
