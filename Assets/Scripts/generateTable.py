from datetime import datetime, timedelta

def generate_fancy_html_table(array1, array2, array3, array4):
    html = '''
    <html>
    <head>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
                font-family: Arial, sans-serif;
            }
            th, td {
                text-align: left;
                padding: 8px;
            }
            th {
                background-color: #f2f2f2;
            }
            /* tr:nth-child(even) {
                background-color: #dddddd;
            } */
            .last-update {
                position: absolute;
                top: 10px;
                right: 10px;
                font-size: 12px;
                font-family: "Trebuchet MS", Arial, sans-serif;
                color: #777777;
            }
            .red-row {
                background-color: #ffcccc;
            }
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

    today = datetime.now().date()

    for row1, row2, row3, row4 in zip(array1, array2, array3, array4):
        deadline = datetime.strptime(row4, '%d-%b-%Y, %I:%M:%S %p').date()
        row_class = 'red-row' if (deadline - today) < timedelta(days=7) else ''

        html += f'''
                <tr class="{row_class}">
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
