__author__ = 'Manuel Escriche'

import requests

#domain = 'http://127.0.0.1:5000'
domain = 'http://backlog.fiware.org'

auth = 'api', 'adc842f790105942e095f5f77484ffa8242a2ec3'

def find_enablersBook():
    url = '{}'.format(domain) + '/api/enablersbook'
    answer =  requests.get(url, auth=auth)
    if not answer.ok: raise Exception
    return answer.json()['book']


def find_nodesBook():
    url = '{}'.format(domain) + '/api/nodesbook'
    answer =  requests.get(url, auth=auth)
    if not answer.ok: raise Exception
    return answer.json()['book']


def find_chaptersBook():
    url = '{}'.format(domain) + '/api/chaptersbook'
    answer =  requests.get(url, auth=auth)
    if not answer.ok: raise Exception
    return answer.json()['book']