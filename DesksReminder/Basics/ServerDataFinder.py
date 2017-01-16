__author__ = 'Manuel Escriche'

import requests

#domain = 'http://127.0.0.1:5000'
domain = 'http://backlog.fiware.org'

auth = 'api', 'adc842f790105942e095f5f77484ffa8242a2ec3'
def find_deliveryboard():
    url = '{}'.format(domain) + '/api/deliveryboard/pending'
    answer =  requests.get(url, auth=auth)
    if not answer.ok: raise Exception
    return answer.json()['book']

def find_all_trackers():
    url = '{}'.format(domain) + '/api/trackersbook/all'
    answer =  requests.get(url, auth=auth)
    if not answer.ok: raise Exception
    return answer.json()['trackers']

def find_nodesk_trackers():
    url = '{}'.format(domain) + '/api/trackersbook/nodesk'
    answer =  requests.get(url, auth=auth)
    if not answer.ok: raise Exception
    return answer.json()['trackers']