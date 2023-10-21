from os import getenv
from dotenv import load_dotenv

load_dotenv() 

def get_github_token():
    return getenv("GITHUB_TOKEN")