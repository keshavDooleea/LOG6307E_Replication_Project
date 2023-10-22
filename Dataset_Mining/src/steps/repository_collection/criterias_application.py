from helpers.request import RequestHelper
from helpers.git import GitHelper
from helpers.json import JsonHelper
from datetime import datetime

class CriteriasApplication:

    def __init__(self, org, repos: list, criterias_count):
        self.org = org
        self.org_url = org["url"]
        self.repos = repos
        self.criterias_count = criterias_count

    # entry point to filter out repos based on 3 criterias applications
    def apply_criterias(self):
        if not self.repos:
            print("Exiting criterias application")
            return

        for idx, repo in enumerate(self.repos):

            print(f"{idx}: Applying criterias for", repo["name"], "repo") 

            # apply criteria 1
            is_repo_downloadable = self.__apply_criteria_1(repo)
            if not is_repo_downloadable:
                continue
            else:
                self.criterias_count.increase_count("c1")

            # apply criteria 2
            is_iac_files = self.__apply_criteria_2(repo)
            if not is_iac_files:
                continue
            else:
                self.criterias_count.increase_count("c2")

            # apply criteria 3
            has_enough_monthly_commits = self.__apply_criteria_3(repo)
            if has_enough_monthly_commits:
                self.criterias_count.increase_count("c3")
                self.criterias_count.add_repo(repo)

        JsonHelper.write(self.criterias_count.get_repos(), f'output/selected_repos/{self.criterias_count.org}.json')

        return self.criterias_count


    # The repository must be available for download
    def __apply_criteria_1(self, repo):
        return not repo["archived"]


    # At least 11% of the files belonging to the repository must be IaC scripts
    def __apply_criteria_2(self, repo):
        iac_threshold = 0.11
        
        if self.org["name"] == "Openstack":
            iac_files, files = self.__apply_criteria_2_for_openstack(repo)
        else:
            iac_files, files = self.__apply_criteria_2_for_git(repo)

        if files == 0:
            return False
        
        # compare iac files with threshold
        return (iac_files / files) >= iac_threshold
    

    def __apply_criteria_2_for_git(self, repo):
        iac_files = []
        
        # get all files in repository
        owner_name, repo_name = GitHelper.get_repo_details(repo)
        branch = repo["default_branch"]

        repo_files_url = f"https://{self.org_url}/repos/{owner_name}/{repo_name}/git/trees/{branch}?recursive=1"
        files_response = RequestHelper.get_api_response(repo_files_url)
        if not files_response:
            return False
        
        files = files_response["tree"]
        if not files:
            return False

        # filter out iac files
        for file in files:
            if GitHelper.is_iac_file(file['path']):
                iac_files.append(file)

        return len(iac_files), len(files)


    def __apply_criteria_2_for_openstack(self, repo):
        iac_files_nb = 0
        files_nb = 0

        _, repo_name = GitHelper.get_repo_details(repo)

        repo_files_url = f"https://opendev.org/api/v1/repos/openstack/{repo_name}/languages"
        files_response = RequestHelper.get_api_response(repo_files_url, self.org["add_token"])

        for key, value in files_response.items():
            files_nb += value
            
            if key == "Puppet":
                iac_files_nb += value
                
        return iac_files_nb, files_nb


    # The repository must have at least two commits per month
    def __apply_criteria_3(self, repo):
        monthly_commits = {}
        return self.get_commits_per_page(repo, 1, self.org["per_page"], monthly_commits)


    # recursive method to calculate commits via pagination for repo
    def get_commits_per_page(self, repo, page_nb, per_page, monthly_commits):
        monthly_commits_threshold = 2

        owner_name, repo_name = GitHelper.get_repo_details(repo)
        commits_url = f"https://{self.org_url}/repos/{owner_name}/{repo_name}/commits?per_page={per_page}&page={page_nb}"
        commits_response = RequestHelper.get_api_response(commits_url, self.org["add_token"])

        # set monthly commits counter
        for commit in commits_response:
            commit_date = commit['commit']['author']['date']
            try:
                commit_date = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                commit_date = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%S%z')
            
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