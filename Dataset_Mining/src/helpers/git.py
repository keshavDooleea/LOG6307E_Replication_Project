class GitHelper:
    
    # get common info from repo
    @staticmethod
    def get_repo_details(repo):
        owner_name = repo["owner"]["login"]
        repo_name = repo["name"]

        return owner_name, repo_name
    
     # checks if a file is an iac script
    @staticmethod
    def is_iac_file(file_name: str):
        return file_name.endswith('.pp')

    @staticmethod
    def get_mirantis_detail():
        return { "name": "Mirantis", "url": "api.github.com" }
    
    @staticmethod
    def get_openstack_detail():
        return { "name": "Openstack", "url": "opendev.org/api/v1" }
    
    @staticmethod
    def get_wikimedia_detail():
        return { "name": "Wikimedia", "url": "api.github.com" }
    
    @staticmethod
    def get_repos_name():
        return [
            # GitHelper.get_mirantis_detail(), 
            GitHelper.get_wikimedia_detail(), 
            # GitHelper.get_openstack_detail()
        ]
