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
from updateRepo import writeContent, readContent


# Configure GitHub Repo Credentials
repo_owner = 'aytuncilhan'
repo_name = 'Personal-Website'
branch_name = 'main'
load_dotenv()
access_token = os.getenv("ACCESS_TOKEN")

# Retrieve already existing jobs
file_path = 'Assets/JobsLib/jobs.json'
exisitng_jobs = readContent(repo_owner, repo_name, access_token, branch_name, file_path)

# Crawl the Job Website

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

## END OF CODE