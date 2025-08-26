import requests
import json

# The song and artist you want to get a playlist from
payload = {
    "song": "Blinding Lights",
    "artist": "The Weeknd"
}

# The URL of your running Flask server
url = "http://127.0.0.1:5000/recommend"

# Send the POST request to the backend
try:
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Check for errors
    
    # Print the JSON output from the backend
    data = response.json()
    print("Recommended Songs:")
    for song in data['recommended_songs']:
        print(f" - {song['song_name']} by {song['artist_name']}")
        
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")