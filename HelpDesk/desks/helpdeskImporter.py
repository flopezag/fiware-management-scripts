from Config.settings import JIRA_USER, JIRA_PASSWORD, JIRA_VERIFY, JIRA_URL, CERTIFICATE
from datetime import datetime
from jira import JIRA
from HelpDesk.platforms.questions import SOF
from logging import info, debug

__author__ = 'Manuel Escriche'


class HelpDeskImporter:
    def __init__(self, domain=JIRA_URL):
        self.base_url = 'https://{}'.format(domain)
        self.user = JIRA_USER
        self.password = JIRA_PASSWORD

        if JIRA_VERIFY is 'False':
            verify_certificate = CERTIFICATE
        else:
            verify_certificate = False

        options = {'server': self.base_url, 'verify': verify_certificate}

        self.jira = JIRA(options=options, basic_auth=(self.user, self.password))
        self.monitors = None
        self.n_transitions = 0
        self.n_monitors = 0
        self.n_assigments = 0

    def get_monitor_url(self, monitor):
        return '{}/browse/{}'.format(self.base_url, monitor.key) if monitor else None

    def get_monitors(self):
        query = 'project in (HELP, HELC)  and issuetype = Monitor'
        self.monitors = sorted(self.jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def update_with(self, questions):
        for question in questions:
            self._update_monitor(question)
            self._create_monitor(question)
            self._assign_monitor(question)

    def update_with_time(self, questions):
        for question in questions:
            self._update_monitor_with_time(question)
            self._create_monitor(question)
            self._assign_monitor(question)

    def _create_monitor(self, question):
        if question.monitor:
            return

        project = 'HELP'
        stamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        description = '\nCreated question in FIWARE Q/A platform on ' + question.added_at.strftime('%d-%m-%Y') + \
                      ' at ' + question.added_at.strftime('%H:%m') + \
                      '\n{color: red}Please, ANSWER this question AT{color} ' + question.url + '\n' + \
                      '\n\n+Question:+\n' + \
                      question.summary + \
                      '\n\n+Description:+\n' + \
                      question.description

        prefix = '[fiware-stackoverflow]' if isinstance(question, SOF) else '[fiware-askbot]'

        issue_dict = {'project': {'key': project},
                      'summary': prefix + ' ' + question.summary,
                      'description': description,
                      'customfield_11000': question.url,
                      'issuetype': {'name': 'Monitor'},
                      'assignee': {'name': None},
                      'labels': question.tags
                      }

        question.monitor = self.jira.create_issue(fields=issue_dict)
        self.jira.remove_watcher(question.monitor, self.user)
        self.n_monitors += 1

        comment = '{}|CREATED monitor | # answers= {}, accepted answer= {}'\
            .format(stamp, question.answer_count, question.is_answered)

        self.jira.add_comment(question.monitor, comment)
        info('--> CREATED ISSUE: {} for question: {}'.format(question.monitor, question))

    def _update_monitor(self, question):
        if not question.monitor:
            return

        stamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        debug('>>>>>> Updating no time question:{} monitor:{} q-url:{}'
              .format(question, question.monitor, question.url))

        status = question.monitor.fields.status.name
        transition = None
        if question.is_answered and status != 'Closed':
            debug('accepted_answer')
            if status == 'Open':
                transition = 'Answer'
            elif status in ('Answered', 'In Progress'):
                transition = 'Finish'
        elif question.answer_count > 0 and status != 'Closed':
            debug('answer_count = {}'.format(question.answer_count))
            if status == 'Open':
                transition = 'Answer'
            elif status == 'In Progress':
                transition = 'Answered'
            elif status == 'Answered':
                pass
                # awaiting = datetime.now() - question.last_activity_at
                # transition = 'Finish' if awaiting.days >= 2 else None
        elif not question.answer_count and status == 'Closed':
            debug('>>>>> Closed issue with no answer: {}, {}, {}'
                  .format(question, question.monitor, question.url))

        debug('transition to={}'.format(transition))
        if transition:
            transitions = self.jira.transitions(question.monitor)
            debug('Available transitions: {}'.format([(t['id'], t['name']) for t in transitions]))
            self.jira.transition_issue(question.monitor, transition)

            comment = '{}|UPDATED status: transition {}| # answers= {}, accepted answer= {}'\
                .format(stamp, transition, question.answer_count, question.is_answered)

            self.jira.add_comment(question.monitor, comment)
            self.n_transitions += 1
            info('--> UPDATE: {} {} from status={} transition={}'
                         .format(question, question.monitor, status, transition))

    def _update_monitor_with_time(self, question):
        if not question.monitor:
            return

        debug('>>>>>> Updating with time question:{} monitor:{} q-url:{}'
              .format(question, question.monitor, question.url))

        status = question.monitor.fields.status.name
        transition = None
        created, now = datetime.strptime(question.monitor.fields.created[:19], '%Y-%m-%dT%H:%M:%S'), datetime.now()
        debug('Status = {}, created = {}, now = {}'.format(status, created, now))
        debug('Is answered = {}, # answers = {}'.format(question.is_answered, question.answer_count))

        if question.is_answered and status != 'Closed':
            debug('->accepted_answer, date= {}'.format(question.answer_date))
            if status == 'Open':
                transition = 'Answer'
            elif status == 'In Progress':
                transition = 'Answered'
            elif status == 'Answered' and question.answer_date:
                debug('answer_date = {}, added_at = {}'.format(question.answer_date, question.added_at))
                transition = 'Finish' if now - created >= question.answer_date - question.added_at else None
        elif question.answer_count > 0 and status != 'Closed':
            debug('->answer_count = {}'.format(question.answer_count))
            if status == 'Open':
                transition = 'Answer'
            elif status == 'In Progress':
                transition = 'Answered'
            elif status == 'Answered':
                pass
                # debug('last_activity_at = {}, added_at {}'
                #                .format(question.last_activity_at, question.added_at))
                # transition = 'Finish' if now - created >= question.last_activity_at - question.added_at  else None
        elif not question.answer_count and status == 'Closed':
            debug('>>>>> Closed issue with no answer: {}, {}, {}'.format(question, question.monitor, question.url))

        debug('transition to={}'.format(transition))
        stamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        if transition:
            transitions = self.jira.transitions(question.monitor)
            debug('Available transitions: {}'.format([(t['id'], t['name']) for t in transitions]))
            self.jira.transition_issue(question.monitor, transition)

            comment = '{}|UPDATED status: transition {}| # answers= {}, accepted answer= {}'\
                .format(stamp, transition, question.answer_count, question.is_answered)

            self.jira.add_comment(question.monitor, comment)
            self.n_transitions += 1
            info('--> UPDATE: {} {} from status={} transition={}'
                 .format(question, question.monitor, status, transition))

    def _assign_monitor(self, question):
        if isinstance(question, SOF):
            if not question.monitor.fields.components:
                question.monitor.update(fields={'components': [{'name': 'FIWARE-TECH-HELP'}]})
                self.n_assigments += 1

    def _clean_monitor(self, question):
        if not question.monitor:
            return

        issue = str(question.monitor)
        question.monitor.delete()
        info('Removed {}'.format(issue))
