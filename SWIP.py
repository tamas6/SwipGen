import urllib.request
import re

# Generate the SWIP URLs from the user input
def generate_swip_urls(swipe_numbers):
    base_url = "https://raw.githubusercontent.com/ethersphere/SWIPs/refs/heads/master/SWIPs/swip-{}.md"
    return [base_url.format(number) for number in swipe_numbers]

# Fetch and process SWIP data
def fetch_swip_data(urls):
    swip_data = []
    for url in urls:
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read().decode('utf-8')
                # Only consider the first 10 lines
                content = "\n".join(content.splitlines()[:10])
                # Extract fields using regex
                fields = re.findall(r'(\w+): (.+)', content)
                swip_entry = {key.lower(): value for key, value in fields}
                swip_data.append((url, swip_entry))
        except Exception as e:
            print(f"Failed to fetch data from the following URL: {url}. Error: {e}")
    return swip_data

# Modify URL from raw to GitHub blob
def modify_url(url):
    return url.replace("raw.githubusercontent.com", "github.com").replace("/refs/heads/master", "/blob/master")

# Generate HTML from SWIP data
def generate_html(swip_data, output_file="swip_table.html"):
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SWIP Table</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }
        .container {
            width: 90%;
            max-width: 1000px;
            margin: 20px auto;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }
        header {
            background-color: #333;
            color: #ffcc00;
            padding: 20px;
            font-size: 24px;
            font-weight: bold;
            text-transform: uppercase;
        }
        .intro {
            padding: 10px;
            font-size: 16px;
            color: #666;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #555;
            color: #ffcc00;
            cursor: pointer;
            font-weight: bold;
            text-transform: uppercase;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #e2e2e2;
        }
        .footer {
            padding: 10px;
            font-size: 12px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>Swarm Improvement Proposals</header>
        <div class="intro">
            Swarm Improvement Proposals (SWIPs) describe standards for the Swarm platform, including core protocol specifications, client APIs, and standards for contracts, interfaces, and utilities.<br><br>
            A browsable version of all current and draft SWIPs can be found on <a href="https://github.com/ethersphere/SWIPs">GitHub</a>.
        </div>
        <table id="swipTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">SWIP</th>
                    <th onclick="sortTable(1)">Title</th>
                    <th onclick="sortTable(2)">Status</th>
                    <th onclick="sortTable(3)">Type</th>
                    <th onclick="sortTable(4)">Author</th>
                    <th onclick="sortTable(5)">Created</th>
                    <th onclick="sortTable(6)">Updated</th>
                </tr>
            </thead>
            <tbody>
    """

    for url, swip in swip_data:
        swip_number = swip.get("swip", "")
        # Modify the URL for the SWIP number to make it a link
        swip_link = modify_url(url)
        html_content += f"""
                <tr>
                    <td><a href="{swip_link}" target="_blank">{swip_number}</a></td>
                    <td>{swip.get("title", "")}</td>
                    <td>{swip.get("status", "")}</td>
                    <td>{swip.get("type", "")}</td>
                    <td>{swip.get("author", "")}</td>
                    <td>{swip.get("created", "")}</td>
                    <td>{swip.get("updated", "")}</td>
                </tr>
        """

    # JavaScript for sorting the table
    html_content += """
            </tbody>
        </table>
        <div class="footer">Sortable columns</div>
    </div>
    <script>
        function sortTable(n) {
            var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
            table = document.getElementById("swipTable");
            switching = true;
            dir = "asc"; 
            while (switching) {
                switching = false;
                rows = table.rows;
                for (i = 1; i < (rows.length - 1); i++) {
                    shouldSwitch = false;
                    x = rows[i].getElementsByTagName("TD")[n];
                    y = rows[i + 1].getElementsByTagName("TD")[n];
                    if (dir == "asc") {
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir == "desc") {
                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                }
                if (shouldSwitch) {
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    switching = true;
                    switchcount++;
                } else {
                    if (switchcount == 0 && dir == "asc") {
                        dir = "desc";
                        switching = true;
                    }
                }
            }
        }
    </script>
</body>
</html>
"""

    # Saving the HTML file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"Successful html: '{output_file}'")

# Main function to start the script
if __name__ == "__main__":
    # Asking for SWIP numbers
    input_numbers = input("Please specify the numbers of the SWIPs to make a list of (e.g., 20,21,11,10,9,333): ")
    swipe_numbers = input_numbers.split(",")
    
    # Generate URLs for SWIPs
    urls = generate_swip_urls(swipe_numbers)
    
    # Fetch SWIP data and generate HTML
    swip_data = fetch_swip_data(urls)
    generate_html(swip_data)
