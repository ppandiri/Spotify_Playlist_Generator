import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load environment variables
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
print("ID:", repr(SPOTIPY_CLIENT_ID))
print("Secret:", repr(SPOTIPY_CLIENT_SECRET))
if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    raise ValueError("Missing SPOTIPY_CLIENT_ID or SPOTIPY_CLIENT_SECRET in .env file")

# Authenticate
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET
    )
)

# Correct Spotify track ID for Blinding Lights
track_id = "0VjIjW4GlUZAMYd2vXMi3b"

# Fetch and print audio features
features = sp.audio_features([track_id])
print(features)