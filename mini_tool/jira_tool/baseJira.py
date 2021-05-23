"""
@Author  : Li Hui
@Contact : hui.4.li@nokia-sbell
"""
import re
from jira.utils import json_loads
from work_path import WorkPath


class BaseJira:
    def __init__(self):
        self.work_dir = WorkPath().directory()

    def get_need_update_field_estimation(self, client, issue_key, data):
        timetracking = client.issue(issue_key.key).fields.timetracking
        if hasattr(timetracking, 'timeSpentSeconds'):
            logged_time = timetracking.timeSpentSeconds
        else:
            logged_time = ''
        return {'remainingEstimate': data['estimation']} if logged_time else {
            'originalEstimate': data['estimation']}

    def createIssue(self, content, data, client):
        """
        JIRA create issue API  is not working, use the below code to replace
        """
        url = 'https://jiradc.ext.net.nokia.com/secure/QuickCreateIssue.jspa?decorator=none'
        pid = client.project(data.get('project')).id
        issuetype_id = client.issue_type_by_name(data.get('issuetype')).id
        token = client._session.cookies.values()[1]
        content['pid'] = pid
        content['issuetype'] = issuetype_id
        content['atl_token'] = token

        headers = {'Origin': 'https://jiradc.ext.net.nokia.com', 'X-AUSERNAME': 'jinbyu', 'Connection': 'keep-alive',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Referer': 'https://jiradc.ext.net.nokia.com/secure/RapidBoard.jspa?rapidView=13285',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Accept': '*/*',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}
        url_labels = self.combine_url_labels(url, data)
        response = client._session.post(url_labels, data=content, headers=headers)
        return json_loads(response)['issueKey']

    def searchIssues(self, jql, client, field="", max_results=100):
        ''' Search issues
        @param jql: JQL, str
        @param max_results: max results, int, default 100
        @return issues: result, list
        '''
        try:
            issues = client.search_issues(jql, fields=field, maxResults=max_results)
            return issues
        except Exception as e:
            print(e)

    @staticmethod
    def handle_labels(data):
        if "labels" in data.keys():
            labels = re.sub(r'\s*', '', data['labels']).split(',')
        else:
            labels = None
        return labels

    def combine_url_labels(self, url, data):
        """
        Handle mutiple labels for one issue
        Expected "&labels=Aic5G_regression&labels=CICD&labels=ci_issues"
        """
        labels_str = ''
        for label in self.handle_labels(data):
            labels_str += '&labels=' + label
        url_labels = url + labels_str
        return url_labels

    def workaround_exact_search_match(self, jql, client, data):
        """
        JIRA API not support exact match for field summary when search issue, workaround as below
        Also not support Special characters search (https://confluence.atlassian.com/jirasoftwareserver085/search-syntax-for-text-fields-981156853.html)
        """
        jql = jql + ' AND status not in (Obsolete, Closed)'

        exist_list = self.searchIssues(jql, client, field="key,summary")
        new_list = []
        for issue_key in exist_list:
            exist_summary = issue_key.fields.summary
            if data["summary"] == exist_summary:
                new_list.append(issue_key)
        return new_list

    def handle_summary_with_reserved_characters(self, summary):
        """
        Will handle '+ - & | ! ( ) { } [ ] ^ ~ * ? \'
        https://confluence.atlassian.com/jirasoftwareserver085/search-syntax-for-text-fields-981156853.html
        """
        reserved_characters = ['+', '-', '&', '|', '!', '(', ')', '{', '}', '[', ']', '^', '~', '*', '?', '\\']
        for reserved in reserved_characters:
            summary = summary.replace(reserved, '@@')
        str_list = summary.split('@@')
        max_len_str = max(str_list, key=len, default='')
        return max_len_str
