
# 3.1.1. Repository Collection

from steps.repository_collection.criterias_application import CriteriasApplication
from helpers.request import RequestHelper

# main entry point for repository collection
def execute_repositories_collection():
    print("3.1.1. Repository collection")

    org = "Mirantis"
    url= f"https://api.github.com/orgs/{org}/repos?page=1&per_page=100"

    repos = RequestHelper.get_api_response(url)
    
    criterias_app = CriteriasApplication(repos)
    criterias_app.apply_criterias()
