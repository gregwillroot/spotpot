SpotPot
=======


SpotPot searches for the top track for each artist in a list, using the Spotify Web API. 
The script saves the results to a CSV file and logs any errors to a text file.

Installation
------------
To use this script, you will need to have Python 3 installed. You can download it from the official website: https://python.org 

You will also need to install 'requests' package.
You can install the package by running the following command:

     pip install requests
    
Usage
------------
    1. Clone the repository to your local machine or download the code.
    2. Add your Spotify API client ID and secret to ids.csv. You can get your client ID and secret by creating a Spotify Developer account and creating a new app.
    3. Add the artist names you want to search for in artists.txt. Each name should be on a separate line.
    4. Run the script.

Notes
------------
The script searches for the top track of each artist in a list, displays the real-time results, saves them to 'results.csv', logs any unfound tracks to 'notfound.txt', and can be resumed where left off, skipping already searched artists and continuing with the next artist in the list.
