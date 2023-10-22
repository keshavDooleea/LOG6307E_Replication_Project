from steps.repository_collection.repositories_via_api import RepositoryCollectionViaAPI
from steps.repository_collection.repositories_via_json import RepositoryCollectionViaJSON

if __name__ == "__main__":

    # repo_collection = RepositoryCollectionViaAPI()
    repo_collection = RepositoryCollectionViaJSON()
    repo_collection.create_dataset()
