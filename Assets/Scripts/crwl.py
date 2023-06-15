import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import base64
from datetime import date
import os

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

publishDate = []
submitDate = []
grade = []
title = []

index = 0
for i, item in items_array_enum:
    relativeIndex = i - index * 47

    if i % 47 != 0:
        string_without_quotes = item.replace("'", "")
        if relativeIndex == 21:
            submitDate.append(string_without_quotes)
            publishDate.append(date.today())
        if relativeIndex == 23:
            grade.append(string_without_quotes)
        if relativeIndex == 25:
            title.append(string_without_quotes[25:len(string_without_quotes)-1])
    else:
        index = index + 1

# table = list(zip(title, grade, submitDate))

# # Print the table with headers
# headers = ['Title', 'Grade', 'Submit Date']
# tbl = tabulate(table, headers=headers)

## UPDATE GITHUB WEBSITE ##

# GitHub repository details
repo_owner = 'aytuncilhan'
repo_name = 'Personal-Website'
file_path = 'ads.html'
branch_name = 'main'
access_token = os.getenv("ACCESS_TOKEN")

# Generate HTML table
table_html = generate_fancy_html_table( publishDate, title, grade, submitDate )

# Encode the content to Base64
encoded_content = base64.b64encode(table_html.encode()).decode()

# Construct the API endpoint
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
