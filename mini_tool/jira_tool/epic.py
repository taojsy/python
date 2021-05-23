"""
@Author  : Li Hui
@Contact : hui.4.li@nokia-sbell
"""
from logger import logger
from baseJira import BaseJira


class JiraEpic(BaseJira):
    def createEpic(self, client, data, user):
        logger.info("Epic does not exist, will create a new one: " + data["summary"])
        content = {
            'summary': data.get('summary'),
            'customfield_12791': data.get('epic_name'),
            'customfield_29791': data.get('CA_links'),
            'customfield_38694': data.get('start_fb'),
            'customfield_38693': data.get('end_fb'),
            'customfield_29790': data.get('team'),
            'customfield_11890': data.get('story_point'),
            'timetracking': data.get('estimation'),
            'assignee': data.get('assignee'),
            'description': data.get('description'),
            'reporter': user,
        }
        issuekey = self.createIssue(content, data, client)
        logger.info('Epic create successfully!')
        return issuekey

    def updateEpic(self, client, issue_key, data):
        logger.info("Epic exists, just update it: " + data["summary"])
        update_data = {
            # 'summary': data['summary'],
            'customfield_12791': data['epic_name'],
            'customfield_38694': data['start_fb'],
            'customfield_38693': data['end_fb'],
            'customfield_11890': eval(data['story_point']) if data['story_point'] else None,
            'timetracking': self.get_need_update_field_estimation(client, issue_key, data),
            'assignee': {'name': data['assignee']},
            'labels': self.handle_labels(data),
            'description': data['description']
        }
        issue = client.issue(issue_key)
        issue.update(fields=update_data)
        logger.info('Epic update successfully!!!')
        return issue
