from steps.repository_collection.main import execute_repositories_collection
from helpers.git import GitHelper

if __name__ == "__main__":

    org = "Mirantis"
    repos = execute_repositories_collection(org)

    for repo in repos:
        print(GitHelper.get_repo_details(repo))

