from steps.repository_collection.main import RepositoryCollection
from helpers.request import RequestHelper

if __name__ == "__main__":

    rate_limit = RequestHelper.get_rate_limit()
    print(rate_limit)

    repo_collection = RepositoryCollection()
    repo_collection.create_dataset()
