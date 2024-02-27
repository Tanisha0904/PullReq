from urllib.request import urlopen
import requests
from secrets_1 import GITHUB_TOKEN


def fetch_files_changed_in_pull_request(owner, repo, pull_request_number, token):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_request_number}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pull_request_info = response.json()
        files_changed = pull_request_info.get("diff_url", [])
        # files_changed = pull_request_info.get("patch_url", [])
        print(files_changed)
        return files_changed
    else:
        print(f"Failed to fetch pull request info: {response.status_code}")
        return None
'''
def fetch_file_content(file_url):
    response = requests.get(file_url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch file content: {response.status_code}")
        return None
'''
def save_url_content_to_file(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"Content from {url} successfully saved to {filename}")
        else:
            print(f"Failed to fetch content from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


owner = "grafana"
repo = "grafana"
pull_request_number = 83361
token = GITHUB_TOKEN
filename="chnagesFromIndividualPR.txt"
files_changed = fetch_files_changed_in_pull_request(owner, repo, pull_request_number, token)
if files_changed:
    save_url_content_to_file(files_changed, filename)