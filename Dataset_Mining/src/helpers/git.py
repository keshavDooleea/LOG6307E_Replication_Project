class GitHelper:

    # get common info from repo
    @staticmethod
    def get_repo_details(repo):
        owner_name = repo["owner"]["login"]
        repo_name = repo["name"]

        return owner_name, repo_name
    
    @staticmethod
    def get_mirantis_name():
        return "Mirantis"
    
    @staticmethod
    def get_openstack_name():
        return "Openstack"
    
    @staticmethod
    def get_wikimedia_name():
        return "Wikimedia"
    
    @staticmethod
    def get_repos_name():
        return [
            GitHelper.get_mirantis_name(), 
            GitHelper.get_wikimedia_name(), 
            # GitHelper.get_openstack_name()
        ]
