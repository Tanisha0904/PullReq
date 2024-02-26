import csv
import json
from urllib.request import urlopen
import requests
from secrets_1 import GITHUB_TOKEN


def get_pull_requests(owner, repo, token):
    headers={
        'Authorization': f'token {token}',
        "Accept": "application/vnd.github+json"
    }
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    response = requests.get(url, headers=headers)
    
    print(response.status_code)
    print(response.links)
    # print(response.content)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch pull requests: {response.status_code}")
        return None
'''   
def get_code(token, pr):
    headers={
        'Authorization': f'token {token}',
        "Accept": "application/vnd.github+json"
    }
    # print(pr)
    if not pr or 'html_url' not in pr[0]:
        print("Invalid pull request data.")
        return None
    
    print(pr[0]['html_url'])
    # url = pr[0]['html_url']+'/files'
    url=""
    #https://github.com/grafana/grafana/pull/83361

    response = requests.get(url, headers=headers)
  
    # print(response.content)
    print(response)
    
    if response:
        return response.content
    else:
        print(f"Failed to fetch code: {response.status_code}")
        print("Response content:", response.content)  #response content for debugging
        return None
    
    
'''
def write_pull_requests_to_file(pull_requests, file_name, data):
    fields = ['number', 'title', 'body', 'changes_made']

    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        # Iterate over pull requests
        for pr in pull_requests:
            try:
                url=data.get(pr['number'], '')
                response = requests.get(url)
                if response.status_code == 200:
                    text = response.text.replace('\n', ' ')
                    data[pr['number']]=text
                    # print(data[pr['number']])
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                text=""
            # Prepare the row data
            row_data = {
                'number': pr['number'],
                'title': pr['title'],
                'body': pr['body'],
                # 'changes_made': text # Get changes_made from data dictionary
                'changes_made': data.get(pr['number'], '')  # Get changes_made from data dictionary
            }
            # Write the row to the CSV file
            writer.writerow(row_data)

'''            
def write_pull_requests_to_file(pull_requests, file_name, data):
    with open(file_name, 'w') as file:
        for pr in pull_requests:
        #     if 'CloudWatch' in pr['title']:
            file.write(f"#{pr['number']}: {pr['title']}, {pr['html_url']}, {pr['merged_at']}\n")     
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
        # file.write(f"{pull_requests[0]}")
    
'''
#------------------ get the code changes in a file------
            
def fetch_files_changed_in_pull_request(owner, repo, number_list, token):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    files_changed_dict = {}  # Dictionary to store files changed for each pull request

    for number in number_list:
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            pull_request_info = response.json()
            # files_changed = pull_request_info.get("diff_url", [])
            # files_changed = pull_request_info.get("patch_url", [])
            files_changed_url = pull_request_info.get("diff_url", "")
            files_changed_dict[number] = files_changed_url
            # print("====================================")
            # print(files_changed_url)
            # print("====================================")
            # # print(files_changed_dict)          
            
        else:
            print(f"Failed to fetch pull request info: {response.status_code}")
            return None
    return files_changed_dict

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


#-------------------------------------------------------
owner = 'grafana'
repo = 'grafana'
token = GITHUB_TOKEN
file_name = 'pull_requests.txt'
csv_file_path = "data.csv"
fields = ['number', 'title', 'body', 'changes_made']

pull_requests = get_pull_requests(owner, repo, token)


# data = json.loads(pull_requests)
number_list = [entry["number"] for entry in pull_requests]
print(number_list)

# pull_code=get_code(token, pull_requests)
pull_request_number=None
# TODO(high): fix this, pull_requests get it in proper format
# files_changed = fetch_files_changed_in_pull_request(owner, repo, pull_requests['number'], token)

files_changed_dict = fetch_files_changed_in_pull_request(owner, repo, number_list, token)

# if files_changed:
#     save_url_content_to_file(files_changed, "chnagesFromIndividualPR.txt")


if pull_requests:
    write_pull_requests_to_file(pull_requests, csv_file_path, files_changed_dict)
    # print(f"Pull requests written to {file_name}")
         
       
else:
    print("Failed to fetch pull requests")

# if pull_code:
#     with open("pull_code.txt", 'w') as file:
#         file.write(pull_code) 
#     print(f"Code changes written to pull_code.txt")     
# else:
#     print("Failed to fetch code")          

















