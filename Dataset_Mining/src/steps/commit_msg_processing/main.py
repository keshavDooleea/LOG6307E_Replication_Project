# 3.1.2. Commit message processing

from helpers.util import Util
from helpers.git import GitHelper
from helpers.request import RequestHelper
from helpers.json import JsonHelper
import re


class CommitMsgProcessing:
    def __init__(self, dataset):
        print("3.1.2. Commit message processing.")
        self.dataset = dataset

    def process(self):
        for org_item in self.dataset:
            repos = org_item["selected_repos"]
            org = org_item["name"]
            self.add_token = org_item["add_token"]        

            self.nb_puppet_files = {}
            self.nb_puppet_commits = 0

            Util.separate_line()
            print("Processing", len(repos), "repos for", org)

            for idx, repo in enumerate(repos):
                extended_commit_messages = []

                owner_name, repo_name = GitHelper.get_repo_details(repo)
                self.org_url = org_item["url"]
                per_page = org_item["per_page"]
                page_nb = 1
                self.handle_pagination(org, owner_name, repo_name, page_nb, per_page, extended_commit_messages, idx)
                
                # print(f"#{idx + 1}: ", repo_name)

                org_xcm = JsonHelper.read(f"output/extended_commit_messages/{org}.json")
                org_xcm[repo_name] = extended_commit_messages
                JsonHelper.write(org_xcm, f"output/extended_commit_messages/{org}.json")
            
            self.save_commit_infos(org)


    def handle_pagination(self, org, owner_name, repo_name, page_nb, per_page, extended_commit_messages, idx):
        print("repo", repo_name, ", page:", page_nb, ", nb_xcm:", self.nb_xcm)

        commits_url = f"https://{self.org_url}/repos/{owner_name}/{repo_name}/commits?per_page={per_page}&page={page_nb}"
        commits_response = RequestHelper.get_api_response(commits_url, self.add_token)

        if not commits_response:
            return
        
        for commit in commits_response:
            if org == "Openstack":
                extra_query = "/git"
            else:
                extra_query = ""
        
            commit_sha = commit["sha"]
            commit_sha_url = f"https://{self.org_url}/repos/{owner_name}/{repo_name}{extra_query}/commits/{commit_sha}"
            commit_sha_response = RequestHelper.get_api_response(commit_sha_url, self.add_token)
           
            files = commit_sha_response["files"]

            for file in files:
                if GitHelper.is_iac_file(file["filename"]):
                    # First, we extract commits that were used to modify at least one IaC script
                    if not (commit_sha in self.nb_puppet_files):
                        self.nb_puppet_files[commit_sha] = 1
                    
                    # Second, we extract the message of the commit identified from the previous step.
                    commit_msg = commit["commit"]["message"]
                    self.nb_puppet_commits += 1

                    # Third, we extract the identifier and use that identifier to extract the summary of the issue.
                    issue_identifier = re.search(r"#(\d+)", commit_msg)

                    if issue_identifier:
                        issue_number = issue_identifier.group(1)
                        issue_url = f"https://{self.org_url}/repos/{owner_name}/{repo_name}/issues/{issue_number}"
                        issue_response = RequestHelper.get_api_response(issue_url, self.add_token)

                        # Fourth, we combine the commit message with any existing issue summary to construct the message for analysis
                        try:
                            issue_summary = issue_response["title"]
                            extended_message = f"Commit Message: {commit_msg}\nIssue Summary: {issue_summary}"
                        except:
                            extended_message = f"Commit Message: {commit_msg}"

                        self.nb_xcm += 1
                        extended_commit_messages.append(extended_message)
            
        
        # 25 is ideal
        if len(commits_response) == per_page and page_nb < 5:
            self.handle_pagination(org, owner_name, repo_name, page_nb + 1, per_page, extended_commit_messages, idx)


    def save_commit_infos(self, org):

        nb_pupp_scripts = 0

        for key in self.nb_puppet_files:
            nb_pupp_scripts += 1

        data = {
            "Puppet Scripts": nb_pupp_scripts,
            "Commits with Puppet Scripts": self.nb_puppet_commits,
        }

        JsonHelper.write(data, f'output/defective_commits/{org}.json')
