from datetime import date, datetime
from Basics.dataFinder import Data
from Basics.nickNames import ContactBook

__author__ = 'Manuel Escriche'


class UrgentDesk:
    def __init__(self):
        self.contactBook = ContactBook()

    def onDeadline(self):
        messages = list()
        for issue in Data().getUrgentDeskOnDeadline():
            summary = issue.fields.summary
            if summary.split('.')[-1] == 'Delivery': continue
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            url = 'http://jira.fiware.org/browse/{}'.format(issue)
            subject = 'FIWARE: Urgent Desk : Deadline = TODAY'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nLet me remind you of the issue {} whose deadline is today.".format(issue) +\
                "\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nUpcoming issues in the Urgent desk are available at\n\thttp://backlog.fiware.org/urgent/upcoming" +\
                "\n\nThanks in advance for cooperation!!" +\
                '\n\nKind Regards,' +\
                '\nFernando'
            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages

    def upcoming(self):
        messages = list()
        for issue in Data().getUrgentDeskUpcoming():
            duedate = datetime.strptime(issue.fields.duedate[:10], '%Y-%m-%d').date()
            timetogo = (duedate - date.today()).days
            if timetogo != 4: continue
            summary = issue.fields.summary
            #if summary.split('.')[-1] == 'Delivery': continue
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            url = 'http://jira.fiware.org/browse/{}'.format(issue)
            subject = 'FIWARE: Urgent Desk : Deadline is Approaching'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nLet me remind you of the issue {} whose deadline is approaching and met in {} days.".format(issue, timetogo) +\
                "\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nUpcoming issues in the Urgent desk are available at\n\thttp://backlog.fiware.org/urgent/upcoming" +\
                "\n\nThanks in advance for cooperation!!" +\
                '\n\nKind Regards,' +\
                '\nFernando'
            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages

    def overdue(self):
        messages = list()
        for issue in Data().getUrgentDeskOverdue():
            duedate = datetime.strptime(issue.fields.duedate[:10], '%Y-%m-%d').date()
            delay = (date.today() - duedate).days
            if delay < 7: continue
            if str(issue) == 'IOT-524': continue

            summary = issue.fields.summary
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            status = issue.fields.status.name
            url = 'http://jira.fiware.org/browse/{}'.format(issue)
            subject = 'FIWARE: Urgent Desk : Overdue Issue'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nLet me remind you of the issue {} which is already delayed {} days.".format(issue, delay) +\
                "\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nOverdue issues in the Urgent desk are available at\n\thttp://backlog.fiware.org/urgent/overdue" +\
                "\n\nI would appreciate you focused on finishing or progressing this item." +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'
            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages

    def impeded(self):
        messages = list()
        for issue in Data().getUrgentDeskImpeded():
            updated = datetime.strptime(issue.fields.updated[:10], '%Y-%m-%d').date()
            noupdated = (date.today() - updated).days
            if noupdated < 7: continue
            #if str(issue) == 'COR-103': continue
            summary = issue.fields.summary
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            url = 'http://jira.fiware.org/browse/{}'.format(issue)
            subject = 'FIWARE: Urgent Desk : Impeded Issue'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nLet me remind you of the issue {} which hasn't been updated for {} days.".format(issue, noupdated) +\
                "\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nImpeded issues in the Urgent desk are available at\n\thttp://backlog.fiware.org/urgent/impeded" +\
                "\n\nI would appreciate you verified its blocking condition persist." +\
                "\n\tif not, please, move it back to In Progress" +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'
            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))

        return messages


if __name__ == "__main__":
    pass