
# 3.1.1. Repository Collection: read repos from JSON files

from helpers.git import GitHelper
from helpers.json import JsonHelper
from helpers.util import Util
from steps.repository_collection.criterias_count import CriteriaCount
from steps.repository_collection.criterias_application import CriteriasApplication

class RepositoryCollectionViaJSON:

    def __init__(self):
        print(f"Preparing dataset for 3.1.1. Repository collection. Reading from JSON.")
        self.dataset = {}

    def create_dataset(self):
        for org in GitHelper.get_repos_name():
            org_name = org["name"]
            repos = JsonHelper.read(f"output/all_repos/{org_name}.json")

            Util.separate_line()
            print("Mining", len(repos), "repos for", org_name)

            criterias_count = CriteriaCount(org_name)
            criterias_app = CriteriasApplication(org, repos, criterias_count)
            criterias_app.apply_criterias()

            self.dataset[org_name] = criterias_count

            Util.separate_line()
            criterias_count.print_count()
            criterias_count.save_count()
    
        Util.separate_line()
        print(f"Finished 3.1.1. Repository collection")