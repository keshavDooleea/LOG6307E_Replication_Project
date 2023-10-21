from helpers.request import RequestHelper

class CriteriasApplication:

    def __init__(self, repos: list):
        self.repos = repos

    # entry point for 3 criterias applications
    def apply_criterias(self):
        if not self.repos:
            print("Exiting criterias application")
            return

        for repo in self.repos: 
            # apply criteria 1
            is_repo_downloadable = self.__apply_criteria_1(repo)
            if not is_repo_downloadable:
                continue

            # apply criteria 2
            is_iac_files = self.__apply_criteria_2(repo)
            if not is_iac_files:
                continue

            # apply criteria 3
            self.__apply_criteria_3(repo)


    # checks if a file is an iac script
    def is_iac_file(self, file_name: str):
        return file_name.endswith('.pp')


    # The repository must be available for download
    def __apply_criteria_1(self, repo):
        return not repo["archived"]


    # At least 11% of the files belonging to the repository must be IaC scripts
    def __apply_criteria_2(self, repo):
        iac_threshold = 0.11
        iac_files = []
        
        # get all files in repository
        owner_name = repo["owner"]["login"]
        repo_name = repo["name"]
        branch = repo["default_branch"]
        repo_files_url = f"https://api.github.com/repos/{owner_name}/{repo_name}/git/trees/{branch}?recursive=1"

        files_response = RequestHelper.get_api_response(repo_files_url)
        if not files_response:
            return False
        
        files = files_response["tree"]
        if not files:
            return False

        # filter out iac files
        for file in files:
            if self.is_iac_file(file['path']):
                iac_files.append(file)

        # compare iac files with threshold
        return len(iac_files) / len(files) >= iac_threshold


    # The repository must have at least two commits per month
    def __apply_criteria_3(self, repo):
        monthly_commits_threshold = 2
        print(repo['name'])

