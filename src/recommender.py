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
from dataclasses import asdict
from typing import List, Dict, Tuple, Union

def _song_to_dict(song: Union[Song, Dict]) -> Dict:
    """Convert a Song dataclass to a dict so score_song can use it."""
    return asdict(song) if isinstance(song, Song) else song

def _user_to_prefs(user: Union[UserProfile, Dict]) -> Dict:
    """Convert a UserProfile dataclass to the prefs dict format used by score_song."""
    if isinstance(user, UserProfile):
        return {
            "preferred_genre": user.favorite_genre,
            "preferred_mood": user.favorite_mood,
            "target_energy": user.target_energy,
        }
    return user

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Union[Song, Dict]]):
        """Store the song catalog used for recommendations."""
        self.songs = songs

    def recommend(self, user: Union[UserProfile, Dict], k: int = 5) -> List[Union[Song, Dict]]:
        """Return the top-k songs (in their original form) that best match the user's preferences."""
        prefs = _user_to_prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, _song_to_dict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: Union[UserProfile, Dict], song: Union[Song, Dict]) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        _, reasons = score_song(_user_to_prefs(user), _song_to_dict(song))
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

# Experiment (Step 3 - Weight Shift): genre halved 2.0 -> 1.0, energy doubled 1.5 -> 3.0.
# Original weights: GENRE_WEIGHT = 2.0, ENERGY_WEIGHT = 1.5 (max score 6.5).
# With these weights each similarity is in [0, 1], so the max score is 1 + 1 + 3 + 1 + 1 = 7.0.
GENRE_WEIGHT = 1.0
ENERGY_WEIGHT = 3.0

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match bonus
    if song['genre'] == user_prefs['preferred_genre']:
        score += GENRE_WEIGHT
        reasons.append("Genre match")

    # +1.0 point for mood match
    if song['mood'] == user_prefs['preferred_mood']:
        score += 1.0
        reasons.append("Mood match")

    # Energy similarity
    energy_similarity = 1.0 - abs(song['energy'] - user_prefs['target_energy'])
    score += ENERGY_WEIGHT * energy_similarity
    reasons.append(f"Energy similarity: {energy_similarity:.2f}")

    # Tempo similarity (skipped if the user has no tempo preference)
    if 'target_tempo' in user_prefs:
        max_tempo = 200  # Assuming a max tempo for normalization
        tempo_similarity = 1.0 - abs(song['tempo_bpm'] - user_prefs['target_tempo']) / max_tempo
        score += 1.0 * tempo_similarity
        reasons.append(f"Tempo similarity: {tempo_similarity:.2f}")

    # Valence similarity (skipped if the user has no valence preference)
    if 'target_valence' in user_prefs:
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