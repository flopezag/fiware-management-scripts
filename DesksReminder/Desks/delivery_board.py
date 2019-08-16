import logging
from datetime import date, datetime
from DesksReminder.Basics.dataFinder import Data
from DesksReminder.Basics.nickNames import ContactBook

__author__ = 'Manuel Escriche'


class DeliveryBoard:
    def __init__(self):
        self.contactBook = ContactBook()

    def upcoming(self):
        book = Data().getDeliveryBoardPending()
        delbook = {str(book[item]): item for item in book}
        data = list()
        for issue in book.values():
            try:
                duedate = datetime.strptime(issue.fields.duedate[:10], '%Y-%m-%d').date()
                # assignee = issue.fields.assignee
            except:
                logging.info('issue {} has not duedate or assignee field'.format(issue))
                continue
            targetslot = (duedate - date.today()).days
            status = issue.fields.status.name

            if targetslot >= 10 and targetslot <= 30 and status != 'Closed':
                data.append(issue)

        messages = list()
        for issue in data:
            url = 'http://jira.fiware.org/browse/{}'.format(issue)
            duedate = datetime.strptime(issue.fields.duedate[:10], '%Y-%m-%d').date()
            targetslot = (duedate - date.today()).days
            summary = issue.fields.summary
            displayName = issue.fields.assignee.displayName.strip()
            nickName = self.contactBook.getNickName(displayName)
            emailAddress = issue.fields.assignee.emailAddress

            deliverable = delbook[str(issue)]

            subject = 'FIWARE: Delivery Board : Coming deadline'

            message = 'Dear {},'.format(nickName.encode('utf-8')) +\
                "\n\nLet me remind you of deliverable {} associated with issue {} " \
                "whose deadline is met in {} days.".format(deliverable, issue, targetslot) +\
                "\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nThe Deliverable dashboard is available at\n\thttp://backlog.fiware.org/delivery/dashboard" +\
                "\n\nI would appreciate you focused on providing deliverable {} on time.".format(deliverable) +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'

            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=emailAddress, nickname=nickName.encode('utf-8'), displayname=displayName,
                                 subject=subject, body=message))
        return messages


if __name__ == "__main__":
    pass
