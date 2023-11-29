import re

from loguru import logger
from decouple import config
import gitlab


class GitlabConnector:
    def __init__(self, personal_api_token: str, project_id: str):
        """
        Create Gitlab instance with token and project
        :param personal_api_token:
        :param project_id:
        """
        assert personal_api_token
        assert project_id
        self.project_id = project_id
        self.__gitlab = gitlab.Gitlab(private_token=personal_api_token)

    @staticmethod
    def factory() -> "GitlabConnector":
        personal_api_token = config('PAT')
        project_id = config('PROJECT_ID', default=False)
        if not project_id:
            # if project is not defined, assume current project
            project_id = config('CI_PROJECT_ID')
        return GitlabConnector(personal_api_token, project_id)

    @property
    def project(self):
        return self.__gitlab.projects.get(self.project_id)

    def get_changelog(self, environment: str = "staging/the_exb") -> None:
        kwargs = {
            'order_by': "finished_at", 'sort': "desc", 'iterator': True,
            "environment": environment, "status": "success"
        }
        deployments_iter = self.project.deployments.list(**kwargs)
        deployment = next(deployments_iter)

        mr_iter = deployment.mergerequests.list(iterator=True)
        issues_merged = []
        for mr in mr_iter:
            if "Closes" not in mr.description:
                logger.info(f"somebody ({mr.author['name']}) did something without issue: {mr.title}")
                continue
            issue_ids = re.findall(r'#(\d+)', mr.description)
            if not issue_ids:
                continue
            for id in issue_ids:
                try:
                    issues_merged.append(self.project.issues.get(id))
                except gitlab.exceptions.GitlabGetError as error:
                    if error.response_code != 404:
                        raise

        for issue in issues_merged:
            logger.info(f"{issue.title}, see {issue.web_url}")
