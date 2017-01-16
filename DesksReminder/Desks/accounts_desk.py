__author__ = 'Manuel Escriche'

from datetime import date, datetime
from Basics.dataFinder import Data
from Basics.nickNames import ContactBook

class AccountsDesk:
    def __init__(self):
        self.contactBook = ContactBook()

    def open(self):
        messages = list()
        for issue in Data().getAccountsDeskOpen():
            created = datetime.strptime(issue.fields.created[:10], '%Y-%m-%d').date()
            unanswered = (date.today() - created).days
            if unanswered <= 1: continue
            summary = issue.fields.summary
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            url = 'http://jira.fiware.org/browse/{}'.format(issue)
            subject = 'FIWARE: Accounts Desk : Open Issue'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nI noticed the issue {} is still OPEN, i.e. not replied for {} days.".format(issue, unanswered) +\
                "\nLet me remind you of our rule to reply in the first 24 hours during working days." +\
                "\nI would appreciate you spent a minute to reply to this request and to progress it on its workflow." +\
                "\n\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nIssues in the Accounts Desk are available at\n\thttp://backlog.fiware.org/lab/upgradeAccount" +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'
            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages

    def inProgress(self):
        messages = list()
        for issue in Data().getAccountsDeskInProgress():
            updated = datetime.strptime(issue.fields.updated[:10], '%Y-%m-%d').date()
            noupdated = (date.today() - updated).days
            if noupdated < 7: continue
            summary = issue.fields.summary
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            url = 'http://jira.fiware.org/browse/{}'.format(issue)
            subject = 'FIWARE: Accounts Desk: stalled Issue?'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nI noticed issue {} is In Progress but no update happened in the last {} days.".format(issue, noupdated) +\
                "\nI would appreciate you spent a minute to update it by reporting its progress in a comment" +\
                "\n\tor if ready for analysing, please, evolve it" +\
                "\n\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nIssues in the Accounts Desk are available at\n\thttp://backlog.fiware.org/lab/upgradeAccount" +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'
            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages

    def scheduled(self):
        messages = list()
        for issue in Data().getAccountsDeskScheduled():
            updated = datetime.strptime(issue.fields.updated[:10], '%Y-%m-%d').date()
            noupdated = (date.today() - updated).days
            if noupdated < 7: continue
            summary = issue.fields.summary
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            url = 'http://jira.fiware.org/browse/{}'.format(issue)
            subject = 'FIWARE: Accounts Desk: stalled Issue?'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nI noticed issue {} is Scheduled but no update happened in the last {} days.".format(issue, noupdated) +\
                "\nI would appreciate you spent a minute to update it by reporting its progress in a comment" +\
                "\n\tor if ready for Answered, please, evolve it" +\
                "\n\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nIssues in the Accounts Desk are available at\n\thttp://backlog.fiware.org/lab/upgradeAccount" +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'
            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages

    def answered(self):
        messages = list()
        for issue in Data().getAccountsDeskAnswered():
            updated = datetime.strptime(issue.fields.updated[:10], '%Y-%m-%d').date()
            noupdated = (date.today() - updated).days
            if noupdated < 7: continue
            summary = issue.fields.summary
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            url = 'http://jira.fiware.org/browse/{}'.format(issue)
            subject = 'FIWARE: Accounts Desk: Closed Issue?'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nI noticed issue {} has been Answered but no update happened in the last {} days.".format(issue, noupdated) +\
                "\nI would appreciate you spent a minute to close it" \
                "\n\tor if the exchange continues, please, update its progress in a comment" \
                "\n\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nIssues in the Accounts Desk are available at\n\thttp://backlog.fiware.org/lab/upgradeAccount" +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'
            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages

    def rejected(self):
        messages = list()
        for issue in Data().getAccountsDeskRejected():
            updated = datetime.strptime(issue.fields.updated[:10], '%Y-%m-%d').date()
            noupdated = (date.today() - updated).days
            if noupdated < 1: continue
            summary = issue.fields.summary
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            url = 'http://jira.fiware.org/browse/{}'.format(issue)
            subject = 'FIWARE: Accounts Desk: Close the procedure'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nI noticed issue {} has been Rejected.".format(issue) +\
                "\nI would appreciate you spent a minute to close the procedure" \
                "\n\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nIssues in the Accounts Desk are available at\n\thttp://backlog.fiware.org/lab/upgradeAccount" +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'
            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages


if __name__ == "__main__":
    pass
