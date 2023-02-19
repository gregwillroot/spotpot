# spotpot
This is a Python script that uses the Spotify Web API to search for and retrieve the top tracks of a list of artists. It stores the results in a CSV file and logs any artists that were not found in a separate text file.
# Prerequisites
    • Python 3.x
    • requests library
    • Spotify developer account with a client ID and secret
# Getting Started
    1. Clone the repository or download the code.
    2. Install the requests library by running pip install requests.
    3. Create a Spotify developer account if you don't already have one.
    4. Create a new app in your Spotify dashboard and note down the client ID and secret.
    5. Save the client ID and secret in a CSV file named ids.csv with headers client_id and client_secret, respectively.
    6. Create a text file named artist.txt and list the names of the artists you want to search for, each on a separate line.
    7. Run the script.
# Notes
    • The script uses the search endpoint of the Spotify Web API to search for the artist and the top-tracks endpoint to retrieve the top track.
    • The script uses client credentials flow for authentication.
    • The script will log any artists that were not found in a separate text file named notfound.txt.
    • The script will continue from where it left off if it is interrupted, by checking the last artist found in the CSV file.
