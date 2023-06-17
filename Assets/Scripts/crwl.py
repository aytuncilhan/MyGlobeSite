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
from parseSoup import scrape_multiple_pages
from generateTable import generate_fancy_html_table
from updateRepo import writeContent


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

jobs = scrape_multiple_pages(soup)

publishDate = []
deadline = []
grade = []
title = []

# Create the arrays for the HTML table
for job in jobs:
    publishDate.append(job.publish_date)
    title.append(job.title)
    grade.append(job.grade)
    deadline.append(job.deadline)

# Create the HTML page
table_html = generate_fancy_html_table( publishDate, title, grade, deadline )

## UPDATE GITHUB WEBSITE ##

# Encode the content to Base64
encoded_html = base64.b64encode(table_html.encode()).decode()

writeContent(repo_owner, repo_name, access_token, branch_name, encoded_html, jobs)