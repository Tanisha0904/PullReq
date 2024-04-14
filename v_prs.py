from collections import defaultdict
import csv
import json
import re
import requests
from secrets_1 import GITHUB_TOKEN


def get_response_from_version_compare_api(
    owner, repo, token, version_prev, version_curr
):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    url = f"https://api.github.com/repos/{owner}/{repo}/compare/{version_prev}...{version_curr}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # print(response.json())
        # with open("message_data.json", "w", encoding="utf-8") as json_file:
        #     json.dump(response.json(), json_file, indent=4)
        return response.json()

    else:
        print(
            f"Failed to fetch commits from version {version_prev} to version {version_curr}: {response.status_code}"
        )
        return None


def get_pr_data(number, file_name):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    url = f"https://api.github.com/repos/grafana/grafana/pulls/{number}"
    response = requests.get(url, headers=headers)
    json_data = []
    if response.status_code == 200:
        pr = response.json()
        label_names = set()
        labels = pr.get("labels", [])
        for label in labels:
            label_name = label.get("name", "")  # Get the name of the label
            label_names.add(label_name)  # Add the label name to the set
        pr_data = {
            "number": pr["number"],
            "title": pr["title"],
            "body": pr["body"],
            "labels": list(label_names),  # Get changes_made from data dictionary
        }
        json_data.append(pr_data)
        return pr_data

    else:
        print(f"Failed to fetch pull requests: {response.status_code}")
        return None

    # Write data to JSON file
    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4)


def write_pr_data_to_file(api_response, file_name, data={}):
    """
    file_path = "D:\BMC\Pull_Req\message_data.json"
    with open(file_path, "r") as json_file:
        api_response = json.load(json_file)
    """

    message_json_data = []
    pr_number_counts = defaultdict(int)
    pattern = r"\(#(\d+)\)"  # pattern to match "(#number)" in the commit messages

    data = api_response["commits"]
    just_messages = []
    i = 0
    for commit_data in data:
        commit_message = commit_data["commit"]["message"]
        date_time = commit_data["commit"]["committer"]["date"]
        just_messages.append(commit_message)
        match = re.search(pattern, commit_message)

        if match:
            number = match.group(1)  # group(1) will capture the number inside (#number)
            title = commit_message.split(f"(#{number})")[
                0
            ].strip()  # Extract title before "(#number)"
            pr_number_counts[number] += 1

            # get the body and labels

            message_json_data.append(get_pr_data(number, file_name))
            # message_json_data.append({"number": number, "title": title})

            # message_json_data.append({"number": number})
            i += 1
            # print(number + title, end="\n--")

    # Sort message_json_data based on the "date_time" key in each dictionary
    sorted_data = sorted(message_json_data, key=lambda x: x["number"])
    # Write data to JSON file
    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump(sorted_data, json_file, indent=4)
    # print(pr_number_counts)


if __name__ == "__main__":
    # Input the versions from the
    # version_prev = input("Enter the first version (e.g., v10.4.1): ")
    # version_curr = input("Enter the second version (e.g., v10.2.6): ")

    version_prev = "v10.2.5"
    version_curr = "v10.2.6"

    owner = "grafana"
    repo = "grafana"
    token = GITHUB_TOKEN
    file_name = f"{version_prev}_{version_curr}_pr_list.json"

    # Get user input for versions

    api_response = get_response_from_version_compare_api(
        owner, repo, token, version_prev, version_curr
    )

    if api_response:
        write_pr_data_to_file(api_response, file_name)
        print(f"Commits' data written to {file_name}")
    else:
        print("Failed to fetch the commits data.")
