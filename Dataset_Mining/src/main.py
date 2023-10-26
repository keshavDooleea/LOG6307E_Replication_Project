from steps.repository_collection.repositories_via_api import RepositoryCollectionViaAPI
from steps.repository_collection.repositories_via_json import (
    RepositoryCollectionViaJSON,
)
from steps.commit_msg_processing.main import CommitMsgProcessing
from helpers.request import RequestHelper
from helpers.git import GitHelper
from sys import exit

def apply_repo_collection(makeAPIRequest):
    if makeAPIRequest:
        repo_collection = RepositoryCollectionViaAPI() # use this when you want to fetch all repos online
    else:
        repo_collection = RepositoryCollectionViaJSON() # use this if all the repos were saved in a JSON file in output/all_repos
    
    repo_collection.create_dataset()
    return


def apply_commit_msg_processing():
    dataset = GitHelper.get_repos_name()
    msg_processing = CommitMsgProcessing(dataset)
    msg_processing.process()

    return


if __name__ == "__main__":
    rate_limit = RequestHelper.get_rate_limit()
    print(rate_limit)

    if rate_limit["remaining"] == 0:
        print("Not enough rate. Exiting.")
        exit(0)

    apply_repo_collection(False)
    apply_commit_msg_processing()


