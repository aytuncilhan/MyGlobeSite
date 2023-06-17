import requests
from bs4 import BeautifulSoup
import base64
import os
from dotenv import load_dotenv
from parseSoup import scrapePage
from generateTable import generate_fancy_html_table
from updateRepo import writeContent, readContent


# Configure GitHub Repo Credentials
repo_owner = 'aytuncilhan'
repo_name = 'Personal-Website'
branch_name = 'main'
load_dotenv()
access_token = os.getenv("ACCESS_TOKEN")

# Retrieve already existing jobs
file_path = 'Assets/JobsLib/jobs.json'
exisitng_jobs = readContent(repo_owner, repo_name, access_token, file_path)

# Crawl the Job Website

url = 'https://nato.taleo.net/careersection/2/jobsearch.ftl?lang=en'
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

retrieved_jobs = scrapePage(soup)

# Create the arrays for the HTML table
publishDate = []
deadline = []
grade = []
title = []
for job in retrieved_jobs:
    publishDate.append(job.publish_date)
    title.append(job.title)
    grade.append(job.grade)
    deadline.append(job.deadline)

# Create the HTML page
table_html = generate_fancy_html_table( publishDate, title, grade, deadline )

# Encode the content to Base64
encoded_html = base64.b64encode(table_html.encode()).decode()

# Update Github repo
writeContent(repo_owner, repo_name, access_token, branch_name, encoded_html, retrieved_jobs)

## END OF CODE