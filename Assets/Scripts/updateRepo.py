import requests
import base64
import json
from job import Job

def writeContent(repo_owner, repo_name, access_token, branch_name, encoded_html, jobs):
    #########################################
    ## 1 -- WRITE THE PYTHON FILE INTO GITHUB
    #########################################

    # Construct the API endpoint
    file_path = 'ads.html'
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"

    # Set the request headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Make a GET request to retrieve the current file information
    response = requests.get(url, headers=headers)
    file_data = response.json()

    # Extract the current sha hash
    current_sha = file_data["sha"]

    # Prepare API request parameters
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'message': 'Update table.html',
        'content': encoded_html,
        'branch': branch_name,
        "sha": current_sha
    }

    # Send API request to create/update file
    response = requests.put(api_url, headers=headers, json=data)

    if response.status_code == 200:
        print('Table.html successfully written to GitHub repository')
    else:
        print(f'Error writing table.html to GitHub repository. Status code: {response.status_code}')
        print(response.text)

    #######################################
    ## 2 -- WRITE THE JSON FILE INTO GITHUB
    #######################################

    # Iterate over the jobs list to convert date into JSON serializable format
    for job in jobs:
        # Convert the date field to a JSON serializable format
        job.publish_date = job.publish_date.isoformat()

    job_data = [job.__dict__ for job in jobs]
    json_string = json.dumps(job_data)

    # Encode the content to Base64
    encoded_content = base64.b64encode(json_string.encode()).decode()

    file_path = 'Assets/JobsLib/jobs.json'
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'

    # Check if the file already exists to get the 'sha' parameter
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        # File exists, get the 'sha' parameter
        file_details = response.json()
        sha = file_details['sha']
    else:
        # File doesn't exist, 'sha' parameter will be empty
        sha = ""

    # Request payload
    payload = {
        "message": "Update JSON file",
        "content": encoded_content,
        "sha": sha
    }

    # Make the API request to create or update the file
    response = requests.put(url, json=payload, headers={"Authorization": f"Bearer {access_token}"})

    # Check the response
    if response.status_code == 200 or response.status_code == 201:
        print("The \"jobs\" JSON file was created/updated successfully.")
    else:
        print(f"Error: {response.json()['message']}")

    return None

def readContent(repo_owner, repo_name, access_token, file_path):

    exisitng_jobs = []

    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'

    # Make the API request to create or update the file
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})

    # Check the response
    if response.status_code == 200:
        # File content retrieved successfully
        file_details = response.json()
        content = file_details['content']

        # Decode the Base64-encoded content
        decoded_content = base64.b64decode(content).decode()

        # Process the JSON data
        json_data = json.loads(decoded_content)

        # Process the JSON data
        for job in json_data:
            # Create an instance of the Job class
            job_instance = Job()

            job_instance.id = job["id"]
            job_instance.publish_date = job["publish_date"]
            job_instance.title = job["title"]
            job_instance.grade = job["grade"]
            job_instance.deadline = job["deadline"]

            exisitng_jobs.append(job_instance)
    else:
        print(f"Error: {response.json()['message']}")
    
    return exisitng_jobs