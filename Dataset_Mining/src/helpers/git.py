class GitHelper:

    # get common info from repo
    @staticmethod
    def get_repo_details(repo):
        owner_name = repo["owner"]["login"]
        repo_name = repo["name"]

        return owner_name, repo_name
