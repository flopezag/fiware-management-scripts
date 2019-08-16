import logging
from jira.client import JIRA
from .ServerDataFinder import find_deliveryboard, find_all_trackers, find_nodesk_trackers
from DesksReminder.Basics.settings import JIRA_USER, JIRA_PASSWORD

__author__ = 'Manuel Escriche'


class Data:
    def __init__(self):
        options = {'server': 'https://jira.fiware.org', 'verify': False}
        self._jira = JIRA(options, basic_auth=(JIRA_USER, JIRA_PASSWORD))

    def getUrgentDeskOnDeadline(self):
        try:
            # trackers = find_all_trackers()
            trackers = 'HELP,FLUA'  # The rest of trackers will not be analysed since end of FI-Next project
        except Exception:
            logging.exception('Not able to find all trackers in web server')
            raise Exception

        query = "duedate = 0d  AND status != Closed AND project in ({}) AND assignee is not EMPTY".format(trackers)
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getUrgentDeskUpcoming(self):
        try:
            # trackers = find_all_trackers()
            trackers = 'HELP,FLUA'  # The rest of trackers will not be analysed since end of FI-Next project
        except Exception:
            logging.exception('Not able to find all trackers in web server')
            raise Exception

        query = "duedate <= 7d  AND status != Closed AND project in ({}) AND assignee is not EMPTY".format(trackers)
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getUrgentDeskImpeded(self):
        try:
            # trackers = find_all_trackers()
            trackers = 'HELP,FLUA' # The rest of trackers will not be analysed since end of FI-Next project
        except Exception:
            logging.exception('Not able to find no-desk trackers in web server')
            raise Exception

        query = "status = Impeded AND project in ({}) AND assignee is not EMPTY".format(trackers)
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getUrgentDeskOverdue(self):
        try:
            # trackers = find_all_trackers()
            trackers = 'HELP,FLUA' # The rest of trackers will not be analysed since end of FI-Next project
        except Exception:
            logging.info('Not able to find all trackers in web server')
            trackers = 'COR,APP,CLD,DATA,MIND,IOT,SEC,WEB,OPS,ACA,CAT,MRK,LAB,' \
                       'COAC,WC,WD,EXPL,PRES,SUS,HELP,HELC,SUPP,FLUA'

        query = "duedate < now()  AND status not in ( Impeded, Closed )  " \
                "AND project in ({}) AND assignee is not EMPTY".format(trackers)

        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getDeliveryBoardPending(self):
        try:
            book = find_deliveryboard()
        except Exception:
            logging.exception('Not able to reach Backlog Web Server')
            raise Exception

        return {item: self._jira.issue(book[item]) for item in book}

    def getTechHelpDeskOpen(self):
        query = 'project = HELP AND status = Open AND component = FIWARE-TECH-HELP AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getTechHelpDeskInProgress(self):
        query = "project = HELP AND status = 'In Progress' AND component = FIWARE-TECH-HELP AND assignee is not EMPTY"
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getTechHelpDeskImpeded(self):
        query = 'project = HELP AND status = Impeded AND component = FIWARE-TECH-HELP AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getTechHelpDeskAnswered(self):
        query = 'project = HELP AND status = Answered AND component = FIWARE-TECH-HELP AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getLabHelpDeskOpen(self):
        query = 'project = HELP AND status = Open AND component = FIWARE-LAB-HELP AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getLabHelpDeskInProgress(self):
        query = "project = HELP AND status = 'In Progress' AND component = FIWARE-LAB-HELP AND assignee is not EMPTY "
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getLabHelpDeskImpeded(self):
        query = 'project = HELP AND status = Impeded AND component = FIWARE-LAB-HELP AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getLabHelpDeskAnswered(self):
        query = 'project = HELP AND status = Answered AND component = FIWARE-LAB-HELP AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getOthersHelpDeskOpen(self):
        query = 'project = HELP AND status = Open AND component not in (FIWARE-LAB-HELP, FIWARE-TECH-HELP) ' \
                'AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getOthersHelpDeskInProgress(self):
        query = "project = HELP AND status = 'In Progress' AND component not in (FIWARE-LAB-HELP, FIWARE-TECH-HELP) " \
                "AND assignee is not EMPTY "
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getOthersHelpDeskImpeded(self):
        query = 'project = HELP AND status = Impeded AND component not in (FIWARE-LAB-HELP, FIWARE-TECH-HELP) ' \
                'AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getOthersHelpDeskAnswered(self):
        query = 'project = HELP AND status = Answered AND component not in (FIWARE-LAB-HELP, FIWARE-TECH-HELP) ' \
                'AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getCoachesHelpDeskOpen(self):
        query = 'project = HELC AND status = Open AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getCoachesHelpDeskInProgress(self):
        query = "project = HELC AND status = 'In Progress' AND assignee is not EMPTY"
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getCoachesHelpDeskImpeded(self):
        query = 'project = HELC AND status = Impeded AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getCoachesHelpDeskAnswered(self):
        query = 'project = HELC AND status = Answered AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getAccountsDeskOpen(self):
        query = 'project = FLUA AND issuetype = UpgradeAccount AND status = Open AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getAccountsDeskInProgress(self):
        query = "project = FLUA AND issuetype = UpgradeAccount AND status = 'In Progress' AND assignee is not EMPTY"
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getAccountsDeskAnalysing(self):
        query = 'project = FLUA AND issuetype = UpgradeAccount AND status = Analysing AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getAccountsDeskScheduled(self):
        query = 'project = FLUA AND issuetype = UpgradeAccount AND status = Scheduled AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getAccountsDeskAnswered(self):
        query = 'project = FLUA AND issuetype = UpgradeAccount AND status = Answered AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)

    def getAccountsDeskRejected(self):
        query = 'project = FLUA AND issuetype = UpgradeAccount AND status = Rejected AND assignee is not EMPTY'
        return sorted(self._jira.search_issues(query, maxResults=False), key=lambda item: item.key)


if __name__ == "__main__":
    pass
