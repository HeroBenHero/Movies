import requests
from bs4 import BeautifulSoup

# URL to extract text from
url = "https://www.1tamilmv.prof/"

# Send a GET request to the URL
response = requests.get(url)

# Get the content of the response
page_content = response.content

# Create a BeautifulSoup object and specify the parser
soup = BeautifulSoup(page_content, 'html.parser')

# Find the HTML element with the specified id
main_area = soup.find(id='ipsLayout_mainArea')

text = main_area.get_text()

# Initialize the HTML content
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Movies Index</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f2f2f2;
            text-align: center;
        }
        h1 {
            color: #333;
        }
        ul {
            list-style-type: none; /* Remove list-style-type */
            padding-left: 0; /* Remove left padding for the list */
        }
        li {
            margin-bottom: 10px;
            background-color: #fff;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease-in-out;
        }
        li:hover {
            background-color: #f7f7f7;
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
            flex-wrap: wrap; /* Allow buttons to wrap to the next line on smaller screens */
        }
        .button-container button {
            background-color: #007bff;
            color: #fff;
            border: none;
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease-in-out;
        }
        .button-container button:hover {
            background-color: #0056b3;
        }

        /* Style for smaller screens (max-width: 600px) */
        @media (max-width: 600px) {
            .button-container {
                flex-direction: column; /* Stack buttons vertically */
                align-items: center; /* Center-align buttons */
            }
            .button-container button {
                margin: 5px 0; /* Add margin to separate buttons */
                width: 100%; /* Make buttons full width */
            }

            /* Two columns for buttons on smaller screens */
            .button-container.two-columns {
                flex-direction: row;
                flex-wrap: wrap;
                justify-content: space-between;
            }
            .button-container.two-columns button {
                width: 48%; /* Adjust button width for two columns */
                margin: 5px 0;
            }
        }
    </style>
    <script>
        // JavaScript for interactivity
        function showLanguage(language) {
            const listItems = document.querySelectorAll("li");

            listItems.forEach(function (item) {
                if (item.classList.contains(language) || language === "all") {
                    item.style.display = "block";
                } else {
                    item.style.display = "none";
                }
            });
        }

        function showCategory(category) {
            const listItems = document.querySelectorAll("li");

            listItems.forEach(function (item) {
                if (item.classList.contains(category) || category === "all") {
                    item.style.display = "block";
                } else {
                    item.style.display = "none";
                }
            });
        }
    </script>
</head>
<body>
    <h1>Movies Index</h1>
    <div class="button-container two-columns"> <!-- Add class for two columns on smaller screens -->
        <button onclick="showLanguage('all')">All</button>
        <button onclick="showLanguage('tam')">Tamil</button>
        <button onclick="showLanguage('eng')">English</button>
        <button onclick="showLanguage('hin')">Hindi</button>
        <button onclick="showLanguage('tel')">Telugu</button>
        <button onclick="showLanguage('kan')">Kannada</button>
        <button onclick="showLanguage('mal')">Malayalam</button>
        <button onclick="showCategory('predvd')">PreDVD</button>
        <button onclick="showCategory('hq')">HQ</button>
        <button onclick="showCategory('hd')">HD</button>
        <button onclick="showCategory('uhd')">UHD</button>
        <button onclick="showCategory('esub')">ESub</button>
        <button onclick="showCategory('hdts')">HDTS</button>
        <button onclick="showCategory('bluray')">BluRay</button>
    </div>
    <ul>
"""
lines = text.strip().split("\n")

# Loop through each line and add it to the HTML content with appropriate language and category classes
for line in lines:
    language_class = None
    if 'tam' in line.lower():
        language_class = 'tam'
    elif 'eng' in line.lower():
        language_class = 'eng'
    elif 'hin' in line.lower():
        language_class = 'hin'
    elif 'tel' in line.lower():
        language_class = 'tel'
    elif 'kan' in line.lower():
        language_class = 'kan'
    elif 'mal' in line.lower():
        language_class = 'mal'
    else:
        language_class = 'other'

    category_class = None
    if 'predvd' in line.lower():
        category_class = 'predvd'
    elif 'hq' in line.lower():
        category_class = 'hq'
    elif 'hdts' in line.lower():
        category_class = 'hdts'
    elif 'uhd' in line.lower():
        category_class = 'uhd'
    elif 'hd' in line.lower():
        category_class = 'hd'
    elif 'esub' in line.lower():
        category_class = 'esub'
    elif 'bluray' in line.lower():
        category_class = 'bluray'

    formatted_line = line.strip().replace('[WATCH]', '').replace('[W]', '').replace('-', '')
    if not formatted_line or "Official Telegram Channel" in formatted_line:
        continue
        
    html_content += f"<li class='{language_class} {category_class}'>{formatted_line}</li>"

# Close the HTML structure
html_content += """
    </ul>
</body>
</html>
"""

# Save the HTML content to a file
with open("1tamilmvlist.html", "w", encoding="utf-8") as html_file:
    html_file.write(html_content)

print("HTML file 'index.html' has been created.")
