import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv() 

# Get API keys from environment variables
SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")

# Check if the keys were loaded successfully
if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    print("Error: SPOTIPY_CLIENT_ID or SPOTIPY_CLIENT_SECRET is missing. Please check your .env file.")
    exit()

print("--- Testing get_track_features() ---")
print(f"Using Client ID: {SPOTIPY_CLIENT_ID}")
print(f"Using Client Secret: {SPOTIPY_CLIENT_SECRET}")

RECOMMENDATION_FEATURES = ['key', 'valence', 'energy', 'speechiness', 'danceability', 'acousticness', 'instrumentalness', 'liveness']

def get_track_features_isolated(track_id):
    """Fetches and filters song features from Spotify."""
    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        audio_features = sp.audio_features(track_id)
        if not audio_features or not audio_features[0]:
            return None
        
        track_features = audio_features[0]
        features_dict = {feature: track_features.get(feature, 0) for feature in RECOMMENDATION_FEATURES}
        return features_dict
    except Exception as e:
        print(f"Error getting features: {e}")
        return None

# A well-known song to test with
track_id_test = "0VjIjW4GlUZAMYd2vXMi3b"
features = get_track_features_isolated(track_id_test)

if features:
    print("\nSuccessfully retrieved features for 'Blinding Lights':")
    print(features)
else:
    print("\nFailed to retrieve features. The API keys may be invalid.")
