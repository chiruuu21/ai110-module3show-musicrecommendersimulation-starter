"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("../data/songs.csv")

    # Starter example profile
    user_prefs = {
        "preferred_genre": "pop",
        "preferred_mood": "happy",
        "target_energy": 0.8,
        "target_tempo": 120,
        "target_valence": 0.7
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop Recommendations:\n")
    print(f"{'Title':<30} {'Score':<10} {'Reasons'}")
    print("-" * 70)

    for rec in recommendations:
        song, score, explanation = rec
        print(f"{song['title']:<30} {score:<10.2f} {explanation}")
if __name__ == "__main__":
    main()
