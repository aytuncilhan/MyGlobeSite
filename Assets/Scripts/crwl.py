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
# url = 'https://nato.taleo.net/careersection/2/jobsearch.ftl?lang=en'
# response = requests.get(url)
# html_content = response.text
# soup = BeautifulSoup(html_content, 'html.parser')

# retrieved_jobs = scrapePage(soup)

# with open('output.txt', 'w') as file:
#     file.write(soup.prettify())



from selenium import webdriver
from selenium.webdriver.support.ui import Select

# Create a WebDriver instance (assuming you have Chrome WebDriver installed)
driver = webdriver.Chrome()

# Load the page
driver.get('https://nato.taleo.net/careersection/2/jobsearch.ftl?lang=en')

# Find the <select> element by its ID
select_element = driver.find_element('css selector', '#requisitionListInterface\\.dropListSize')

# Select the option with value="100"
select = Select(select_element)
select.select_by_value('100')

# Fetch the updated page source
updated_html = driver.page_source

with open('output_updated.txt', 'w') as file:
    file.write(updated_html)


# Create a BeautifulSoup object from the updated HTML
soup2 = BeautifulSoup(updated_html, 'html.parser')

with open('output_updated_soup.txt', 'w') as file:
    file.write(soup2.prettify())

retrieved_jobs = scrapePage(soup2)

# Close the browser
driver.quit()


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

# Update Github repo with the ads.html and jobs.json
writeContent(repo_owner, repo_name, access_token, branch_name, encoded_html, retrieved_jobs)

## END OF CODE