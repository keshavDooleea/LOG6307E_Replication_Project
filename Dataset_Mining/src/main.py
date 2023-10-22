from steps.repository_collection.repositories_via_api import RepositoryCollectionViaAPI
from steps.repository_collection.repositories_via_json import RepositoryCollectionViaJSON
from steps.commit_msg_processing.main import CommitMsgProcessing
from helpers.request import RequestHelper
from helpers.json import JsonHelper

def apply_repo_collection():
    # repo_collection = RepositoryCollectionViaAPI()
    repo_collection = RepositoryCollectionViaJSON()
    repo_collection.create_dataset()
    dataset = repo_collection.dataset
    
    return


def apply_commit_msg_processing():
    dataset = {
        "Mirantis": JsonHelper.read("output/selected_repos/Mirantis.json"),
        "Wikimedia": JsonHelper.read("output/selected_repos/Wikimedia.json"),
        "Openstack": []
    }

    msg_processing = CommitMsgProcessing(dataset)
    msg_processing.process()

    return



if __name__ == "__main__":

    rate_limit = RequestHelper.get_rate_limit()
    print(rate_limit)

    # apply_repo_collection()
    apply_commit_msg_processing()


