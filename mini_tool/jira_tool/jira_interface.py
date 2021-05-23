"""
@Author  : Li Hui
@Contact : hui.4.li@nokia-sbell
"""
import traceback
from jiraUtils import JiraUtils
from logger import logger


if __name__ == '__main__':
    jiraUtils = JiraUtils()
    try:
        if jiraUtils.issuetype == "epic":
            jiraUtils.handle_epic()
        elif jiraUtils.issuetype in ["story", "task"]:
            jiraUtils.handle_story_task(jiraUtils.issuetype)
        elif jiraUtils.issuetype == 'competence area':
            jiraUtils.handle_competence_area()
        jiraUtils.write_to_file()

    except Exception as e:
        logger.error("Create/Update failed！Please check the log file.")
        logger.error(traceback.format_exc())
    finally:
        jiraUtils.close_jira()
