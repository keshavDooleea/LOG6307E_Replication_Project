
# 3.1.1. Repository Collection

from steps.repository_collection.criterias_application import CriteriasApplication
from helpers.request import RequestHelper

# main entry point for repository collection
def execute_repositories_collection(org: str):
    print(f"Running 3.1.1. Repository collection for {org}")

    selected_repos = []
    get_repositories_per_page(org, 1, 100, selected_repos)
    
    print(f"Finished 3.1.1. Repository collection for {org}")

    return selected_repos



def get_repositories_per_page(org, page_nb, per_page, selected_repos):
    url= f"https://api.github.com/orgs/{org}/repos?page={page_nb}&per_page={per_page}"
    repos = RequestHelper.get_api_response(url)

    criterias_app = CriteriasApplication(repos)
    selected_repos += criterias_app.apply_criterias()

    # handle pagination: if lenght of response is 100, means there can be more on the next page
    if len(repos) == per_page:
        get_repositories_per_page(org, page_nb + 1, per_page, selected_repos)




