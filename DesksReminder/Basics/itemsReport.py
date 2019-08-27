from Config.settings import JIRA_URL

__author__ = 'Manuel Escriche'


def getTextMessagesReport(messages):
    if len(messages):
        result = ''.join(
            map(lambda x: '\n\t\t* {}, {}, {}'.format(x['issue'].key, x['displayname'].encode('utf-8'), x['summary']),
                messages))
    else:
        result = '>>>> No issues found to be reminded of.'

    return result


def getHtmlMessagesReport(messages):
    return '\n'.join('#{0}, <a href="http://{4}/browse/{1}">{1}</a>, '
                     '{2}, {3}<br>'.format(n,
                                           item['issue'].key,
                                           item['displayname'],
                                           item['summary'].encode('utf-8'),
                                           JIRA_URL)
                     for n, item in enumerate(messages.encode('utf-8'))) \
        if len(messages) else '>>>> No issues found to be reminded of. <br>'
