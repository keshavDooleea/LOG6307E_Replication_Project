
# 3.1.1. Repository Collection

from steps.repository_collection.criterias_application import CriteriasApplication
from steps.repository_collection.criterias_count import CriteriaCount
from helpers.request import RequestHelper
from helpers.git import GitHelper
from helpers.util import Util

class RepositoryCollection:

    def __init__(self):
        print(f"Preparing dataset for 3.1.1. Repository collection")
        self.dataset = {}

    def create_dataset(self):
        for org in GitHelper.get_repos_name():
            Util.separate_line()
            print("Mining", org)

            criterias_count = CriteriaCount(org)
            self.get_repositories_per_page(org, 1, 100, criterias_count)
            self.dataset[org] = criterias_count
            Util.separate_line()
            criterias_count.print_count()
        
        print(f"Finished 3.1.1. Repository collection")


    def get_repositories_per_page(self, org, page_nb, per_page, criterias_count):
        curr_repos_len = criterias_count.get_repos_length()
        print(f"Fetching page {page_nb} for {org} - currently {curr_repos_len} repo{'s' if curr_repos_len > 1 else ''}")

        url= f"https://api.github.com/orgs/{org}/repos?page={page_nb}&per_page={per_page}"
        repos = RequestHelper.get_api_response(url)

        criterias_app = CriteriasApplication(repos, criterias_count)
        criterias_app.apply_criterias()

        # handle pagination: if lenght of response is 100, means there can be more on the next page
        if len(repos) == per_page:
            self.get_repositories_per_page(org, page_nb + 1, per_page, criterias_count)




