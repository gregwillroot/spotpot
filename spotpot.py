import requests
import json
from base64 import b64encode
import time
import csv
import os

songs = []
notfound = []
if not os.path.exists("results.csv"):
    with open("results.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Year", "Track ID", "Track Name","Artist ID", "Artist Name", "Album ID", "Popularity"])

# Spotify Web API endpoint for searching for tracks
endpoint = "https://api.spotify.com/v1/search"

# Client ID and secret for authentication
client_ids = []
client_secrets = []
with open("ids.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        client_ids.append(row["client_id"])
        client_secrets.append(row["client_secret"])

current_client = 0

# Authenticate and get access token
auth_headers = {"Authorization": f"Basic {b64encode(f'{client_ids[current_client]}:{client_secrets[current_client]}'.encode()).decode()}"}
auth_data = {"grant_type": "client_credentials"}
auth_response = requests.post("https://accounts.spotify.com/api/token", headers=auth_headers, data=auth_data)
if auth_response.status_code != 200:
    print("Authentication failed.")
    exit()
access_token = json.loads(auth_response.text)["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}

# Read artist names from file
last_found_artist = ''
with open("results.csv", "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) > 0 and row[0] == "Year":
            continue
        last_found_artist = row[4]
        
# Deduplicate artist names while preserving order
with open("artist.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    seen = set()
    deduped_lines = []
    for line in lines:
        line = line.strip()
        if line not in seen:
            seen.add(line)
            deduped_lines.append(line)
    with open("artist.txt", "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(deduped_lines))

with open("artist.txt", "r", encoding="utf-8") as file:
    artists = file.read().splitlines()

if last_found_artist != '':
    found = False
    for i, a in enumerate(artists):
        if a.lower() == last_found_artist.lower():
            artists = artists[i+1:]  # skip the found artist
            found = True
            break
    if not found:
        print(f"Artist '{last_found_artist}' not found in the list.")
else:
    found = True

if found:
    # Search for top track for each artist
    for artist in artists:
    # Search for artist ID
        query = f"artist:\"{artist}\""
        search_params = {"q": query, "type": "artist", "limit": 1, "offset": 0, "market": "PL"}
        try:
            response = requests.get(endpoint, headers=headers, params=search_params)
            if response.status_code == 429 or response.status_code == 401:
                print(f"Error {response.status_code}. Trying again.")
                current_client = (current_client + 1) % len(client_ids)
                auth_headers = {"Authorization": f"Basic {b64encode(f'{client_ids[current_client]}:{client_secrets[current_client]}'.encode()).decode()}"}
                auth_response = requests.post("https://accounts.spotify.com/api/token", headers=auth_headers, data=auth_data)
                if auth_response.status_code != 200:
                    print("Authentication failed.")
                    exit()
                access_token = json.loads(auth_response.text)["access_token"]
                headers = {"Authorization": f"Bearer {access_token}"}
                continue
            elif response.status_code != 200:
                print(f"Request failed for artist {artist}.")
                notfound.append(artist)
                with open("notfound.txt", "a", encoding="utf-8") as file:
                    file.write(artist + "\n")
                continue
            data = json.loads(response.text)
            artists = data["artists"]["items"]
            if len(artists) == 0:
                print(f"No artist found with name {artist}.")
                notfound.append(artist)
                with open("notfound.txt", "a", encoding="utf-8") as file:
                    file.write(artist + "\n")
                continue
            artist_name = artists[0]["name"]
            if artist_name.lower() != artist.lower():
                print(f"No artist found with name {artist}.")
                notfound.append(artist)
                with open("notfound.txt", "a", encoding="utf-8") as file:
                    file.write(artist + "\n")
                continue
                
                
            artist_id = artists[0]["id"]

            top_tracks_endpoint = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
            search_params = {"country": "PL","limit": 1, "offset": 0}
            response = requests.get(top_tracks_endpoint, headers=headers, params=search_params)
            if response.status_code == 429 or response.status_code == 401:
                print(f"Error {response.status_code}. Trying again.")
                current_client = (current_client + 1) % len(client_ids)
                auth_headers = {"Authorization": f"Basic {b64encode(f'{client_ids[current_client]}:{client_secrets[current_client]}'.encode()).decode()}"}
                auth_response = requests.post("https://accounts.spotify.com/api/token", headers=auth_headers, data=auth_data)
                if auth_response.status_code != 200:
                    print("Authentication failed.")
                    exit()
                access_token = json.loads(auth_response.text)["access_token"]
                headers = {"Authorization": f"Bearer {access_token}"}
                continue
            elif response.status_code != 200:
                print(f"Request failed for artist {artist}.")
                notfound.append(artist)
                with open("notfound.txt", "a", encoding="utf-8") as file:
                    file.write(artist + "\n")
                continue
            data = json.loads(response.text)
            top_tracks = data["tracks"]
            if len(top_tracks) == 0:
                print(f"No top track found for artist {artist_name}.")
                notfound.append(artist_name)
                with open("notfound.txt", "a", encoding="utf-8") as file:
                    file.write(artist_name + "\n")
                continue
            top_track = top_tracks[0]
            track_id = top_track["id"]
            track_name = top_track["name"]
            album_id = top_track["album"]["id"]
            artist_id = top_track["artists"][0]["id"]
            artist_name = top_track["artists"][0]["name"]
            popularity = top_track["popularity"]

            data = json.loads(response.text)
            tracks = data["tracks"]
            if len(tracks) == 0:
                print(f"No tracks found for artist {artist}.")
                notfound.append(artist)
                with open("notfound.txt", "a", encoding="utf-8") as file:
                    file.write(artist + "\n")
                continue

            track = tracks[0]
            if track["album"]["release_date"]:
                release_year = track["album"]["release_date"][:4]
            else:
                release_year = "N/A"
            track_id = "https://open.spotify.com/track/" + track["id"]
            track_name = track["name"]
            popularity = track["popularity"]
            song_data = {
                "Release Year": release_year,
                "Track ID": track_id,
                "Track Name": track_name,
                "Artist ID":artist_id,
                "Artist Name": artist,
                "Album ID":album_id,
                "Popularity": popularity
            }
            songs.append(song_data)
            values = list(song_data.values())
            print(f"Found song for artist {artist} - {song_data['Track Name']}, {song_data['Release Year']}")
            with open("results.csv", "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(song_data.values())
            time.sleep(0.0)
        except requests.exceptions.RequestException as e:
            print(f"Request failed for artist {artist}: {e}")
            notfound.append(artist)
            with open("notfound.txt", "a", encoding="utf-8") as file:
                file.write(artist + "\n")
