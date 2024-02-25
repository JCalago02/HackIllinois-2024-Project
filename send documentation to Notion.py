# -*- coding: utf-8 -*-
NOTION_API_KEY = 'secret_oQNXJ1hHm4tjPwhjFUB47fNkT19RQq8Vns8kZVwzBw3'
PAGE_ID = 'e13eaf2a0dab409c84e4b541eee8a0c3'
DATABASE_ID = 'b97ac1b4c573431bb43cba64d659bb97'

import requests
import json
import base64

def retrieve_page_blocks(page_id, headers):
    get_blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    blocks_response = requests.get(get_blocks_url, headers=headers)
    if blocks_response.status_code == 200:
        return blocks_response.json().get("results", [])
    else:
        print("Failed to retrieve page blocks.")
        print(blocks_response.text)
        return []

def update_or_create_content(page_id, headers, file, description):
    existing_blocks = retrieve_page_blocks(page_id, headers)
    update_properties_url = f"https://api.notion.com/v1/pages/{page_id}"
    properties_data = {
        "Authors": {
            "multi_select": [{"name": author} for author in authors]
        },
        "Last edited": {
            "rich_text": [{"text": {"content": last_edited}}]
        }
    }
    properties_response = requests.patch(update_properties_url, headers=headers, json={"properties": properties_data})
    if properties_response.status_code != 200:
        print("Failed to update the properties of the page.")
        return False

    file_block_id = None
    description_updated = False

    # Search for an existing block with the filename
    for block in existing_blocks:
        if block['type'] == 'heading_3' and file in block['heading_3']['text'][0]['text']['content']:
            file_block_id = block['id']
            continue  # Continue to find the next block which should be the description

        # If the file block was found, the next text block is assumed to be the description
        if file_block_id and block['type'] == 'paragraph':
            update_block_url = f"https://api.notion.com/v1/blocks/{block['id']}"
            update_data = {
                "paragraph": {
                    "text": [{"type": "text", "text": {"content": description}}]
                }
            }
            update_response = requests.patch(update_block_url, headers=headers, json=update_data)
            description_updated = update_response.status_code == 200
            break  # Once the description is updated, exit the loop

    if not description_updated:
        # If the filename is not found or description not updated, add both as new blocks
        create_blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        create_data = {
            "children": [
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "text": [{"type": "text", "text": {"content": file}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "text": [{"type": "text", "text": {"content": description}}]
                    }
                }
            ]
        }
        create_response = requests.patch(create_blocks_url, headers=headers, json=create_data)
        description_updated = create_response.status_code == 200

    return description_updated


def add_or_update_entry_to_notion_database(tag, file, description, authors, last_edited):
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16"
    }

    authors_multi_select = [{"name": author} for author in authors]
    # Search for an existing entry with the same tag/category
    query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    query_data = {
        "filter": {
            "property": "Category",
            "title": {
                "equals": tag
            }
        }
    }
    search_response = requests.post(query_url, headers=headers, json=query_data)

    if search_response.status_code != 200:
        print("Failed to search the database.")
        print(f"Status Code: {search_response.status_code}")
        print(f"Response Text: {search_response.text}")
        return

    search_results = search_response.json()
    existing_pages = search_results.get("results", [])

    # If an existing page with the same tag is found, update it
    if existing_pages:
        page_id = existing_pages[0]["id"]
        if update_or_create_content(page_id, headers, file, description):
            print("Page content updated successfully.")
        else:
            print("Failed to update page content.")

    else:
        # Create a new page
        data = {
          "parent": {"database_id": DATABASE_ID},
          "properties": {
              "Category": {
                  "title": [{"text": {"content": tag}}]
              },
              "Authors": {
                  "multi_select": authors_multi_select
              }, "Last edited": {
                  "rich_text": [{"text": {"content": last_edited}}]
              }
          },
          "children": [  # Use children to add content blocks to the page
              {
                  "object": "block",
                  "type": "heading_3",
                  "heading_3": {
                      "text": [{"type": "text", "text": {"content": file}}]
                  }
              },
              {
                  "object": "block",
                  "type": "paragraph",
                  "paragraph": {
                      "text": [{"type": "text", "text": {"content": description}}]
                  }
              }
          ]
        }
        # Use the /pages endpoint to create a new page (entry) in the database
        response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)

        # Check the response
        if response.status_code == 200:
            print("New entry added to the database successfully.")
            print(response.json())
        else:
            print("Failed to add entry to the database.")
            print(f"Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")

def getLatestCommitFiles():
  url_commit = "https://api.github.com/repos/JCalago02/HackIllinois-2024-Project/commits"
  response_commit = requests.get(url_commit)
  data = response_commit.json()
  latest_commit_sha = data[0]['sha']
  commit_detail_url = f"https://api.github.com/repos/JCalago02/HackIllinois-2024-Project/git/trees/{latest_commit_sha}?recursive=1"
  commit_response = requests.get(commit_detail_url)
  commit_data = commit_response.json()
  files = [item for item in commit_data['tree'] if item['type'] == 'blob']
  return files

curr_commit = getLatestCommitFiles()

def convertFile(files):
  all_content = []
  for i in range(len(files)):
    file_sha = files[i]['sha']
    url_file_content = f"https://api.github.com/repos/JCalago02/HackIllinois-2024-Project/git/blobs/{file_sha}"
    response = requests.get(url_file_content)
    file_data = response.json()
    content = base64.b64decode(file_data['content'])
    all_content.append(str(content))
  return all_content

all_content = convertFile(curr_commit)

def extractContent(curr_content):
  file_info = dict()
  terms = curr_content.split('/')
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

for i in range(0, len(all_content)):
  now = datetime.now()
  file_info, flags = extractContent(all_content[i])
  tag = ''
  description = ''
  file = ''
  authors = ''
  if ("@category" in file_info): tag = file_info["@category"]
  if ("@description" in file_info): description = file_info["@description"]
  if ("@file" in file_info): file = file_info["@file"]
  if ("@author" in file_info): authors = file_info["@author"].split(",")
  last_edited = str(now)[:19]
  if (tag != ''):
    new_entry = add_or_update_entry_to_notion_database(tag, file, description, authors, last_edited)

# A dummy test case
# from datetime import datetime
# now = datetime.now()
# tag = "backend comp"
# description = "this change should be published!"
# file = "test2.py"
# authors = ["Maxwell Yang", "Jericho Calago!", "Abhinav Khanduja!"]
# last_edited = str(now)[:19]
# new_entry = add_or_update_entry_to_notion_database(tag, file, description, authors, last_edited)