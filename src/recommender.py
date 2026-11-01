from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

import csv
from typing import List, Dict, Tuple

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Dict]):
        """Store the song catalog used for recommendations."""
        self.songs = songs

    def recommend(self, user: Dict, k: int = 5) -> List[Dict]:
        """Return the top-k song dicts that best match the user's preferences."""
        recommendations = recommend_songs(user, self.songs, k)
        return [rec[0] for rec in recommendations]  # Extract only the song dictionaries

    def explain_recommendation(self, user: Dict, song: Dict) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        _, reasons = score_song(user, song)
        return f"Recommended because: {', '.join(reasons)}"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file, converting numeric fields to floats."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert numerical fields to float
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    # +2.0 points for genre match
    if song['genre'] == user_prefs['preferred_genre']:
        score += 2.0
        reasons.append("Genre match")

    # +1.0 point for mood match
    if song['mood'] == user_prefs['preferred_mood']:
        score += 1.0
        reasons.append("Mood match")

    # Energy similarity
    energy_similarity = 1.0 - abs(song['energy'] - user_prefs['target_energy'])
    score += 1.5 * energy_similarity
    reasons.append(f"Energy similarity: {energy_similarity:.2f}")

    # Tempo similarity
    max_tempo = 200  # Assuming a max tempo for normalization
    tempo_similarity = 1.0 - abs(song['tempo_bpm'] - user_prefs['target_tempo']) / max_tempo
    score += 1.0 * tempo_similarity
    reasons.append(f"Tempo similarity: {tempo_similarity:.2f}")

    # Valence similarity
    valence_similarity = 1.0 - abs(song['valence'] - user_prefs['target_valence'])
    score += 1.0 * valence_similarity
    reasons.append(f"Valence similarity: {valence_similarity:.2f}")

    return score, reasons

import heapq
from typing import List, Dict, Tuple

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top-k (song, score, explanation) tuples ranked by score."""
    # Calculate scores and explanations for all songs
    scored_songs = [
        (song, *score_song(user_prefs, song))  # Unpack score and reasons
        for song in songs
    ]

    # Use heapq.nlargest to get the top-k songs by score
    top_k_songs = heapq.nlargest(k, scored_songs, key=lambda x: x[1])

    # Return the top-k songs with their scores and explanations
    return [(song, score, f"Score: {score:.2f}. Reasons: {', '.join(reasons)}") for song, score, reasons in top_k_songs]