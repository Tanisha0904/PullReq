import csv
import json
import requests
from secrets_1 import GITHUB_TOKEN

def get_pull_requests(owner, repo, token):
    headers = {
        'Authorization': f'token {token}',
        "Accept": "application/vnd.github+json"
    }
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    response = requests.get(url, headers=headers)

    # '''
    # if theres no pagination
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch pull requests: {response.status_code}")
        return None
    print(response.status_code)
    # '''
    print("Rate limit:", response.headers.get('X-RateLimit-Limit'))
    print("Remaining requests:", response.headers.get('X-RateLimit-Remaining'))
    print("Pagination links:", response.links)

    if response.status_code == 200:
        data = response.json()

        while 'next' in response.links:
            next_url = response.links['next']['url']
            response = requests.get(next_url, headers=headers)
            if response.status_code == 200:
                data += response.json()
            else:
                print(f"Failed to fetch next page of results. Status code: {response.status_code}")
                break

        return data
    else:
        print(f"Failed to fetch pull requests: {response.status_code}")
        return None

"""
def write_pull_requests_to_file(pull_requests, file_name, data={}):
    fields = ['number', 'title', 'body', 'changes_made']
    label_names = set()
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        # Iterate over pull requests

        for pr in pull_requests:
            # try:
            #     url=data.get(pr['number'], '')
            #     response = requests.get(url)
            #     if response.status_code == 200:
            #         text = response.text.replace('\n', ' ')
            #         data[pr['number']]=text
            #         # print(data[pr['number']])
            # except Exception as e:
            #     print(f"An error occurred: {str(e)}")
            #     text=""
            # Prepare the row data

            labels = pr.get(
                "labels", []
            )  # Get the list of labels for the current pull request
            for label in labels:
                label_name = label.get("name", "")  # Get the name of the label
                label_names.add(label_name)
            row_data = {
                "number": pr["number"],
                "title": pr["title"],
                "body": pr["body"],
                # 'changes_made': text # Get changes_made from data dictionary
                "changes_made": data.get(
                    pr["number"], ""
                ),  # Get changes_made from data dictionary
                "labels": list(label_names),
            }
            # Write the row to the CSV file
            writer.writerow(row_data)


"""


def write_pull_requests_to_file(pull_requests, file_name, data={}):
    # Iterate over pull requests and prepare data
    json_data = []

    for pr in pull_requests:
        label_names = set()
        labels = pr.get(
            "labels", []
        )  # Get the list of labels for the current pull request
        for label in labels:
            label_name = label.get("name", "")  # Get the name of the label
            label_names.add(label_name)  # Add the label name to the set

        pr_data = {
            "number": pr["number"],
            "title": pr["title"],
            "body": pr["body"],
            "changes_made": data.get(pr["number"], ""),
            "labels": list(label_names),  # Get changes_made from data dictionary
        }
        json_data.append(pr_data)

    # Write data to JSON file
    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4)


# ------------writing pull requests data to a text fil-------------
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
# ------------------ get the code changes in a csv file-----------

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
            # files_changed_url = pull_request_info.get("patch_url", "")
            files_changed_url = pull_request_info.get("diff_url", "")
            files_changed_dict[number] = files_changed_url
            # print(files_changed_url)
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


# ------------------------driver code-------------------------------
owner = 'grafana'
repo = 'grafana'
token = GITHUB_TOKEN
file_name = 'pull_requests.txt'
csv_file_path = "data.csv"
json_file_path = "data_2.json"
fields = ['number', 'title', 'body', 'changes_made']

pull_requests = get_pull_requests(owner, repo, token)

number_list = [entry["number"] for entry in pull_requests]
print(number_list)

pull_request_number=None

# files_changed_dict = fetch_files_changed_in_pull_request(owner, repo, number_list, token)
files_changed_dict = {}
if pull_requests:
    write_pull_requests_to_file(pull_requests, json_file_path, files_changed_dict)
    print(f"Pull requests' data written to {csv_file_path}")


else:
    print("Failed to fetch pull requests")
