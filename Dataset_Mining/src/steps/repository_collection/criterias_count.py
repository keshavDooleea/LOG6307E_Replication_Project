from helpers.json import JsonHelper

class CriteriaCount:

    def __init__(self, org: str):
        self.org = org
        self.criterias_count = {}
        self.criterias_count["c1"] = 0
        self.criterias_count["c2"] = 0
        self.criterias_count["c3"] = 0
        self.criterias_count["repos"] = []

    def get_repos(self):
        return self.criterias_count["repos"]
    
    def get_repos_length(self):
        return len(self.criterias_count["repos"])
    
    def increase_count(self, criteria: str):
        self.criterias_count[criteria] += 1

    def add_repo(self, repo: list):
        self.criterias_count["repos"].append(repo)

    def print_count(self):
        print("Organization :", self.org)
        print("Criteria 1   :", self.criterias_count["c1"])
        print("Criteria 2   :", self.criterias_count["c2"])
        print("Criteria 3   :", self.criterias_count["c3"])
        # print("Total repos  :", self.get_repos_length())

    def save_count(self):
        data = {
                "Criteria 1": self.criterias_count["c1"],
                "Criteria 2": self.criterias_count["c2"],
                "Criteria 3": self.criterias_count["c3"]
        }

        JsonHelper.write(data, f'output/criterias_count/{self.org}.json')
