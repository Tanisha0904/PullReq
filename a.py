import json
from urllib.request import urlopen


data=urlopen('https://github.com/grafana/grafana/pull/83361').read()
# print(data)
    
try:
    # Attempt to decode the data as JSON
    json_data = json.loads(data)
    print(json_data)
except json.JSONDecodeError:
    # If decoding fails, print an error message
    print("Failed to decode data as JSON")



# Check if there are more pages
    while 'next' in response.links:
        next_url = response.links['next']['url']
        
        # Make a GET request to fetch the next page of results
        response = requests.get(next_url)
        if response.status_code == 200:
            # Extract code changes from the API response
            code_changes = response.json()
            
            # Process code changes for the current page
            for change in code_changes:
                print(f"File: {change['filename']}")
                print(f"Additions: {change['additions']}, Deletions: {change['deletions']}")
                print(f"Changes: {change['changes']}")
        else:
            print(f"Failed to fetch next page of results. Status code: {response.status_code}")
else:
    print(f"Failed to fetch pull request information. Status code: {response.status_code}")