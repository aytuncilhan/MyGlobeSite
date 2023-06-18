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
            .last-update {
                position: absolute;
                top: 10px;
                right: 10px;
                font-size: 12px;
                font-family: "Trebuchet MS", Arial, sans-serif;
                color: #777777;
            }
            .filter-label {
                margin-right: 5px;
            }
            .filter-select {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        </style>
        <script>
            function filterTable(columnIndex) {
                var input, filter, table, tr, td, i;
                input = document.getElementById("filter-" + columnIndex);
                filter = input.value.toUpperCase();
                table = document.getElementById("job-table");
                tr = table.getElementsByTagName("tr");

                for (i = 1; i < tr.length; i++) {
                    td = tr[i].getElementsByTagName("td")[columnIndex];
                    if (td) {
                        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                            tr[i].style.display = "";
                        } else {
                            tr[i].style.display = "none";
                        }
                    }
                }
            }
        </script>
    </head>
    <body>
        <div id="filters">
            <label class="filter-label" for="filter-0">Publish Date:</label>
            <select class="filter-select" id="filter-0" onchange="filterTable(0)">
                <option value="">All</option>
    '''
    unique_dates = set(array1)
    for date in unique_dates:
        html += f'<option value="{date}">{date}</option>'

    html += '''
            </select>

            <label class="filter-label" for="filter-1">Title:</label>
            <select class="filter-select" id="filter-1" onchange="filterTable(1)">
                <option value="">All</option>
    '''
    unique_titles = set(array2)
    for title in unique_titles:
        html += f'<option value="{title}">{title}</option>'

    html += '''
            </select>

            <label class="filter-label" for="filter-2">Grade:</label>
            <select class="filter-select" id="filter-2" onchange="filterTable(2)">
                <option value="">All</option>
    '''
    unique_grades = set(array3)
    for grade in unique_grades:
        html += f'<option value="{grade}">{grade}</option>'

    html += '''
            </select>

            <label class="filter-label" for="filter-3">Deadline:</label>
            <select class="filter-select" id="filter-3" onchange="filterTable(3)">
                <option value="">All</option>
    '''
    unique_deadlines = set(array4)
    for deadline in unique_deadlines:
        html += f'<option value="{deadline}">{deadline}</option>'

    html += '''
            </select>
        </div>

        <table id="job-table">
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

    def calculate_color(days_left):
        if days_left <= 1:
            alpha = 1.0
        elif days_left >= 5:
            return 'rgb(255, 255, 255)'  # White color for more than 14 days
        else:
            alpha = 1.0 - ((days_left - 1) / 4)

        return f'rgba(255, 153, 153, {alpha})'

    for row1, row2, row3, row4 in zip(array1, array2, array3, array4):
        deadline = datetime.strptime(row4, '%d-%b-%Y, %I:%M:%S %p').date()
        days_left = (deadline - today).days

        row_color = calculate_color(days_left)

        html += f'''
                <tr style="background-color: {row_color}">
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
