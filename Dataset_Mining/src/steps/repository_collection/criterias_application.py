from helpers.request import RequestHelper
from helpers.git import GitHelper
from datetime import datetime

class CriteriasApplication:

    def __init__(self, repos: list):
        self.repos = repos

    # entry point to filter out repos based on 3 criterias applications
    def apply_criterias(self):
        if not self.repos:
            print("Exiting criterias application")
            return

        selected_repos = []

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
            has_enough_monthly_commits = self.__apply_criteria_3(repo)
            if has_enough_monthly_commits:
                selected_repos.append(repo)

        return selected_repos


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
        owner_name, repo_name = GitHelper.get_repo_details(repo)
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
        monthly_commits = {}
        return self.get_commits_per_page(repo, 1, 100, monthly_commits)


    # recursive method to calculate commits via pagination for repo
    def get_commits_per_page(self, repo, page_nb, per_page, monthly_commits):
        monthly_commits_threshold = 2

        owner_name, repo_name = GitHelper.get_repo_details(repo)
        commits_url = f"https://api.github.com/repos/{owner_name}/{repo_name}/commits?per_page={per_page}&page={page_nb}"
        commits_response = RequestHelper.get_api_response(commits_url)

        # set monthly commits counter
        for commit in commits_response:
            commit_date = datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
            month_year = commit_date.strftime('%Y-%m')

            if month_year in monthly_commits:
                monthly_commits[month_year] += 1
            else:
                monthly_commits[month_year] = 1

        # compare monthly commits nb
        for month_year, commit_count in monthly_commits.items():
            if commit_count < monthly_commits_threshold:
                return False
        
        # handle pagination: if lenght of response is 100, means there can be more on the next page
        if len(commits_response) == per_page:
            return self.get_commits_per_page(repo, page_nb + 1, per_page, monthly_commits)
        
        return True