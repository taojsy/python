"""
@Author  : Li Hui
@Contact : hui.4.li@nokia-sbell
"""
from logger import logger
from baseJira import BaseJira


class JiraStory(BaseJira):
    def create(self, data, client, user, issuetype):
        logger.info("%s does not exist, will create a new one: %s" % (issuetype.capitalize(), data["summary"]))
        content = {
            'summary': data.get('summary'),
            'customfield_12790': data.get('Epic_links'),
            'assignee': data.get('assignee'),
            'description': data.get('description'),
            'timetracking': data.get('estimation'),
            'customfield_29790': data.get('team'),
            'reporter': user}

        issuekey = self.createIssue(content, data, client)
        logger.info('%s create successfully!', issuetype.capitalize())
        return issuekey

    def update(self, data, client, issue_key, issuetype):
        logger.info("%s exists, just update it: %s" % (issuetype.capitalize(), data["summary"]))

        labels = self.handle_labels(data)
        update_data = {
            # 'summary': data['summary'],
            # 'customfield_12790': data['Epic_links'],
            'timetracking': self.get_need_update_field_estimation(client, issue_key, data),
            'assignee': {'name': data['assignee']},
            'labels': labels,
            'customfield_11890': eval(data['story_point']) if data['story_point'] else None,
            'description': data['description']
        }
        issue = client.issue(issue_key)
        issue.update(update_data)
        logger.info('%s update successfully!', issuetype.capitalize())
        return issue
