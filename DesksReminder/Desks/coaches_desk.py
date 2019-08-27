from datetime import date, datetime
from DesksReminder.Basics.dataFinder import Data
from DesksReminder.Basics.nickNames import ContactBook
from Config.settings import JIRA_URL

__author__ = 'Manuel Escriche'


class CoachesHelpDesk:
    def __init__(self):
        self.contactBook = ContactBook()

    def open(self):
        messages = list()
        for issue in Data().getCoachesHelpDeskOpen():
            created = datetime.strptime(issue.fields.created[:10], '%Y-%m-%d').date()
            unanswered = (date.today() - created).days

            if unanswered <= 1:
                continue

            summary = issue.fields.summary
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            # status = issue.fields.status.name
            url = 'http://{}/browse/{}'.format(JIRA_URL, issue)
            subject = 'FIWARE: Coaches Help Desk : Open Issue'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nI noticed the issue {} is still OPEN, i.e. not replied for {} days.".format(issue, unanswered) +\
                "\nLet me remind you of our rule to reply in the first 24 hours during working days." +\
                "\nI would appreciate you spent a minute to reply to this request and to evolve its status" +\
                "\n\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nIssues in the Coaches Help Desk are available at\n\thttp://backlog.fiware.org/helpdesk/coaches" +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'

            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages

    def inProgress(self):
        messages = list()
        for issue in Data().getCoachesHelpDeskInProgress():
            updated = datetime.strptime(issue.fields.updated[:10], '%Y-%m-%d').date()
            noupdated = (date.today() - updated).days

            if noupdated < 7:
                continue

            summary = issue.fields.summary
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            url = 'http://{}/browse/{}'.format(JIRA_URL, issue)
            subject = 'FIWARE: Coaches Help Desk: stalled Issue?'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nI noticed issue {} is In Progress but no update happened in the last {} days.".format(issue,
                                                                                                           noupdated) +\
                "\nI would appreciate you spent a minute to update it by reporting its progress in a comment" \
                "\n\tor if there were a blocking condition, please, report it in a comment and evolve " \
                "its status to Impeded." +\
                "\n\tor if it was answered, please, evolve its status." +\
                "\n\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nIssues in the Coaches Help Desk are available at\n\thttp://backlog.fiware.org/helpdesk/coaches" +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'

            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages

    def answered(self):
        messages = list()
        for issue in Data().getCoachesHelpDeskAnswered():
            updated = datetime.strptime(issue.fields.updated[:10], '%Y-%m-%d').date()
            noupdated = (date.today() - updated).days

            if noupdated < 4:
                continue

            summary = issue.fields.summary
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            url = 'http://{}/browse/{}'.format(JIRA_URL, issue)
            subject = 'FIWARE: Coaches Help Desk: Closed Issue?'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nI noticed issue {} has been Answered but no update happened " \
                "in the last {} days.".format(issue, noupdated) +\
                "\nI would appreciate you spent a minute to close it" \
                "\n\tor if the exchange continues, please, update its progress in a comment" \
                "\n\tor if there were a blocking condition, please, report it in a comment and " \
                "evolve its status to Impeded." +\
                "\n\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nIssues in the Coaches Help Desk are available at\n\thttp://backlog.fiware.org/helpdesk/coaches" +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'

            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages

    def impeded(self):
        messages = list()
        for issue in Data().getCoachesHelpDeskImpeded():
            updated = datetime.strptime(issue.fields.updated[:10], '%Y-%m-%d').date()
            noupdated = (date.today() - updated).days

            if noupdated < 7:
                continue

            summary = issue.fields.summary
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            url = 'http://{}/browse/{}'.format(JIRA_URL, issue)
            subject = 'FIWARE: Coaches Help Desk: Impeded Issue?'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nI noticed issue {} is Impeded but no update happened in the last {} days.".format(issue,
                                                                                                       noupdated) +\
                "\nI would appreciate you spent a minute to check its blocking condition persist:" \
                "\n\tif so, please, add a comment stating it" \
                "\n\tif not, please, get it back to In Progress, and address it" +\
                "\n\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nIssues in the Coaches Help Desk are available at\n\thttp://backlog.fiware.org/helpdesk/coaches" +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'

            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages


if __name__ == "__main__":
    pass
