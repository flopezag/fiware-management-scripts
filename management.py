from logging import _nameToLevel as nameToLevel
from argparse import ArgumentParser
from Common.emailer import Emailer
from DesksReminder.reminders import HelpDeskTechReminder, HelpDeskLabReminder, HelpDeskOtherReminder, \
                                    UrgentDeskReminder, AccountsDeskReminder
from HelpDesk.synchronization import AskbotSync, HelpDeskCaretaker
from HelpDesk.stackoverflowsync import StackOverflowSync
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

__author__ = 'Fernando López'
__version__ = "1.3.0"


def init():
    parser = ArgumentParser(prog='Jira Management Scripts', description='')
    parser.add_argument('-l', '--log',
                        default='INFO',
                        help='The logging level to be used.')

    args = parser.parse_args()
    loglevel = None

    try:
        loglevel = nameToLevel[args.log.upper()]
    except Exception as e:
        print('Invalid log level: {}'.format(args.log))
        print('Please use one of the following values:')
        print('   * CRITICAL')
        print('   * ERROR')
        print('   * WARNING')
        print('   * INFO')
        print('   * DEBUG')
        print('   * NOTSET')
        exit()

    return loglevel


if __name__ == "__main__":
    loglevel = init()

    mailer = Emailer(loglevel=loglevel)

    disable_warnings(InsecureRequestWarning)

    # Send reminder of pending JIRA tickets
    techReminder = HelpDeskTechReminder(loglevel=loglevel, mailer=mailer)
    techReminder.process()

    labReminder = HelpDeskLabReminder(loglevel=loglevel, mailer=mailer)
    labReminder.process()

    otherReminder = HelpDeskOtherReminder(loglevel=loglevel, mailer=mailer)
    otherReminder.process()

    urgentReminder = UrgentDeskReminder(loglevel=loglevel, mailer=mailer)
    urgentReminder.process()

    accountReminder = AccountsDeskReminder(loglevel=loglevel, mailer=mailer)
    accountReminder.process()

    # Askbot synchronization and Jira caretaker actions
    askbotSync = AskbotSync(loglevel=loglevel)
    askbotSync.process()
    
    helpdeskCaretaker = HelpDeskCaretaker(loglevel=loglevel)
    helpdeskCaretaker.process()

    # StackoverFlow synchronization
    stackoverflowSync = StackOverflowSync(loglevel=loglevel)
    stackoverflowSync.process(year=2015, month=9, day=21)
