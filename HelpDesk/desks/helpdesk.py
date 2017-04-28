import logging
import re
from itertools import ifilterfalse
from jira import JIRA
from .resourcesBooks import find_enablersbook, find_nodesbook, find_chaptersbook
from Basics.emailer import Emailer
from Basics.settings import JIRA_USER, JIRA_PASSWORD
from logging import INFO, DEBUG

__author__ = 'Manuel Escriche'

channels = {'Fiware-smart-cities-req': 'FIWARE-SMART-CITIES-REQ',
            'Fiware-tech-help': 'FIWARE-TECH-HELP',
            'Fiware-general-help': 'FIWARE-GENERAL-HELP',
            'Fiware-open-data-req': 'FIWARE-OPEN-DATA-REQ',
            'Fiware-mundus-req': 'FIWARE-MUNDUS-REQ',
            'Fiware-speakers-req': 'FIWARE-SPEAKERS-REQ',
            'Fiware-collaboration-req': 'FIWARE-COLLABORATION-REQ',
            'Fiware-feedback': 'FIWARE-FEEDBACK',
            'Fiware-lab-help': 'FIWARE-LAB-HELP',
            'Fiware-training-req': 'FIWARE-TRAINING-REQ',
            'Fiware-ops-help': 'FIWARE-OPS-HELP',
            'SPAM': 'SPAM'
            }

keywords = {'FIWARE-TECH-HELP': 'Tech',
            'FIWARE-GENERAL-HELP': 'General',
            'FIWARE-SMART-CITIES-REQ': 'SmartCities',
            'FIWARE-OPEN-DATA-REQ': 'OpenData',
            'FIWARE-MUNDUS-REQ': 'Mundus',
            'FIWARE-COLLABORATION-REQ': 'Collabora',
            'FIWARE-SPEAKERS-REQ': 'Speaker',
            'FIWARE-FEEDBACK': 'Feedback',
            'FIWARE-LAB-HELP': 'Lab',
            'FIWARE-TRAINING-REQ': 'Training',
            'FIWARE-OPS-HELP': 'Ops'}

noTechChannels = ('FIWARE-GENERAL-HELP', 'FIWARE-SMART-CITIES-REQ', 'FIWARE-OPEN-DATA-REQ', 'FIWARE-MUNDUS-REQ',
                  'FIWARE-COLLABORATION-REQ', 'FIWARE-SPEAKERS-REQ', 'FIWARE-FEEDBACK', 'FIWARE-TRAINING-REQ',
                  'FIWARE-OPS-HELP')

issuetypedict = {'Monitor': 'Question', 'extRequest': 'Request'}


class HelpDesk:
    def __init__(self, domain='jira.fiware.org'):
        self.base_url = 'https://{}'.format(domain)
        self.user = JIRA_USER
        self.password = JIRA_PASSWORD
        options = {'server': self.base_url, 'verify': False}
        self.jira = JIRA(options=options, basic_auth=(self.user, self.password))
        self.emailer = Emailer(log_level=DEBUG)
        self.enablersBook = find_enablersbook()
        self.nodesBook = find_nodesbook()
        self.chaptersBook = find_chaptersbook()
        self.n_assignments = 0
        self.n_channeled = 0
        self.n_removed = 0
        self.n_renamed = 0

    def _change_channel(self):
        query = 'project = HELP AND issuetype in (extRequest, Monitor) ' \
                'AND component in (FIWARE-TECH-HELP, FIWARE-LAB-HELP) and updated >= -1d'
        inrequests = sorted(self.jira.search_issues(query, maxResults=25), key=lambda item: item.key)
        # issues changed to LAB channel when node has been set up
        # HD node    = issue.fields.customfield_11104
        requests = filter(lambda x: x.fields.components[0].name == 'FIWARE-TECH-HELP', inrequests)
        condition = lambda x: x.fields.customfield_11104 and not \
            x.fields.customfield_11103 and not \
            x.fields.customfield_11105 and\
            x.fields.customfield_11104.value != 'Unknown'

        for issue in filter(condition, requests):
            enabler = issue.fields.customfield_11105

            if enabler and enabler.value != 'Unknown':
                continue

            chapter = issue.fields.customfield_11103

            if chapter and chapter.value != 'Unknown':
                continue

            issue.update(fields={'components': [{'name': 'FIWARE-LAB-HELP'}]})
            logging.info('update issue= {} - change to LAB channel')

        # issues changed to TECH channel when enabler or chapter has been set up
        # HD enabler = issue.fields.customfield_11105
        requests = filter(lambda x: x.fields.components[0].name == 'FIWARE-LAB-HELP', inrequests)
        condition = lambda x: x.fields.customfield_11105 and not \
            x.fields.customfield_11104 and \
            x.fields.customfield_11105.value != 'Unknown'

        for issue in filter(condition, requests):
            node = issue.fields.customfield_11104

            if node and node.value != 'Unknown':
                continue

            issue.update(fields={'components': [{'name': 'FIWARE-TECH-HELP'}]})
            logging.info('update issue= {} - change to TECH channel'.format(issue))

        # HD chapter = issue.fields.customfield_11103
        condition = lambda x: x.fields.customfield_11103 and not \
            x.fields.customfield_11104 and \
            x.fields.customfield_11103.value != 'Unknown'

        for issue in filter(condition, requests):
            node = issue.fields.customfield_11104

            if node and node.value != 'Unknown':
                continue

            issue.update(fields={'components': [{'name': 'FIWARE-TECH-HELP'}]})
            logging.info('update issue= {} - change to TECH channel'.format(issue))

    def _assign_tech_channel(self):
        query = 'project = HELP AND issuetype in (extRequest, Monitor) ' \
                'AND component = FIWARE-TECH-HELP AND status != Closed AND assignee = EMPTY and updated >= -1d'

        requests = sorted(self.jira.search_issues(query, maxResults=25), key=lambda item: item.key)

        # HD chapter = issue.fields.customfield_11103
        # HD node    = issue.fields.customfield_11104
        # HD enabler = issue.fields.customfield_11105

        # make fields visible with value 'Unknown'
        condition = lambda x: not x.fields.customfield_11103 and not \
            x.fields.customfield_11104 and not \
            x.fields.customfield_11105

        for issue in filter(condition, requests):
            enabler_values = self.jira.editmeta(issue)['fields']['customfield_11105']['allowedValues']
            enabler = next(filter(lambda x: x['value'] == 'Unknown', enabler_values))

            chapter_values = self.jira.editmeta(issue)['fields']['customfield_11103']['allowedValues']
            chapter = next(filter(lambda x: x['value'] == 'Unknown', chapter_values))

            node_values = self.jira.editmeta(issue)['fields']['customfield_11104']['allowedValues']
            node = next(filter(lambda x: x['value'] == 'Unknown', node_values))

            issue.update(fields={'customfield_11103': chapter, 'customfield_11104': node, 'customfield_11105': enabler})

            logging.info('update issue: issue= {} node={}, chapter={}, enabler={}'.format(issue,
                                                                                          node['value'],
                                                                                          chapter['value'],
                                                                                          enabler['value']))

        # assign issues whose enabler has been set up, chapter is also filled consistently
        # HD enabler = issue.fields.customfield_11105
        condition = lambda x: x.fields.customfield_11105 and x.fields.customfield_11105.value != 'Unknown'

        for issue in filter(condition, requests):
            enabler = issue.fields.customfield_11105.value
            if enabler in self.enablersBook:
                chapter_values = self.jira.editmeta(issue)['fields']['customfield_11103']['allowedValues']
                chapter = next(filter(lambda x: x['value'] == self.enablersBook[enabler]['chapter'], chapter_values))

                if chapter:
                    issue.update(fields={'customfield_11103': chapter})

                component = self.jira.component(self.enablersBook[enabler]['component'])
                assignee = component.assignee.name
                self.jira.assign_issue(issue, assignee=assignee)

                logging.info('assign issue= {} enabler={} chapter={} assignee={}'
                             .format(issue, enabler, chapter['value'], assignee))
            else:
                message = 'Dear Help Desk Caretaker Admin,' +\
                    "\n\nPlease, have a look at '{}' Enabler " \
                    "because it wasn't found in the Enablers book.".format(enabler) +\
                    '\n\nThanks in advance for cooperation!!' +\
                    '\n\nKind Regards,' +\
                    '\nFernando'
                self.emailer.send_adm_msg('Unknown Enabler: {}'.format(enabler), message)

        # assign issues for chapter leaders, enabler field is not assigned
        # HD enabler = issue.fields.customfield_11105
        # HD chapter = issue.fields.customfield_11103
        condition = lambda x: x.fields.customfield_11103 and x.fields.customfield_11103.value != 'Unknown'

        for issue in filter(condition, requests):
            enabler = issue.fields.customfield_11105
            if enabler and enabler.value != 'Unknown':
                continue

            chapter = issue.fields.customfield_11103.value

            if chapter in self.chaptersBook:
                component = self.jira.component(self.chaptersBook[chapter]['coordination_key'])
                assignee = component.assignee.name
                self.jira.assign_issue(issue, assignee=assignee)
                logging.info('assign issue= {} chapter={} assignee={}'.format(issue, chapter, assignee))
            else:
                message = 'Dear Help Desk Caretaker Admin,' +\
                    "\n\nPlease, have a look at {} Chapter " \
                    "because it wasn't found in the Chapters book.".format(chapter) +\
                    '\n\nThanks in advance for cooperation!!' +\
                    '\n\nKind Regards,' +\
                    '\nFernando'
                self.emailer.send_adm_msg('Unknown Chapter: {}'.format(chapter), message)

    def _assign_lab_channel(self):
        query = 'project = HELP AND issuetype in (extRequest, Monitor) AND component = FIWARE-LAB-HELP ' \
                'AND status != Closed and assignee = EMPTY and updated >= -1d'
        requests = sorted(self.jira.search_issues(query, maxResults=25), key=lambda item: item.key)
        # HD chapter = issue.fields.customfield_11103
        # HD node    = issue.fields.customfield_11104
        # HD enabler = issue.fields.customfield_11105

        # make issues visible
        condition = lambda x: not x.fields.customfield_11103 and not \
            x.fields.customfield_11104 and not \
            x.fields.customfield_11105

        for issue in filter(condition, requests):
            enabler_values = self.jira.editmeta(issue)['fields']['customfield_11105']['allowedValues']
            enabler = next(filter(lambda x: x['value'] == 'Unknown', enabler_values))

            node_values = self.jira.editmeta(issue)['fields']['customfield_11104']['allowedValues']
            node = next(filter(lambda x: x['value'] == 'Unknown', node_values))

            issue.update(fields={'customfield_11105': enabler, 'customfield_11104': node})
            logging.info('update issue= {} node={} enabler={}'.format(issue, node['value'], enabler['value']))

        # assign issues whose node has been set up
        # HD node    = issue.fields.customfield_11104
        condition = lambda x: x.fields.customfield_11104 and x.fields.customfield_11104.value != 'Unknown'

        for issue in filter(condition, requests):
            node = issue.fields.customfield_11104.value
            if node in self.nodesBook:
                assignee = self.nodesBook[node]['support']
                self.jira.assign_issue(issue, assignee=assignee)
                logging.info('assign issue= {} node={} assignee={}'.format(issue, node, assignee))
            else:
                message = 'Dear Help Desk Caretaker Admin,' +\
                    "\n\nPlease, have a look at {} Node because it wasn't found in the Enablers book.".format(node) +\
                    '\n\nThanks in advance for cooperation!!' +\
                    '\n\nKind Regards,' +\
                    '\nFernando'
                self.emailer.send_adm_msg('Unknown Node: {}'.format(node), message)

    def channel_requests(self):
        query = 'project = HELP AND issuetype = extRequest AND component = EMPTY'
        requests = sorted(self.jira.search_issues(query, maxResults=25), key=lambda item: item.key)
        for request in requests:
            summary = request.fields.summary

            if re.search(r'\[SPAM\]', summary):
                request.update(fields={'components': [{'name': 'SPAM'}]})
                continue

            match = re.search(r'\[[^\]]+?\]', summary)

            if match:
                channel = match.group(0)[1:-1]
                if channel not in channels:
                    continue

                request.update(fields={'components': [{'name': channels[channel]}]})
                self.n_channeled += 1

                if not request.fields.assignee:
                    assignee = None if channel in ('Fiware-tech-help', 'Fiware-lab-help', 'SPAM') else '-1'
                    self.jira.assign_issue(request, assignee)
                    self.n_assignments += 1
                logging.info('updated request {}, channel= {}'.format(request, channel))

    def assign_requests(self):
        self._change_channel()
        self._assign_tech_channel()
        self._assign_lab_channel()

    def naming(self):
        query = 'project = HELP AND issuetype in (extRequest, Monitor) ' \
                 'AND status = Closed and updated >= -1d AND component != EMPTY'
        issues = sorted(self.jira.search_issues(query, maxResults=25), key=lambda item: item.key)
        # name spam
        logging.info('====== SPAM =======')
        condition = lambda x: x.fields.components[0].name == 'SPAM'
        for issue in filter(condition, issues):
            if not re.match(r'SPAM\s=>', issue.fields.summary):
                summary = 'SPAM => ' + re.sub(r'\[[^\]]+?\]', '', issue.fields.summary.strip())
                issue.update(fields={'summary': summary, 'customfield_11103': None,
                                     'customfield_11104': None, 'customfield_11105': None})
                logging.info('update issue:{} {}'.format(issue, summary))

        # name othen channels than TECH and LAB
        _channels = '|'.join(ifilterfalse(lambda x: x in ('Tech', 'Lab'), keywords.values()))

        logging.info('====== other channels than Tech and Lab =======')
        condition = lambda x: x.fields.components[0].name in noTechChannels
        for issue in filter(condition, issues):
            try:
                issuetype = issuetypedict[issue.fields.issuetype.name]
            except Exception as e:
                logging.warning(e)
                issuetype = 'Unknown'

            chkeyword = keywords[issue.fields.components[0].name]
            pattern = r'FIWARE\.{}\.{}\.'.format(issuetype, chkeyword)

            # formato correcto
            if re.match(pattern, issue.fields.summary):
                continue

            # en canal equivocado
            gpattern = r'FIWARE\.{}\.({})\.'.format(issuetype, _channels)

            if re.match(gpattern, issue.fields.summary.strip()):
                summary = re.sub(r'\.({})\.'.format(_channels), chkeyword, issue.fields.summary).strip()
            else:
                summary = re.sub(r'\[[^\]]+?\]', '', issue.fields.summary.strip())
                summary = re.sub(r'\.FIWARE\.(Request|Question)\.\w+\.', '', summary)
                summary = 'FIWARE.{}.{}.{}'.format(issuetype, chkeyword, summary)
            issue.update(fields={'summary': summary, 'customfield_11103': None,
                                 'customfield_11104': None, 'customfield_11105': None})
            logging.info('update issue:{} {}'.format(issue, summary))
            self.n_renamed += 1
        # name Lab channel
        # HD chapter = issue.fields.customfield_11103
        # HD node    = issue.fields.customfield_11104
        # HD enabler = issue.fields.customfield_11105

        logging.info('===== Lab channel ========')
        condition = lambda x: x.fields.components[0].name == 'FIWARE-LAB-HELP'
        # HD node    = issue.fields.customfield_11104
        for issue in filter(condition, issues):
            try:
                issuetype = issuetypedict[issue.fields.issuetype.name]
            except Exception as e:
                logging.warning(e)
                issuetype = 'Unknown'

            chunks = issue.fields.summary.strip().split('.')
            node = issue.fields.customfield_11104
            nodeValue = node.value if node else 'Unknown'
            _channels = '|'.join(keywords.values())

            if nodeValue != 'Unknown':
                pattern = r'FIWARE\.{}\.Lab\.{}\.'.format(issuetype, nodeValue)

                if re.match(pattern, issue.fields.summary):
                    continue

                pattern = r'FIWARE\.{}\.({})\.{}\.'.format(issuetype, _channels, nodeValue)

                if re.match(pattern, issue.fields.summary):
                    summary = '.'.join(chunks[0:2]) + '.Lab.' + '.'.join(chunks[3:])
                else:
                    summary = re.sub(r'\[[^\]]+?\]', '', issue.fields.summary).strip()
                    summary = re.sub(r'FIWARE\.(Request|Question)\.\w+\.', '', summary)
                    summary = 'FIWARE.{}.Lab.{}.{}'.format(issuetype, nodeValue, summary)
                issue.update(fields={'summary': summary, 'customfield_11103': None, 'customfield_11105': None})
            else:
                pattern = r'FIWARE\.{}\.Lab\.'.format(issuetype)

                if re.match(pattern, issue.fields.summary):
                    continue

                pattern = r'FIWARE\.{}\.({})\.'.format(issuetype, _channels)

                if re.match(pattern, issue.fields.summary):
                    summary = '.'.join(chunks[0:2]) + '.Lab.' + '.'.join(chunks[3:])
                else:
                    summary = re.sub(r'\[[^\]]+?\]', '', issue.fields.summary).strip()
                    summary = re.sub(r'FIWARE\.(Request|Question)\.\w+\.', '', summary)
                    summary = 'FIWARE.{}.Lab.{}.'.format(issuetype, summary)
                issue.update(fields={'summary': summary, 'customfield_11103': None,
                                     'customfield_11104': None, 'customfield_11105': None})
            logging.info('update issue: {} {}'.format(issue, summary))
            self.n_renamed += 1

        # name Tech channel
        # HD chapter = issue.fields.customfield_11103
        # HD node    = issue.fields.customfield_11104
        # HD enabler = issue.fields.customfield_11105

        logging.info('===== Tech channel =======')
        condition = lambda x: x.fields.components[0].name == 'FIWARE-TECH-HELP'
        for issue in filter(condition, issues):
            chapter_values = self.jira.editmeta(issue)['fields']['customfield_11103']['allowedValues']

            try:
                issuetype = issuetypedict[issue.fields.issuetype.name]
            except Exception as e:
                logging.warning(e)
                issuetype = 'Unknown'

            chunks = issue.fields.summary.strip().split('.')
            chapter = issue.fields.customfield_11103
            enabler = issue.fields.customfield_11105
            chapter_value = chapter.value if chapter else 'Unknown'
            enabler_value = enabler.value if enabler else 'Unknown'

            if enabler_value != 'Unknown':
                try:
                    enablerkeyword = self.enablersBook[enabler_value]['backlog_keyword']
                    chapterkeyword = self.enablersBook[enabler_value]['chapter']
                except KeyError:
                    logging.exception('Unknown enabler {}'.format(enabler_value))
                    continue
                chapter = next(filter(lambda x: x['value'] == chapterkeyword, chapter_values))

                pattern = r'FIWARE\.{}\.Tech\.{}\.{}\.'.format(issuetype, chapterkeyword, enablerkeyword)

                if re.match(pattern, issue.fields.summary):
                    continue

                pattern = r'FIWARE\.{}\.({})\.{}\.{}\.'.format(issuetype, _channels, chapterkeyword, enablerkeyword)

                if re.match(pattern, issue.fields.summary):
                    summary = '.'.join(chunks[0:2]) + '.Tech.' + '.'.join(chunks[3:])
                else:
                    summary = re.sub(r'\[[^\]]+?\]', '', issue.fields.summary).strip()
                    summary = re.sub(r'FIWARE\.(Request|Question)\.\w+\.', '', summary)
                    summary = 'FIWARE.{}.Tech.{}.{}.{}'.format(issuetype, chapterkeyword, enablerkeyword, summary)

                issue.update(fields={'summary': summary, 'customfield_11103': chapter, 'customfield_11104': None})

            elif enabler_value == 'Unknown' and chapter_value != 'Unknown':
                pattern = r'FIWARE\.{}\.Tech\.{}\.'.format(issuetype, chapter_value)

                if re.match(pattern, issue.fields.summary):
                    continue

                pattern = r'FIWARE\.{}\.({})\.{}\.'.format(issuetype, _channels, chapter_value)

                if re.match(pattern, issue.fields.summary):
                    summary = '.'.join(chunks[0:2]) + '.Tech.' + '.'.join(chunks[3:])
                else:
                    summary = re.sub(r'\[[^\]]+?\]', '', issue.fields.summary).strip()
                    summary = re.sub(r'FIWARE\.(Request|Question)\.\w+\.', '', summary)
                    summary = 'FIWARE.{}.Tech.{}.{}'.format(issuetype, chapter_value, summary)

                issue.update(fields={'summary': summary, 'customfield_11104': None, 'customfield_11105': None})

            else:
                pattern = r'FIWARE\.{}\.Tech\.'.format(issuetype)

                if re.match(pattern, issue.fields.summary):
                    continue

                pattern = r'FIWARE\.{}\.({})\.'.format(issuetype, _channels)

                if re.match(pattern, issue.fields.summary):
                    summary = '.'.join(chunks[0:2]) + '.Tech.' + '.'.join(chunks[3:])
                else:
                    summary = re.sub(r'\[[^\]]+?\]', '', issue.fields.summary).strip()
                    summary = re.sub(r'FIWARE\.(Request|Question)\.\w+\.', '', summary)
                    summary = 'FIWARE.{}.Tech.{}.'.format(issuetype, summary)

                issue.update(fields={'summary': summary, 'customfield_11103': None,
                                     'customfield_11104': None, 'customfield_11105': None})

            logging.info('update issue: {} {}'.format(issue, summary))
            self.n_renamed += 1

    def remove_spam(self):
        query = 'project in (HELP, HELC) and component = SPAM and updated <= -7d'
        # query = 'project in (HELP, HELC) and component = SPAM'
        requests = sorted(self.jira.search_issues(query, maxResults=25), key=lambda item: item.key)
        for request in requests:
            request.delete()
            logging.info('DELETED SPAM {}'.format(request))
            self.n_removed += 1
