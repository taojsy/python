"""
@Author  : Li Hui
@Contact : hui.4.li@nokia-sbell
"""
import os
import pandas as pd
from logger import logger
from baseJira import BaseJira


class JiraCompetenceArea(BaseJira):
    def __init__(self, jira_tool_file):
        super(JiraCompetenceArea, self).__init__()
        self.file = jira_tool_file
        self.issue_id_for_customField_mapping = self.get_fields_value_id_mapping_template()

    def get_fields_value_id_mapping_template(self):
        logger.info('Try to get fields_value_id_mapping_template from:%s', self.file)
        while not os.path.exists(self.file):
            logger.error("can not find file".format(self.file))
        df = pd.read_excel(self.file, sheet_name='fields_value_id_mapping')
        return df.loc[0]['competence_area_issue_id']

    def createCA(self, client, data, user):
        logger.info("Competence Area does not exist, will create a new one: " + data["summary"])
        content = {
            'summary': data.get('summary'),
            'customfield_38690': self.fields_value_id_mapping(client, data.get('competence_area'), 'customfield_38690'),# competence_area value should be ID, eg.CloudRAN CI=214831
            'customfield_38702': data.get('item_id'),
            'customfield_29791': data.get('EI_links'),
            'assignee': data.get('assignee'),
            'description': data.get('description'),
            'customfield_11890': data.get('story_point'),
            'timetracking': data.get('estimation'),
            'reporter': user,
        }
        issuekey = self.createIssue(content, data, client)
        # Field "labels", "fusion_component" and "activity_type" use JIRA update to create, otherwise cannot be created successfully
        issue = client.issue(issuekey)
        issue.update(fields={'labels': self.handle_labels(data),
                             'customfield_38750': {'value': data.get('activity_type')},
                             'customfield_38691': [{'value': data.get('fusion_component')}]
                             })

        logger.info('Competence Area create successfully!')
        return issuekey

    def updateCA(self, client, issue_key, data):
        logger.info("Competence Area exists, just update it: " + data["summary"])
        update_data = {
            # 'summary': data.get('summary'),
            'customfield_38702': data.get('item_id'),
            'customfield_38750': {'value': data.get('activity_type')},
            'assignee': {'name': data.get('assignee')},
            'labels': self.handle_labels(data),
            'description': data.get('description'),
            'customfield_11890': eval(data.get('story_point')) if data.get('story_point') else None,
            'timetracking': self.get_need_update_field_estimation(client, issue_key, data),
            'customfield_38691': [{'value': data.get('fusion_component')}]
        }
        issue = client.issue(issue_key)
        issue.update(fields=update_data)
        logger.info('Competence Area update successfully!!!')
        return issue

    def fields_value_id_mapping(self, client, value, customfield):
        value_id = ''
        issue = client.issue(self.issue_id_for_customField_mapping)
        meta = client.editmeta(issue)
        allowedValues = meta['fields'][customfield]['allowedValues']
        for options in allowedValues:
            if options['value'] == value:
                value_id = options['id']
                break
        if value_id:
            return value_id
        else:
            raise ValueError('Your {value} for {field} is Not an allowed value!'.format(value=value, field=customfield))
