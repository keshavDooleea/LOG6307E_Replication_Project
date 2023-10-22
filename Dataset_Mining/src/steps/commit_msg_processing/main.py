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
        for org in self.dataset:
            repos = self.dataset[org]

            Util.separate_line()
            print("Processing", len(repos), "repos for", org)

            extracted_commits = []
            extended_commit_messages = {}

            for idx, repo in enumerate(repos):
                owner_name, repo_name = GitHelper.get_repo_details(repo)
                extended_commit_messages[repo_name] = []
                self.org_url = "api.github.com"
                per_page = 100
                page_nb = 1
                commits_url = f"https://{self.org_url}/repos/{owner_name}/{repo_name}/commits?per_page={per_page}&page={page_nb}"
                commits_response = RequestHelper.get_api_response(commits_url)

                # First, we extract commits that were used to modify at least one IaC script
                for commit in commits_response:
                    commit_sha = commit["sha"]
                    commit_sha_url = f"https://api.github.com/repos/{owner_name}/{repo_name}/commits/{commit_sha}"
                    commit_sha_response = RequestHelper.get_api_response(commit_sha_url)

                    files = commit_sha_response["files"]

                    for file in files:
                        if GitHelper.is_iac_file(file["filename"]):
                            extracted_commits.append(commit)
                            break

                # Second, we extract the message of the commit identified from the previous step.
                for commit in extracted_commits:
                    commit_msg = commit["commit"]["message"]

                    # Third, we extract the identifier and use that identifier to extract the summary of the issue.
                    issue_identifier = re.search(r"#(\d+)", commit_msg)

                    if issue_identifier:
                        issue_number = issue_identifier.group(1)
                        issue_url = f"https://api.github.com/repos/{owner_name}/{repo_name}/issues/{issue_number}"
                        issue_response = RequestHelper.get_api_response(issue_url)

                        # Fourth, we combine the commit message with any existing issue summary to construct the message for analysis
                        try:
                            issue_summary = issue_response["title"]
                            extended_message = f"Commit Message: {commit_msg}\nIssue Summary: {issue_summary}"
                        except:
                            extended_message = f"Commit Message: {commit_msg}"

                        extended_commit_messages[repo_name].append(extended_message)
                
                print(f"#{idx + 1}: Found", len(extended_commit_messages[repo_name]), "extended commit messages for", repo_name)

                org_xcm = JsonHelper.read(f"output/extended_commit_messages/{org}.json")
                org_xcm[repo_name] = extended_commit_messages[repo_name]
                JsonHelper.write(org_xcm, f"output/extended_commit_messages/{org}.json")
