import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import base64
from datetime import date
import os
import re
from dotenv import load_dotenv
from job import Job
from datetime import date
import json

def generate_fancy_html_table(array1, array2, array3, array4):
    html = f'''
    <html>
    <head>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
                font-family: Arial, sans-serif;
            }}
            th, td {{
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            tr:nth-child(even) {{
                background-color: #dddddd;
            }}
            .last-update {{
                position: absolute;
                top: 10px;
                right: 10px;
                font-size: 12px;
                font-family: "Trebuchet MS", Arial, sans-serif;
                color: #777777;
            }}
        </style>
    </head>
    <body>
        
        <table>
            <thead>
                <tr>
                    <th>Publish Date</th>
                    <th>Title</th>
                    <th>Grade</th>
                    <th>Deadline</th>
                </tr>
            </thead>
            <tbody>
    '''

    for row1, row2, row3, row4 in zip(array1, array2, array3, array4):
        html += f'''
                <tr>
                    <td>{row1}</td>
                    <td>{row2}</td>
                    <td>{row3}</td>
                    <td>{row4}</td>
                </tr>
        '''

    html += '''
            </tbody>
        </table>
        <span id="last-update" class="last-update"></span>
        <script>
            // Fetch the last commit date from GitHub API
            fetch('https://api.github.com/repos/aytuncilhan/Personal-Website/commits')
                .then(response => response.json())
                .then(data => {
                    const lastCommitDate = new Date(data[0].commit.committer.date);
                    const formattedDate = lastCommitDate.toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        hour: 'numeric',
                        minute: 'numeric'
                    });
                    document.getElementById('last-update').textContent = `Last Updated: ${formattedDate}`;
                })
                .catch(error => console.error(error));
        </script>
    </body>
    </html>
    '''

    return html

# GitHub repository details
repo_owner = 'aytuncilhan'
repo_name = 'Personal-Website'
branch_name = 'main'
load_dotenv()
access_token = os.getenv("ACCESS_TOKEN")

### RETRIEVE ALREADY EXISTING JOBS

exisitng_jobs = []

file_path = 'Assets/JobsLib/jobs.json'
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


# Crawl Job Website

url = 'https://nato.taleo.net/careersection/2/jobsearch.ftl?lang=en'
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')
# Find specific elements using CSS selectors
from bs4 import BeautifulSoup
import re

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the script tag containing the JavaScript code
script_tags = soup.find_all('script', text=re.compile(r'api\.fillInterface'))

desired_arguments = None

for script_tag in script_tags:
    # Extract the JavaScript code from the script tag
    javascript_code = script_tag.text

    # Use regular expressions to extract the input arguments
    pattern = r'api\.fillList\(["\'](.*?)["\'], (.*?)\);'  # Regular expression pattern to match the arguments
    match = re.search(pattern, javascript_code)

    if match and match.group(1) == 'requisitionListInterface':
        desired_arguments = match.group(2)  # Extract the arguments
        break

pattern = r'\[(.*?)\]'  # Regular expression pattern to match the content within square brackets
matches = re.findall(pattern, desired_arguments)

final_str = matches[0]

# Split the cleaned string at the delimiter ', '
items_array = final_str.split('\',\'')
items_array_enum = enumerate(items_array, 1)

jobs = []  # A list to store Job objects

publishDate = []
deadline = []
grade = []
title = []

# Create an instance of the Job class
job_instance = Job()

index = 0
for i, item in items_array_enum:
    relativeIndex = i - index * 47

    if i % 47 != 0:
        string_without_quotes = item.replace("'", "")
        if relativeIndex == 21:
            job_instance.publish_date = date.today()
            publishDate.append(date.today())

            job_instance.deadline = string_without_quotes
            deadline.append(string_without_quotes)

        if relativeIndex == 23:
            job_instance.grade = string_without_quotes
            grade.append(string_without_quotes)
            
        if relativeIndex == 25:
            trimmed_title = string_without_quotes[25:len(string_without_quotes)-1]
            job_instance.title = trimmed_title
            title.append(trimmed_title)

        if relativeIndex == 36:
            # Define the pattern to match the job number
            pattern = r"Job Number:\s*(\d+)"

            # Use regex to find the job number
            match = re.search(pattern, string_without_quotes)

            if match:
                job_instance.id = match.group(1)
            else:
                job_instance.id = "-1"
    else:
        index = index + 1

        # Append the instance into the list and Create a new instance of the Job class
        jobs.append(job_instance)
        job_instance = Job()

## UPDATE GITHUB WEBSITE ##

# Generate HTML table
table_html = generate_fancy_html_table( publishDate, title, grade, deadline )

# Encode the content to Base64
encoded_content = base64.b64encode(table_html.encode()).decode()


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
    'content': encoded_content,
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