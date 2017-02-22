
import re
import logging
from jira import JIRA
# from settings import settings
from Basics.settings import JIRA_USER, JIRA_PASSWORD

__author__ = 'Manuel Escriche'

accelerators_dict = {'Fiware-finodex-coaching': 'FINODEX',
                     'Fiware-fractals-coaching': 'FRACTALS',
                     'Fiware-soulfi-coaching': 'SOUL-FI',
                     'Fiware-incense-coaching': 'INCENSe',
                     'Fiware-finish-coaching': 'Finish',
                     'Fiware-creatifi-coaching': 'CreatiFI',
                     'Fiware-ceedtech-coaching': 'CEED-Tech',
                     'Fiware-europeanpioneers-coaching': 'EuropeanPioneers',
                     'Fiware-fabulous-coaching': 'FABulous',
                     'Fiware-fiadopt-coaching': 'FI-ADOPT',
                     'Fiware-fic3-coaching': 'FI-C3',
                     'Fiware-fiche-coaching': 'FICHe',
                     'Fiware-frontiercities-coaching': 'FrontierCities',
                     'Fiware-impact-coaching': 'IMPACT',
                     'Fiware-smartagrifood-coaching': 'SmartAgriFood2',
                     'Fiware-speedup-coaching': 'SpeedUp Europe',
                     'Fiware-odine-coaching': 'ODINE'
                     }


class CoachesHelpDesk:
    def __init__(self, domain='jira.fiware.org'):
        self.base_url = 'https://{}'.format(domain)
        self.user = JIRA_USER
        self.password = JIRA_PASSWORD
        options = {'server': self.base_url, 'verify': False}
        self.jira = JIRA(options=options, basic_auth=(self.user, self.password))
        self.n_assignment = 0
        self.n_clones = 0
        self.n_renamed = 0

    def assign_request(self):
        query = 'project = HELC AND issuetype = extRequest AND component = EMPTY'
        requests = sorted(self.jira.search_issues(query, maxResults=False), key=lambda item: item.key)
        for request in requests:
            summary = request.fields.summary
            if re.search(r'\[SPAM\]', summary):
                request.update(fields={'components': [{'name': 'SPAM'}]})
                continue
            match = re.search(r'\[[^\]]+?\]', summary)
            if match:
                accelerator = match.group(0)[1:-1]
                if accelerator in accelerators_dict:
                    components = {'name': accelerators_dict[accelerator]}
                    # request.update(fields={'components':[components]}, assignee={'name': '-1'})
                    request.update(fields={'components': [components]})

                    if not request.fields.assignee:
                        self.jira.assign_issue(request, '-1')

                    self.n_assignment += 1
                    logging.info('updated request {}, accelerator= {}'.format(request, accelerator))

    def clone_to_main(self):
        self._clone_tech()
        self._clone_lab()

    def _clone_tech(self):
        query = 'project = HELC AND issuetype = extRequest AND component = _TECH_ AND not assignee = EMPTY'
        requests = sorted(self.jira.search_issues(query, maxResults=False), key=lambda item: item.key)

        for request in requests:
            fields = {'project': {'key': 'HELP'},
                      'components': [{'name': 'FIWARE-TECH-HELP'}],
                      'summary': request.fields.summary,
                      'description': request.fields.description,
                      'issuetype': {'name': request.fields.issuetype.name},
                      'priority': {'name': request.fields.priority.name},
                      'labels': request.fields.labels,
                      'assignee': {'name': None},
                      'reporter': {'name': request.fields.reporter.name}
                      }
            new_issue = self.jira.create_issue(fields=fields)

            self.jira.create_issue_link('relates to', new_issue, request)
            self.jira.add_watcher(new_issue, request.fields.assignee.name)
            self.jira.remove_watcher(new_issue, self.user)

            components = [{'name': comp.name} for comp in request.fields.components if comp.name != '_TECH_']
            request.update(fields={'components': components})

            # self.jira.add_watcher(new_issue, request.fields.assignee.name)
            logging.info('CREATED TECH ISSUE: {} from {}'.format(new_issue, request))
            self.n_clones += 1

    def _clone_lab(self):
        query = 'project = HELC AND issuetype = extRequest AND component = _LAB_ AND not assignee = EMPTY'
        requests = sorted(self.jira.search_issues(query, maxResults=False), key=lambda item: item.key)

        for request in requests:
            fields = {'project': {'key': 'HELP'},
                      'components': [{'name': 'FIWARE-LAB-HELP'}],
                      'summary': request.fields.summary,
                      'description': request.fields.description,
                      'issuetype': {'name': request.fields.issuetype.name},
                      'priority': {'name': request.fields.priority.name},
                      'labels': request.fields.labels,
                      'assignee': {'name': None},
                      'reporter': {'name': request.fields.reporter.name}
                      }
            new_issue = self.jira.create_issue(fields=fields)

            self.jira.create_issue_link('relates to', new_issue, request)
            self.jira.add_watcher(new_issue, request.fields.assignee.name)
            self.jira.remove_watcher(new_issue, self.user)

            components = [{'name': comp.name} for comp in request.fields.components if comp.name != '_LAB_']
            request.update(fields={'components': components})

            logging.info('CREATED LAB ISSUE: {} from {}'.format(new_issue, request))
            self.n_clones += 1

    def naming(self):
        query = 'project = HELC AND issuetype = extRequest AND status = Closed and updated >= -1d'
        requests = sorted(self.jira.search_issues(query, maxResults=False), key=lambda item: item.key)
        for request in requests:
            component = request.fields.components[0].name
            summary = request.fields.summary

            if re.match(r'FIWARE.Request.Coach.{}'.format(component), summary):
                continue

            summary = re.sub(r'\[[^\]]+?\]', '', summary)
            summary = 'FIWARE.Request.Coach.{}.{}'.format(component, summary.strip())
            request.update(summary=summary)
            logging.info('{} {} {} {}'.format(request, request.fields.status, component, summary))
            self.n_renamed += 1
