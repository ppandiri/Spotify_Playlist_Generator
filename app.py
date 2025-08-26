import os
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from scipy.spatial.distance import euclidean
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from analysis import load_data, analyze_pca_features, analyze_correlation_with_popularity

# --- API Key Management (BEST PRACTICE) ---
# Load environment variables from a .env file.
# The .env file should be in the same directory as this script.
load_dotenv() 

# It's crucial to never hard-code API keys. Use environment variables instead.
# The 'get' method with a default value prevents errors if the variable is not set.
SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID", "YOUR_CLIENT_ID_HERE")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET", "YOUR_CLIENT_SECRET_HERE")

# --- Global Initialization ---
app = Flask(__name__)
sp = None
df = None
# The feature list for the recommender system is now static and reliable.
# This list is based on features available in both the local dataset and the Spotify API.
RECOMMENDATION_FEATURES = ['key', 'valence', 'energy', 'speechiness', 'danceability', 'acousticness', 'instrumentalness', 'liveness']


def get_spotify_client():
    """Initializes and returns the Spotipy client."""
    global sp
    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except Exception as e:
        print(f"Error initializing Spotipy: {e}")
        sp = None # Ensure sp is None on failure

def load_data_and_set_global_df():
    """
    Loads data and sets the global DataFrame.
    """
    global df
    df = load_data()
    if df is not None:
        # After loading, check if the DataFrame contains all required features
        missing_cols = [col for col in RECOMMENDATION_FEATURES if col not in df.columns]
        if missing_cols:
            print(f"Error: The dataset is missing the following required columns: {missing_cols}")
            df = None


def get_track_features(track_id):
    """
    Fetches specific audio features for a given track ID using the Spotify API.
    Returns a pandas Series of the selected features.
    """
    if sp is None or track_id is None:
        return None

    try:
        # Get all audio features from the API
        audio_features = sp.audio_features(track_id)
        if not audio_features or not audio_features[0]:
            return None

        track_features = audio_features[0]

        # Filter the features based on our static list for consistency
        # Use .get() with a default value to prevent KeyError if a feature is missing
        features_dict = {feature: track_features.get(feature, 0) for feature in RECOMMENDATION_FEATURES}
        features_series = pd.Series(features_dict)
        return features_series
    except Exception as e:
        print(f"Error fetching features for track ID {track_id}: {e}")
        return None

def find_similar_songs(chosen_song_features, num_recommendations=20):
    """
    Finds songs in the dataset most similar to the chosen song
    using Euclidean distance.
    """
    global df
    if df is None or chosen_song_features is None:
        return []
    
    # Use the static list of features for consistency
    feature_cols = RECOMMENDATION_FEATURES

    # Ensure the chosen song features has all required columns before proceeding
    if not all(col in chosen_song_features.index for col in feature_cols):
        print("Error: The chosen song's features do not match the required recommendation features.")
        return []

    # Handle the case where the feature series might have a different index order
    chosen_song_values = chosen_song_features[feature_cols].values

    # Calculate Euclidean distances
    distances = np.apply_along_axis(
        lambda x: euclidean(chosen_song_values, x),
        1,
        df[feature_cols].values
    )

    # Find indices of the closest songs
    closest_songs_indices = np.argsort(distances)

    recommended_songs = []
    # Iterate through the sorted indices to find unique songs
    for index in closest_songs_indices:
        song_name = df.iloc[index]['track_name']
        artist_name = df.iloc[index]['track_artist']

        # Prevent the same song and duplicates from being in the playlist
        if song_name != chosen_song_features.name and (song_name, artist_name) not in recommended_songs:
            recommended_songs.append({'song_name': song_name, 'artist_name': artist_name})
            if len(recommended_songs) >= num_recommendations:
                break
    return recommended_songs

# --- Flask Backend Endpoints ---
@app.route('/recommend', methods=['POST'])
def recommend():
    """
    API endpoint to generate a playlist from a user-provided song and artist.
    Expects a JSON body with 'song' and 'artist' keys.
    """
    if df is None or sp is None:
        return jsonify({"error": "Backend not initialized. Data or Spotify client is missing."}), 500

    data = request.get_json()
    user_song = data.get('song')
    user_artist = data.get('artist')

    if not user_song or not user_artist:
        return jsonify({"error": "Please provide both 'song' and 'artist'."}), 400

    try:
        # Search for the track on Spotify
        query = f"track:{user_song} artist:{user_artist}"
        results = sp.search(q=query, type='track', limit=1)

        if not results['tracks']['items']:
            return jsonify({"error": f"Could not find '{user_song}' by '{user_artist}' on Spotify."}), 404

        track_id = results['tracks']['items'][0]['id']
        song_features = get_track_features(track_id)

        if song_features is None:
            return jsonify({"error": "Could not retrieve audio features for the song."}), 500

        # Find similar songs and return the list
        recommended_songs = find_similar_songs(song_features)
        return jsonify({"recommended_songs": recommended_songs}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    """A simple home endpoint for testing."""
    return "Spotify Playlist Generator Backend is running!"

# --- Main Execution Block ---
if __name__ == '__main__':
    get_spotify_client()
    load_data_and_set_global_df()

    if df is not None:
        # Run the analysis from the separate file if data is loaded
        print("--- Running Data Analysis ---")
        analyze_pca_features(df)
        print("\n" + "="*30 + "\n")
        analyze_correlation_with_popularity(df)
        print("\n" + "="*30 + "\n")
        print("--- Starting Backend Server ---")
        app.run(debug=True, port=5000)
    else:
        print("Application cannot start. Please ensure the dataset is available.")
