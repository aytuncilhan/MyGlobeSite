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
import parseSoup

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