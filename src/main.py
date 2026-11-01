"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# Standard user profiles
STANDARD_PROFILES = {
    "High-Energy Pop": {
        "preferred_genre": "pop",
        "preferred_mood": "happy",
        "target_energy": 0.85,
        "target_tempo": 125,
        "target_valence": 0.8,
    },
    "Chill Lofi": {
        "preferred_genre": "lofi",
        "preferred_mood": "chill",
        "target_energy": 0.35,
        "target_tempo": 75,
        "target_valence": 0.6,
    },
    "Deep Intense Rock": {
        "preferred_genre": "rock",
        "preferred_mood": "intense",
        "target_energy": 0.92,
        "target_tempo": 150,
        "target_valence": 0.45,
    },
}

# Adversarial / edge-case profiles designed to "trick" the scoring logic
ADVERSARIAL_PROFILES = {
    # Conflicting prefs: high energy but a sad mood (no "sad" songs exist in the catalog)
    "Sad but Hyped": {
        "preferred_genre": "pop",
        "preferred_mood": "sad",
        "target_energy": 0.9,
        "target_tempo": 130,
        "target_valence": 0.2,
    },
    # Genre bonus vs. everything else: metal fan who wants calm, slow, positive songs
    "Peaceful Metalhead": {
        "preferred_genre": "metal",
        "preferred_mood": "peaceful",
        "target_energy": 0.1,
        "target_tempo": 60,
        "target_valence": 0.9,
    },
    # Genre that doesn't exist in the catalog -> genre bonus can never fire
    "Ghost Genre (k-pop)": {
        "preferred_genre": "k-pop",
        "preferred_mood": "happy",
        "target_energy": 0.8,
        "target_tempo": 120,
        "target_valence": 0.8,
    },
    # Case sensitivity: "Pop"/"Happy" won't match "pop"/"happy"
    "Capitalized Pop": {
        "preferred_genre": "Pop",
        "preferred_mood": "Happy",
        "target_energy": 0.85,
        "target_tempo": 125,
        "target_valence": 0.8,
    },
    # Out-of-range values: similarities can go negative
    "Out of Range": {
        "preferred_genre": "edm",
        "preferred_mood": "party",
        "target_energy": 1.5,
        "target_tempo": 300,
        "target_valence": -0.5,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top-k recommendations for a single profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print(f"\n=== Profile: {name} ===")
    print(f"Prefs: {user_prefs}\n")
    print(f"{'#':<3} {'Title':<22} {'Genre':<11} {'Mood':<12} {'Score':<6}")
    print("-" * 58)
    for i, (song, score, _) in enumerate(recommendations, start=1):
        print(f"{i:<3} {song['title']:<22} {song['genre']:<11} {song['mood']:<12} {score:<6.2f}")
    print(f"\nTop pick explanation: {recommendations[0][2]}")


def main() -> None:
    songs = load_songs("../data/songs.csv")

    print("\n######## STANDARD PROFILES ########")
    for name, prefs in STANDARD_PROFILES.items():
        print_recommendations(name, prefs, songs)

    print("\n\n######## ADVERSARIAL / EDGE-CASE PROFILES ########")
    for name, prefs in ADVERSARIAL_PROFILES.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
