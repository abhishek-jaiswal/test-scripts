import base64
import json
import os
import yaml
from github import Github
from github.GithubException import UnknownObjectException # 404 exception


class writer(object):
    def write_yaml(self, filename, data):
        with open(filename, "w") as fp:
            yaml.safe_dump({"data":data}, fp, default_flow_style=False)


    def write_json(self, filename, data):
        with open(filename, 'w') as fp:
            json.dump({"data":data}, fp, sort_keys=True, indent=4)

class GitSahayak(writer):
    def __init__(self):
        if "git_user" not in os.environ:
            raise Exception("401 Set git User and git git_passwd in environment variable")

        if "git_passwd" not in os.environ:
            raise Exception("401 Set git User and git git_passwd in environment variable")

        self.git_user = os.getenv('git_user', 'jkabhishek')
        self.git_passwd = os.getenv('git_passwd', None)

        # data store
        self.data_store = []

        # create a Github instance
        # using an access token
        # g = Github("access_token"
        # using username and password
        self.git_instance = Github(self.git_user, self.git_passwd)

    def repo_generator(self):
        repo_data_store = []
        for repo in self.git_instance.get_user().get_repos():
            print(repo.full_name)
            try:
                if repo.get_readme().content:
                    readme = base64.b64decode(repo.get_readme().content)
            except UnknownObjectException as error:
                readme = None
            except Exception as error:
                raise error
            repo_data_store.append({
                "repo_full_name": repo.full_name,
                "repo_description": repo.description,
                "repo_url": repo.html_url,
                "repo_readme":readme,
                "repo_languages": repo.get_languages(),

            })
            self.data_store = repo_data_store


if __name__ == "__main__":
    g = GitSahayak()
    g.repo_generator()
    g.write_yaml('repo_data.yaml', g.data_store)
    g.write_json('repo_data.json', g.data_store)
