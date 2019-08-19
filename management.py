import os
import logging
import argparse
from Util.emailer import Emailer

__author__ = 'Fernando López'


def init(¡):
    parser = argparse.ArgumentParser(prog='Jira Management Scripts', description='')
    parser.add_argument('-l', '--log',
                        default='INFO',
                        help='The logging level to be used.')

    args = parser.parse_args()
    loglevel = getattr(logging, args.log.upper(), None)

    if not isinstance(log_level, int):
        print('Invalid log level: {}'.format(args.log))
        exit()

    return loglevel


if __name__ == "__main__":
    loglevel = init()

    mailer = Emailer(loglevel=loglevel)

    techReminder = HelpDeskTechReminder(loglevel=loglevel, mailer=mailer)
    techReminder.process()

    labReminder = HelpDeskLabReminder(loglevel=loglevel, mailer=mailer)
    labReminder.process()

    otherReminder = HelpDeskOtherReminder(loglevel=loglevel, mailer=mailer)
    otherReminder.process()

    urgentReminder = UrgentDeskReminder(loglevel=loglevel, mailer=mailer)
    urgentReminder.process()
    '''

    accountReminder = AccountsDeskReminder(loglevel=log_level, mailer=mailer)
    accountReminder.process()
    '''

    parser = argparse.ArgumentParser(prog='Askbot', description='Synchronising scripts')
    parser.add_argument('-l', '--log',
                        default='INFO',
                        help='The logging level to be used.')

    args = parser.parse_args()
    log_level = getattr(logging, args.log.upper(), None)

    if not isinstance(log_level, int):
        print('Invalid log level: {}'.format(args.log))
        exit()

    accountReminder = AskbotSync(loglevel=log_level)
    accountReminder.process()

    helpdeskCaretaker = HelpDeskCaretaker(loglevel=log_level)
    helpdeskCaretaker.process()


    parser = argparse.ArgumentParser(prog='StackOverflow', description='StackOverflow synchronising script')
    parser.add_argument('-l', '--log',
                        default='INFO',
                        help='The logging level to be used.')

    args = parser.parse_args()

    log_level = getattr(logging, args.log.upper(), None)
    if not isinstance(log_level, int):
        print('Invalid log level: {}'.format(args.log))
        print('Please use one of the following values:')
        print('   * CRITICAL')
        print('   * ERROR')
        print('   * WARNING')
        print('   * INFO')
        print('   * DEBUG')
        print('   * NOTSET')
        exit()

    stackoverflowSync = StackOverflowSync()

    stackoverflowSync.get_stack_monitor()

    dividing_day = datetime(year=2015, month=9, day=21)

    stackoverflowSync.questions_with_no_answer(partition_date=dividing_day)
    stackoverflowSync.questions_with_answers(partition_date=dividing_day)

    stackoverflowSync.get_answers()

    logging.info('helpdesk: # issues created = {}'.format(stackoverflowSync.get_number_issues_created()))
    logging.info('helpdesk: # issues transitions = {}'.format(stackoverflowSync.get_number_transitions()))
    logging.info('helpdesk: # issues assignments = {}'.format(stackoverflowSync.get_number_assignments()))
    logging.info('stackoverflow questions= {}'.format(stackoverflowSync.get_questions()))

    stackoverflowSync.close_log_file()
