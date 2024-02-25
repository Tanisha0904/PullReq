import requests
from secrets_1 import GITHUB_TOKEN


def get_pull_requests(owner, repo, token):
    headers={
        'Authorization': f'token {token}',
        "Accept": "application/vnd.github+json"
    }
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    response = requests.get(url, headers=headers)
    
    # print(response.status_code)
    # print(response.content)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch pull requests: {response.status_code}")
        return None
    
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
    # pull_request_url = pr[0]['html_url']
    # url = pull_request_url + '/files'
    url='https://github.com/grafana/grafana/pull/83361/files'
    response = requests.get(url, headers=headers)
        
        # print(response.status_code)
        # print(response.content)
    # print(response.json())
    if response.status_code == 200:
        # return response.json()
        print("done")
    else:
        print(f"Failed to fetch code: {response.status_code}")
        return None
    


def write_pull_requests_to_file(pull_requests, file_name):
    with open(file_name, 'w') as file:
        for pr in pull_requests:
            if 'CloudWatch' in pr['title']:
                file.write(f"#{pr['number']}: {pr['title']}, {pr['html_url']}, {pr['merged_at']}\n")                

        # file.write(f"{pull_requests[0]}")
    





# Example usage:
owner = 'grafana'
repo = 'grafana'
token = GITHUB_TOKEN
file_name = 'pull_requests.txt'

pull_requests = get_pull_requests(owner, repo, token)
pull_code=get_code(token, pull_requests)

if pull_requests:
    # for pr in pull_requests:
    #     print(f"PR #{pr['number']}: {pr['title']}")
    write_pull_requests_to_file(pull_requests, file_name)
    # print(f"Pull requests written to {file_name}")
    # print(pull_requests[0])

        
else:
    print("Failed to fetch pull requests")

if pull_code:
    with open("pull_code.txt", 'w') as file:
        file.write(pull_code)      
else:
    print("Failed to fetch code")          


