from logging import info
from datetime import date, datetime
from DesksReminder.Basics.dataFinder import Data
from DesksReminder.Basics.nickNames import ContactBook
from Config.settings import JIRA_URL

__author__ = 'Manuel Escriche'


class DeliveryBoard:
    def __init__(self):
        self.contactBook = ContactBook()

    def upcoming(self):
        book = Data().getDeliveryBoardPending()
        del_book = {str(book[item]): item for item in book}
        data = list()
        for issue in book.values():
            try:
                due_date = datetime.strptime(issue.fields.duedate[:10], '%Y-%m-%d').date()
                # assignee = issue.fields.assignee
            except:
                info('issue {} has not duedate or assignee field'.format(issue))
                continue
            target_slot = (due_date - date.today()).days
            status = issue.fields.status.name

            if target_slot >= 10 and target_slot <= 30 and status != 'Closed':
                data.append(issue)

        messages = list()
        for issue in data:
            url = 'http://{}/browse/{}'.format(JIRA_URL, issue)
            due_date = datetime.strptime(issue.fields.duedate[:10], '%Y-%m-%d').date()
            target_slot = (due_date - date.today()).days
            summary = issue.fields.summary
            display_name = issue.fields.assignee.displayName.strip()
            nick_name = self.contactBook.getNickName(display_name)
            email_address = issue.fields.assignee.emailAddress

            deliverable = del_book[str(issue)]

            subject = 'FIWARE: Delivery Board : Coming deadline'

            message = 'Dear {},'.format(nick_name.encode('utf-8')) +\
                "\n\nLet me remind you of deliverable {} associated with issue {} " \
                "whose deadline is met in {} days.".format(deliverable, issue, target_slot) +\
                "\nIssue Summary: {}".format(summary.encode('utf-8')) +\
                "\nYou can access it at {}".format(url) +\
                "\n\nThe Deliverable dashboard is available at\n\thttp://backlog.fiware.org/delivery/dashboard" +\
                "\n\nI would appreciate you focused on providing deliverable {} on time.".format(deliverable) +\
                '\n\nThanks in advance for cooperation!!' +\
                '\n\nKind Regards,' +\
                '\nFernando'

            messages.append(dict(issue=issue, summary=summary.encode('utf-8'),
                                 email=email_address, nickname=nick_name.encode('utf-8'), displayname=display_name,
                                 subject=subject, body=message))
        return messages


if __name__ == "__main__":
    pass
