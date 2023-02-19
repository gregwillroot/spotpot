SpotPot
=======


SpotPot is a Python script that uses the Spotify Web API to search for top tracks of a list of artists and store their details in a CSV file. It is designed to be run periodically to keep the CSV file up-to-date.

Getting Started
------------
1. Clone the repository or download the script directly from the repository.
2. Install the required packages using pip by running the command pip install -r requirements.txt.
3. Create a file named ids.csv in the same directory as the script. In this file, list the client ID and secret ID of the Spotify Web API. You can obtain them from the Spotify Developer Dashboard.
4. Create a file named artist.txt in the same directory as the script. In this file, list the names of the artists whose top tracks you want to search. Each artist should be on a separate line. For example:

       Pink Floyd
       U2
    
Usage
------------
Run the script from the command line using the command python spotpot.py. The SpotPot will search for the top track of each artist listed in artist.txt and store the details of the track in a file named results.csv. If results.csv does not exist, the script will create it.

If the script is run multiple times, it will only search for the top tracks of the artists that have not been searched before. It keeps track of the last artist found in results.csv and skips it and all the artists before it in the artist.txt file.

If it won't be able to find the artist, it will add it to a file named notfound.txt.

Authentication
------------
The script uses the Client Credentials Flow to authenticate with the Spotify Web API. It reads the client ID and secret ID from ids.csv

Output
------------

The results.csv file contains the following columns:

    Year
    Track ID
    Track Name
    Artist ID
    Artist Name
    Album ID
    Popularity

License
------------

This project is licensed under the MIT License.
