# -*- coding: utf-8 -*-
from jira import JIRA
import os, datetime
import pandas as pd
from logger import logger
from story import JiraStory
from epic import JiraEpic
from competence_area import JiraCompetenceArea
from baseJira import BaseJira


class JiraUtils(BaseJira):
    def __init__(self):
        super(JiraUtils, self).__init__()
        self.jira_tool_file = os.path.join(self.work_dir, 'jira_tool.xlsm')
        self.user, self.pwd, self.issuetype = self.get_basic_info()
        self.client = self._create_jira_client()
        self.jiraStory = JiraStory()
        self.jiraEpic = JiraEpic()
        self.jiraCA = JiraCompetenceArea(self.jira_tool_file)
        self.new_data = []
        self.default_value = ""

    def get_basic_info(self):
        logger.info('Current working directory path is %s', self.work_dir)
        logger.info('Try to get basic information from:%s', self.jira_tool_file)
        while not os.path.exists(self.jira_tool_file):
            logger.error("can not find file".format(self.jira_tool_file))
        df = pd.read_excel(self.jira_tool_file, sheet_name='start_create_update')
        basic_info = df.loc[0]
        issuetype = basic_info['issuetype'].strip().lower()
        logger.info('Issue type is:%s', issuetype)
        return basic_info['username'], basic_info['password'], issuetype

    def _create_jira_client(self):
        logger.info('Start to connect to JIRA Server!')
        client = JIRA(server="https://jiradc.int.net.nokia.com", basic_auth=(self.user, self.pwd))
        client._session.post(url='https://jiradc.ext.net.nokia.com/login.jsp',
                             data={'os_username': self.user, 'os_password': self.pwd})
        logger.info('Connect to JIRA Server successfully!')
        return client

    def handle_epic(self):
        logger.info('***********Start to handle epic***************')
        df = pd.read_excel(self.jira_tool_file,
                           names=['project', 'summary', 'epic_name', 'issuetype', 'CA_links', 'assignee', 'labels',
                                  'description', 'start_fb', 'end_fb', 'story_point', 'estimation', 'team'],
                           sheet_name='jira_epic',
                           converters={'estimation': str, 'story_point': str, 'team': str, 'start_fb':str, 'end_fb':str})
        df = df.fillna(self.default_value, inplace=False)
        for i in df.index:
            data = df.loc[i].copy(deep=True)
            summary = self.handle_summary_with_reserved_characters(data["summary"])
            jql = "project = " + data['project'] + " AND summary ~ " + '\"' + summary +\
                  '\"' + " AND  'Parent Link' = " + '\"' + data['CA_links'] + '\"' + ""
            exist_list = self.workaround_exact_search_match(jql, self.client, data)

            if len(exist_list) == 0:
                data["key"] = self.jiraEpic.createEpic(self.client, data, self.user)
            elif len(exist_list) == 1:
                data["key"] = self.jiraEpic.updateEpic(self.client, exist_list[0], data)
            else:
                logger.error("More than one issue found:" + data["summary"])
                raise Exception
            self.new_data.append(data)

    def handle_story_task(self, issuetype):
        logger.info('***********Start to handle story/task***************')
        df = pd.read_excel(self.jira_tool_file,
                           names=['project', 'summary', 'issuetype', 'Epic_links', 'assignee', 'labels', 'description',
                                  'story_point', 'estimation', 'team'], sheet_name='jira_'+issuetype,
                           converters={'estimation': str, 'team': str})

        df = df.fillna(self.default_value, inplace=False)
        for i in df.index:
            data = df.loc[i].copy(deep=True)
            summary = self.handle_summary_with_reserved_characters(data["summary"])
            jql = "project = " + data["project"] + " AND summary ~ " + '\"' + summary +\
                  '\"' + " AND 'Epic Link' = " + '\"' + data["Epic_links"] + '\"' + ""
            exist_list = self.workaround_exact_search_match(jql, self.client, data)

            if len(exist_list) == 0:
                data["key"] = self.jiraStory.create(data, self.client, self.user, issuetype)
            elif len(exist_list) == 1:
                data["key"] = self.jiraStory.update(data, self.client, exist_list[0], issuetype)
            else:
                logger.error("More than one issue found:" + data["summary"])
                raise Exception
            self.new_data.append(data)

    def handle_competence_area(self):
        logger.info('***********Start to handle competence area***************')
        df = pd.read_excel(self.jira_tool_file,
                           names=['project', 'summary', 'competence_area', 'item_id', 'activity_type', 'issuetype', 'EI_links', 'fusion_component', 'assignee', 'labels', 'description',
                                  'story_point', 'estimation'], sheet_name='jira_competence_area',
                           converters={'estimation': str, 'activity_type': str, 'competence_area': str})

        df = df.fillna(self.default_value, inplace=False)
        for i in df.index:
            data = df.loc[i].copy(deep=True)
            summary = self.handle_summary_with_reserved_characters(data["summary"])
            jql = "project = " + data['project'] + " AND summary ~ " + '\"' + summary +\
                  '\"' + " AND  'Parent Link' = " + '\"' + data['EI_links'] + '\"' + ""
            exist_list = self.workaround_exact_search_match(jql, self.client, data)

            if len(exist_list) == 0:
                data["key"] = self.jiraCA.createCA(self.client, data, self.user)
            elif len(exist_list) == 1:
                data["key"] = self.jiraCA.updateCA(self.client, exist_list[0], data)
            else:
                logger.error("More than one found:" + data["summary"])
                raise Exception
            self.new_data.append(data)

    def close_jira(self):
        self.client.close()

    def write_to_file(self, ):
        file = 'jira_' + datetime.datetime.now().strftime('%Y%m%d%H%M') + '.xlsx'
        new_file = os.path.join(self.work_dir, file)
        df = pd.DataFrame(self.new_data)
        df.to_excel(new_file, index=False)
        logger.info("All done! Please check the file:<{}>".format(new_file))
