from datetime import date
import re
from job import Job
from datetime import date

def scrape_multiple_pages(soup):
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

    # Create an instance of the Job class
    job_instance = Job()

    index = 0
    for i, item in items_array_enum:
        relativeIndex = i - index * 47

        if i % 47 != 0:
            string_without_quotes = item.replace("'", "")
            if relativeIndex == 21:
                job_instance.publish_date = date.today()

                job_instance.deadline = string_without_quotes

            if relativeIndex == 23:
                job_instance.grade = string_without_quotes
                
            if relativeIndex == 25:
                trimmed_title = string_without_quotes[25:len(string_without_quotes)-1]
                job_instance.title = trimmed_title

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

    return jobs