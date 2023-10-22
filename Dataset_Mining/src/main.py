from steps.repository_collection.repositories_via_api import RepositoryCollectionViaAPI
from steps.repository_collection.repositories_via_json import RepositoryCollectionViaJSON
from helpers.request import RequestHelper

if __name__ == "__main__":

    rate_limit = RequestHelper.get_rate_limit()
    print(rate_limit)

    # repo_collection = RepositoryCollectionViaAPI()
    repo_collection = RepositoryCollectionViaJSON()
    repo_collection.create_dataset()
