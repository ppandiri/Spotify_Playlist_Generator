import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

def load_data():
    """
    Loads the Spotify song data from a local CSV file.
    """
    try:
        print("Loading data from local file: data.csv")
        df = pd.read_csv('data.csv')

        # Drop columns that are not needed for the recommendation algorithm
        df.drop(columns=[
            'id', 'name', 'album', 'album_id', 'artists', 'artist_ids',
            'track_number', 'disc_number', 'explicit', 'duration_ms',
            'time_signature', 'year', 'release_date'
        ], inplace=True, errors='ignore')
        return df
    except FileNotFoundError:
        print("Error: 'data.csv' file not found. Please ensure it is in the same directory.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def analyze_pca_features(df):
    """
    Performs PCA on the DataFrame and returns the top three features in each component.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the song data.
    """
    if df is None:
        print("Data not loaded. Cannot perform PCA.")
        return []

    # Drop columns that are not relevant for PCA analysis
    pca_df = df.copy()
    pca_df.drop(columns=['track_name', 'track_artist', 'track_album_name'], inplace=True, errors='ignore')

    # Initialize PCA and fit it to your data
    pca = PCA(n_components=3)
    pca.fit(pca_df)

    # Get the importance of each feature in the principal components
    feature_importance = np.abs(pca.components_)

    # Get the indices of the top three features in each component
    top_three_indices = [component.argsort()[-3:][::-1] for component in feature_importance]

    # Retrieve the names of the top three features in each component
    top_three_features = [[pca_df.columns[i] for i in indices] for indices in top_three_indices]

    print("Top three features in each PCA component:")
    for i, features in enumerate(top_three_features):
        print(f"Component {i+1}: {features}")

    # Add this new section to print the explained variance ratio
    print("\nExplained Variance Ratio:")
    for i, ratio in enumerate(pca.explained_variance_ratio_):
        print(f"Component {i+1}: {ratio:.4f}")
    
    # Return a single list of all top features
    all_top_features = [feature for component in top_three_features for feature in component]
    return all_top_features

def analyze_correlation_with_popularity(df):
    """
    Calculates and returns the top three features most correlated with popularity.

    Args:
        df (pd.DataFrame): The DataFrame containing the song data.
    """
    if df is None:
        print("Data not loaded. Cannot analyze correlation.")
        return []

    if 'popularity' not in df.columns:
        print("Warning: 'popularity' column not found in data. Skipping correlation analysis.")
        return []

    correlation_matrix = df.corr(numeric_only=True)
    correlation_with_popularity = correlation_matrix['popularity'].abs().sort_values(ascending=False)

    # Get the top three features, excluding 'popularity' itself
    top_three_features = correlation_with_popularity.index[1:4].tolist()
    print("Top three features most correlated with popularity:", top_three_features)
    return top_three_features

if __name__ == '__main__':
    # Load the data from the local CSV file
    df = load_data()

    if df is not None:
        print("--- Running Data Analysis ---")
        pca_features = analyze_pca_features(df)
        print("\n" + "="*30 + "\n")
        correlation_features = analyze_correlation_with_popularity(df)
        print(f"\nPCA Features: {pca_features}")
        print(f"Correlation Features: {correlation_features}")
    else:
        print("Data could not be loaded. Please check that 'data.csv' exists.")
