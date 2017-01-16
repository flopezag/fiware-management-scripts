__author__ = 'Manuel Escriche'


def getTextMessagesReport(messages):
    return '\n\t'.join('#{}, {}, {}, {}'.format(n, item['issue'].key,
                                                item['displayname'],
                                                item['summary']) for n,item in enumerate(messages)) \
    if len(messages) else  '>>>> No issues found to be reminded of.'

def getHtmlMessagesReport(messages):
    return '\n'.join('#{0}, <a href="http://jira.fiware.org/browse/{1}">{1}</a>, '
                     '{2}, {3}<br>'.format(n, item['issue'].key,
                                           item['displayname'],
                                           item['summary'])
                     for n,item in enumerate(messages)) \
        if len(messages) else  '>>>> No issues found to be reminded of. <br>'