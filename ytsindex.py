#@markdown **YTS List Movies HTML**
import requests
from datetime import datetime

# Get the current year
current_year = datetime.now().year

# Define the API endpoint
endpoint = "https://yts.mx/api/v2/list_movies.json"

# Define parameters
params = {
    "sort_by": "year",
    "order_by": "desc",
    "limit": 50,  # You can adjust the limit as needed
    "year": current_year  # Filter by the current year
}


page = 1  # Initialize the page number

# Create an HTML string to store the movie list
html_output = f"""<!DOCTYPE html>
<html>
<head>
    <title>Movies Released in {current_year}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 20px;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            color: #333;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
        }}
        li {{
            width: 48%; /* Set the width for two columns */
            background-color: #fff;
            margin-bottom: 20px;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
            cursor: pointer;
        }}
        li:hover {{
            background-color: #f2f2f2;
        }}
        .hidden {{
            display: none;
        }}
        .cover-image {{
            max-width: 100%;
        }}
    </style>
</head>
<body>
    <h1>Movies Released in {current_year}</h1>
    <ul>
    """

while True:
  try:
        # Set the page parameter for the current page
        params["page"] = page

        # Send a GET request to the API
        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Check if the response contains movie data
            if data.get("status") == "ok" and "movies" in data.get("data"):
                movies = data["data"]["movies"]

                for movie in movies:
                    if int(movie['year']) < int(current_year):
                        raise Exception("Year of the movie is not current year")

                    # Extract relevant movie details
                    movie_title = movie['title']
                    movie_language = movie['language']
                    small_cover_image = movie['small_cover_image']
                    movie_description = movie.get('description_full', 'N/A')

                    # Create a string with all torrent details
                    torrent_details = ""
                    for torrent in movie['torrents']:
                        torrent_url = torrent['url']
                        quality = torrent['quality']
                        size = torrent['size']
                        seeds = torrent['seeds']
                        peers = torrent['peers']
                        torrent_details += f"<a href='{torrent_url}'>Download Torrent</a>\tQuality: {quality}\tSize: {size}\tSeeds: {seeds}\tPeers: {peers}<br>"

                    html_output += f"""
                    <li onclick="toggleInfo(this)">
                        <div class="movie-title">{movie_title}</div>
                        <div class="movie-info hidden">
                            <p>Year: {movie['year']}</p>
                            <p>Language: {movie_language}</p>
                            <p>Description: {movie_description}</p>
                            <img src="{small_cover_image}" alt="Cover Image" class="cover-image">
                            <p>Torrent Details:<br>{torrent_details}</p>
                        </div>
                    </li>
                    """

                # Check if there are more pages to fetch
                if data["data"]["movie_count"] <= page * params["limit"]:
                    break
                else:
                    page += 1
            else:
                html_output += f"<p>No movie data found for {current_year}.</p>"
                break
        else:
            html_output += f"<p>Error: {response.status_code} - {response.text}</p>"
            break


  except Exception as e:
    if str(e)=="Year of the movie is not current year":
      break
    else:
      print(f"An error occurred: {e}")

# Close the HTML document
html_output += """
    </ul>
    <script>
        function toggleInfo(element) {
            const info = element.querySelector(".movie-info");
            info.classList.toggle("hidden");
        }
    </script>
</body>
</html>
    """

# Save the HTML to a file or display it as needed
with open("ytslist.html", "w", encoding="utf-8") as html_file:
    html_file.write(html_output)
print("HTML file 'movies.html' created successfully.")


