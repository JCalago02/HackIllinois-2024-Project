import requests
import base64

def getLatestCommitFiles():
  url_commit = "https://api.github.com/repos/maxwelltheyang/HackIllinois-2024-Project/commits"
  response_commit = requests.get(url_commit)
  data = response_commit.json()
  latest_commit_sha = data[0]['sha']
  commit_detail_url = f"https://api.github.com/repos/maxwelltheyang/HackIllinois-2024-Project/git/trees/{latest_commit_sha}?recursive=1"
  commit_response = requests.get(commit_detail_url)
  commit_data = commit_response.json()
  files = [item for item in commit_data['tree'] if item['type'] == 'blob']
  return files

print(getLatestCommitFiles())

def convertFile(files):
  all_content = []
  for i in range(len(files)):
    file_sha = files[i]['sha']
    url_file_content = f"https://api.github.com/repos/maxwelltheyang/HackIllinois-2024-Project/git/blobs/{file_sha}"
    response = requests.get(url_file_content)
    file_data = response.json()
    content = base64.b64decode(file_data['content'])
    all_content.append(str(content))
  return all_content

content = convertFile(getLatestCommitFiles())

def extractContent(content):
  file_info = dict()
  terms = content.split('/')
  flags = []
  canCheck = False
  for term in terms:
    if (term == "doc_start***"):
      canCheck = True
    elif (canCheck == True):
      start = term.find('@')
      if (start != -1):
        subterm = term[start:]
        index = subterm.find(' ')
        flag = term[start:start + index]
        flags.append(flag)
        info = subterm[index + 1:]
        file_info.update({flag : info})
    elif (term == "doc_end***"):
      canCheck = False
  return file_info, flags

for encoded in content:
  print(extractContent(encoded))