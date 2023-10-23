from bs4 import BeautifulSoup
import requests

def extract_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div with id 'archive'
    div = soup.find('div', {'id': 'archive'})

    # Extract all links
    links = list(dict.fromkeys(a['href'] for a in div.find_all('a', href=True)))

    # Extract all text
    text_list = [line.strip() for line in div.get_text().splitlines() if line.strip()]

    # Extract all image sources
    images = [img['src'] for img in div.find_all('img', src=True)]

    return list(zip(text_list, links, images))

# List of URLs
urls = [
    'https://tamilyogi.plus/category/tamilyogi-bluray-movies/',    
    'https://tamilyogi.plus/category/tamilyogi-dubbed-movies-online/',
    'https://tamilyogi.plus/category/tamil-web-series/',
    'https://tamilyogi.plus/category/tamilyogi-full-movie-online/'
]

# Create an HTML file
with open('tamilyogilist.html', 'w') as html_file:
    html_file.write('<html>')
    html_file.write('<head>')
    html_file.write('<style>')
    html_file.write('''
        body {
            background-color: #f2f2f2;
            font-family: Arial, sans-serif;
        }
        .category {
            padding: 10px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1);
            margin: 20px auto;
            text-align: center;
        }
        .category img, .category a {
            display: none;
            margin-top: 10px;
        }
        .category.open img, .category.open a {
            display: block;
        }
        .category h3 {
            margin: 0;
            padding: 10px;
            cursor: pointer;
            background-color: #007BFF;
            color: #fff;
            border-radius: 5px 5px 0 0;
        }
        .category p {
            padding: 10px;
            cursor: pointer;
        }
        #category-buttons {
            text-align: center;
            padding: 10px;
        }
        .category-button {
            padding: 10px 20px;
            margin: 5px;
            cursor: pointer;
            background-color: #007BFF;
            color: #fff;
            border: none;
        }
    ''')
    html_file.write('</style>')
    html_file.write('</head>')
    html_file.write('<body>')

    # Generate category buttons at the top
    html_file.write('<div id="category-buttons">')
    html_file.write(f'<span class="category-button" onclick="showAllCategories()">Show All</span>')
    for index, url in enumerate(urls):
        category_name = url.split("/")[-2].replace('-', ' ').title()
        html_file.write(f'<span class="category-button" onclick="showCategory({index})">{category_name}</span>')
    html_file.write('</div>')

    # Generate content for each category
    for index, url in enumerate(urls):
        category_data = extract_info(url)
        category_name = url.split("/")[-2].replace('-', ' ').title()
        html_file.write(f'<div class="category" id="category-{index}">')
        html_file.write(f'<h3 onclick="toggleCategory({index})">{category_name}</h3>')
        for text, link, image in category_data:
            html_file.write(f'<p onclick="toggleDetails(this)">{text}</p>')
            html_file.write(f'<a href="{link}" class="link">{link}</a>')
            # html_file.write(f'<img src="{image}" alt="{text}" class="image">')
        html_file.write('</div>')

    # JavaScript to show/hide categories and details
    html_file.write('<script>')
    html_file.write('''
        function showAllCategories() {
            var categories = document.querySelectorAll('.category');
            for (var i = 0; i < categories.length; i++) {
                categories[i].style.display = 'block';
            }
        }

        function showCategory(index) {
            var categories = document.querySelectorAll('.category');
            for (var i = 0; i < categories.length; i++) {
                categories[i].style.display = 'none';
            }
            categories[index].style.display = 'block';
        }
        
        function toggleCategory(index) {
            var categories = document.querySelectorAll('.category');
            for (var i = 0; i < categories.length; i++) {
                categories[i].classList.remove('open');
            }
            categories[index].classList.add('open');
        }
        
        function toggleDetails(textElement) {
            var details = textElement.nextElementSibling;
            details.style.display = (details.style.display === 'none' || details.style.display === '') ? 'block' : 'none';
        }
    ''')
    html_file.write('</script>')

    html_file.write('</body>')
    html_file.write('</html>')
