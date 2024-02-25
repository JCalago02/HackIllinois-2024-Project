'''
/doc_start***/
@category Backend Folders/
@file to-json.py/
@description a file that writes commit history to json file/
@author Abhinav Khanduja/
/doc_end***/
'''
from dataclasses import dataclass
from datetime import *
import json
@dataclass
class commit:
    def __init__(self, message: str, author: str, avatar: str, branch: str, commit_time: datetime, merge_into: str, sha: str):
        self.message = message
        self.author = author
        self.avatar = avatar
        self.branch = branch
        self.commit_time = commit_time
        self.merge_into = merge_into
        self.sha = sha
    
    def __lt__(self, other):
        return self.commit_time < other.commit_time

import requests
shatoname = {}
names = []
BRANCH = 'main'

def committodict(commy: commit):
    spongebob = {}
    spongebob['message'] = commy.message
    spongebob['author'] = commy.author
    spongebob['avatar'] = commy.avatar
    spongebob['branch'] = commy.branch
    spongebob['mergeInto'] = commy.merge_into
    return spongebob    
    

def get_branch_names_from_commit_message(commit_message):
    # This function assumes the default GitHub merge commit message format
    # "Merge branch 'feature-branch' into 'main'"
    # You may need to customize this parsing logic based on your repo's conventions.
    if " into " in commit_message and "'" in commit_message:
        parts = commit_message.split(" into ")
        feature_branch_part = parts[0]
        base_branch_part = parts[1]
        feature_branch = feature_branch_part.split("'")[1]  # Extracting the feature branch name
        base_branch = base_branch_part.split("'")[0]  # Extracting the base branch name
        return feature_branch, base_branch
    else:
        return None, None  # Could not determine branch names from the message

# Function to get a list of merge commits from a repository using the GitHub API
def get_merge_commits_with_branches(owner, repo, sha, auth_token=None):
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if auth_token:  # If authentication is provided
        headers["Authorization"] = f"token {auth_token}"

    merge_commits_info = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        params = {"per_page": per_page, "page": page}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        commits = response.json()

        if not commits:
            break

        for commite in commits:
            if len(commite['parents']) > 1:
                if(sha == commite['sha']):
                    commit_sha = commite['sha']
                    commit_url = commite['url']
                    commit_response = requests.get(commit_url, headers=headers)
                    commit_response.raise_for_status()
                    commit_data = commit_response.json()
                    commit_message = commit_data['commit']['message']
                    feature_branch, base_branch = get_branch_names_from_commit_message(commit_message)

                    if feature_branch and base_branch:
                        ting = base_branch
                    
                    return ting
        page += 1

    return ting


def get_branches_for_commit(user: str, repo: str, commit_sha: str, access_token: str='')-> list[str]:
    #get a list of branch names for the given commit
    
    branches = []
    url = url = f"https://api.github.com/repos/{user}/{repo}/commits/{commit_sha}/branches-where-head"
    headers = {
        'Authorization': f'token {ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    } if access_token else {}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        branches_data = response.json()
        for branch_info in branches_data:
            branches.append(branch_info['name'])
    else:
        raise Exception(f"Failed to fetch branches for commit {commit_sha}: {response.content}")

    return branches
    
    
ACCESS_TOKEN = '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'
USER = 'JCalago02'
REPO = 'HackIllinois-2024-Project'

def get_pull_requests(user, repo, state='all'):
    """
    Get a list of all pull requests in a specified GitHub repository.

    :param user: Username of the repository owner
    :param repo: Repository name
    :param state: State of the pull requests. Can be 'open', 'closed', or 'all'.
    :return: A list of pull request information
    """
    url = f"https://api.github.com/repos/{user}/{repo}/pulls"
    headers = {
        'Authorization': f'token {ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    params = {'state': state}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        pr_data = response.json()
        #print(pr_data)
        sha_branch_dict = {}
        for pr in pr_data:
            #print(pr['base']['sha'])
            #print(pr['base']['ref'])
            sha_branch_dict[pr['base']['sha']] = pr['base']['ref']
        
        return sha_branch_dict
    else:
        raise Exception(f'Failed to fetch pull requests: {response.content}')

# Example usage:



def get_commits(user: str, repo: str, branch: str, access_token: str = '') -> list[commit]:
    commits_list = []
    url = f"https://api.github.com/repos/{USER}/{REPO}/commits?sha={branch}"
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json',
    } if access_token else {}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commits = response.json()
        for commit_info in commits:
            commit_sha = commit_info['sha']
            timestamp = commit_info['commit']['author']['date']
            commit_time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
            
            mivar = ''
            merge = "Merge branch"
            into = "into"
            if(merge in commit_info['commit']['message'] and into in commit_info['commit']['message']):
                merges_with_branches = get_merge_commits_with_branches(USER, REPO, commit_sha, ACCESS_TOKEN)
                mivar = merges_with_branches
                
                
            commit_data = commit(
                message=commit_info['commit']['message'],
                author=commit_info['commit']['author']['name'],
                avatar=commit_info['author']['avatar_url'] if commit_info['author'] else '',
                branch=branch,
                commit_time=commit_time,
                merge_into=mivar,
                sha= commit_info['sha']
            )
            
            commits_list.append(commit_data)

    else: 
        raise Exception(f"Failed to fetch commits: {response.content}")
    
    return commits_list

    
try:
    commitlist = []
    api_url = f"https://api.github.com/repos/{USER}/{REPO}/branches"
    
    headers = {
        'Authorization': f'token {ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        branches_data = response.json()
        
        for branch in branches_data:
            names.append(branch['name'])
            
    names.reverse()
    shatoname = get_pull_requests(USER, REPO)
    for bname in names:
        commits = get_commits(USER, REPO, bname, ACCESS_TOKEN)
        for commite in commits:
            flag = 0
            for i in commitlist:
                if(i.sha == commite.sha):
                    flag = 1
                    
            if(flag == 0):
                commitlist.append(commite)
        
    commitlist.sort()
            
    commitlist.reverse()
    commitlist = commitlist[:26]
    commitlist.reverse()

    patrick = []
    for sandy in commitlist:
        patrick.append(committodict(sandy))
    
    json_string = json.dumps(patrick)
    print(json_string)
    with open("data.json", "w") as outfile:
        outfile.write(json_string)
    
    
except Exception as e:
    print(e)